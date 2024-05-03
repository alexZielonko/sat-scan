data "aws_availability_zones" "available_zones" {
  state = "available"
}

resource "aws_vpc" "sat_scan_vpc" {
  cidr_block           = var.vpc_cidr_block
  enable_dns_hostnames = true
  tags = {
    Name = "sat_scan_vpc"
  }
}

resource "aws_subnet" "sat_scan_public_subnet" {
  count                   = 2
  cidr_block              = cidrsubnet(aws_vpc.sat_scan_vpc.cidr_block, 8, 2 + count.index)
  availability_zone       = data.aws_availability_zones.available_zones.names[count.index]
  vpc_id                  = aws_vpc.sat_scan_vpc.id
  map_public_ip_on_launch = true
  tags = {
    Name = "sat_scan_public_subnet${count.index}"
  }
}

resource "aws_subnet" "sat_scan_private_subnet" {
  count             = 2
  cidr_block        = cidrsubnet(aws_vpc.sat_scan_vpc.cidr_block, 8, count.index)
  availability_zone = data.aws_availability_zones.available_zones.names[count.index]
  vpc_id            = aws_vpc.sat_scan_vpc.id
  tags = {
    Name = "sat_scan_private_subnet_${count.index}"
  }
}

resource "aws_internet_gateway" "gateway" {
  vpc_id = aws_vpc.sat_scan_vpc.id
}

resource "aws_route" "internet_access" {
  route_table_id         = aws_vpc.sat_scan_vpc.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.gateway.id
}

resource "aws_eip" "gateway" {
  count      = 2
  vpc        = true
  depends_on = [aws_internet_gateway.gateway]
}

resource "aws_nat_gateway" "gateway" {
  count         = 2
  subnet_id     = element(aws_subnet.sat_scan_public_subnet.*.id, count.index)
  allocation_id = element(aws_eip.gateway.*.id, count.index)
}

resource "aws_route_table" "private" {
  count  = 2
  vpc_id = aws_vpc.sat_scan_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = element(aws_nat_gateway.gateway.*.id, count.index)
  }
}

resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = element(aws_subnet.sat_scan_private_subnet.*.id, count.index)
  route_table_id = element(aws_route_table.private.*.id, count.index)
}

resource "aws_security_group" "sat_scan_web_sg" {
  name        = "sat_scan_web_sg"
  description = "Security group for sat scan vpc"

  vpc_id = aws_vpc.sat_scan_vpc.id

  // Allow inbound traffic to EC2 on TCP port 80
  ingress {
    description = "Allow all traffic through HTTP"
    from_port   = "80"
    to_port     = "80"
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  // Limit EC2 SSH traffic to local IP
  ingress {
    description = "Allow SSH from my computer"
    from_port   = "22"
    to_port     = "22"
    protocol    = "tcp"
    cidr_blocks = ["${var.local_ip}/32"]
  }

  // Allow all outbound traffic
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "sat_scan_web_sg"
  }
}

resource "aws_lb" "default" {
  name            = "sat_scan_load_balancer"
  subnets         = aws_subnet.sat_scan_public_subnet.*.id
  security_groups = [aws_security_group.sat_scan_web_sg.id]
}

resource "aws_lb_target_group" "sat_scan_lb_target_group" {
  name        = "sat_scan_lb_target_group"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.sat_scan_vpc.id
  target_type = "ip"
}

resource "aws_lb_listener" "sat_scan_lb_listener" {
  load_balancer_arn = aws_lb.default.id
  port              = "80"
  protocol          = "HTTP"

  default_action {
    target_group_arn = aws_lb_target_group.sat_scan_lb_target_group.id
    type             = "forward"
  }
}

resource "aws_ecs_task_definition" "sat_scan_ecs_task_definition" {
  family                   = "hello-world-app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 1024
  memory                   = 2048

  container_definitions = <<DEFINITION
[
  {
    "image": "registry.gitlab.com/architect-io/artifacts/nodejs-hello-world:latest",
    "cpu": 1024,
    "memory": 2048,
    "name": "hello-world-app",
    "networkMode": "awsvpc",
    "portMappings": [
      {
        "containerPort": 3000,
        "hostPort": 3000
      }
    ]
  }
]
DEFINITION
}

resource "aws_security_group" "sat_scan_api_task_sg" {
  name   = "sat_scan_task_security_group"
  vpc_id = aws_vpc.sat_scan_vpc.id

  ingress {
    protocol        = "tcp"
    from_port       = 3000
    to_port         = 3000
    security_groups = [aws_security_group.sat_scan_web_sg.id]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ecs_cluster" "main" {
  name = "sat_scan_cluster"
}

resource "aws_ecs_service" "ecs_api_service" {
  name            = "hello-world-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.ecs_api_service.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    security_groups = [aws_security_group.sat_scan_api_task_sg.id]
    subnets         = aws_subnet.sat_scan_private_subnet.*.id
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.hello_world.id
    container_name   = "hello-world-app"
    container_port   = 3000
  }

  depends_on = [aws_lb_listener.hello_world]
}

# resource "aws_security_group" "sat_scan_db_sg" {
#   name        = "sat_scan_db_sg"
#   description = "Security group for RDS"

#   vpc_id = aws_vpc.sat_scan_vpc.id

#   // Restrict RDS access to private subnet (not accessible via internet), 
#   // no inbound/outbound rules provided

#   // Allow traffic between EC2 security group to the DB security group
#   ingress {
#     description     = "Allow PostgreSQL traffic from only the web security group"
#     from_port       = "5432"
#     to_port         = "5432"
#     protocol        = "tcp"
#     security_groups = [aws_security_group.sat_scan_web_sg.id]
#   }

#   tags = {
#     Name = "sat_scan_db_sg"
#   }
# }

# resource "aws_db_subnet_group" "sat_scan_db_subnet_group" {
#   name        = "sat_scan_db_subnet_group"
#   description = "DB subnet group"

#   subnet_ids = [for subnet in aws_subnet.sat_scan_private_subnet : subnet.id]
# }

# resource "aws_db_instance" "sat_scan_database" {
#   allocated_storage = var.settings.database.allocated_storage
#   engine            = var.settings.database.engine
#   engine_version    = var.settings.database.engine_version
#   instance_class    = var.settings.database.instance_class
#   db_name           = var.settings.database.db_name

#   username = var.db_username
#   password = var.db_password

#   db_subnet_group_name   = aws_db_subnet_group.sat_scan_db_subnet_group.id
#   vpc_security_group_ids = [aws_security_group.sat_scan_db_sg.id]

#   skip_final_snapshot = var.settings.database.skip_final_snapshot
# }

# resource "aws_key_pair" "sat_scan_kp" {
#   key_name = "sat_scan_kp"

#   // Used as public key for SSH key
#   // Key created in same directory as main.tf
#   public_key = file("sat_scan_kp.pub")
# }

# // Create API EC2 Instance
# resource "aws_instance" "sat_scan_api" {
#   count = var.settings.api.count

#   ami           = data.aws_ami.ubuntu.id
#   instance_type = var.settings.api.instance_type

#   subnet_id = aws_subnet.sat_scan_public_subnet[count.index].id
#   key_name  = aws_key_pair.sat_scan_kp.key_name

#   vpc_security_group_ids = [aws_security_group.sat_scan_web_sg.id]

#   tags = {
#     Name = "sat_scan_api${count.index}"
#   }
# }

# // Create an Elastic IP for each API EC2 instance
# resource "aws_eip" "sat_scan_api_eip" {
#   count = var.settings.api.count

#   instance = aws_instance.sat_scan_api[count.index].id

#   // Place Elastic IP in the VPC
#   vpc = true

#   tags = {
#     Name = "sat_scan_api_eip_${count.index}"
#   }
# }
