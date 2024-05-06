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

  // Limit SSH traffic to local IP
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
  name            = "sat-scan-load-balancer"
  subnets         = aws_subnet.sat_scan_public_subnet.*.id
  security_groups = [aws_security_group.sat_scan_web_sg.id]
}

resource "aws_lb_target_group" "sat_scan_lb_target_group" {
  name        = "sat-scan-lb-target-group"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.sat_scan_vpc.id
  target_type = "ip"

  health_check {
    path = "/health-check"
  }
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

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

# https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html
resource "aws_iam_role" "ecsTaskExecutionRole" {
  name               = "sat-scan-ecs-execution-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = aws_iam_role.ecsTaskExecutionRole.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_cloudwatch_log_group" "sat-scan-api-log-group" {
  name = "sat-scan-api-log-group"

  tags = {
    Environment = "production"
    Application = "sat-scan-api"
  }
}

resource "aws_ecs_task_definition" "sat_scan_ecs_task_definition" {
  family                   = "sat-scan-api-family"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 1024
  memory                   = 2048

  execution_role_arn = aws_iam_role.ecsTaskExecutionRole.arn

  container_definitions = <<DEFINITION
[
  {
    "image": "730335620736.dkr.ecr.us-east-2.amazonaws.com/sat-scan:latest",
    "cpu": 1024,
    "memory": 2048,
    "name": "sat-scan-api-family",
    "networkMode": "awsvpc",
    "portMappings": [
      {
        "containerPort": 5000,
        "hostPort": 5000
      }
    ],
    "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
            "awslogs-group": "sat-scan-api-log-group",
            "awslogs-region": "${var.aws_region}",
            "awslogs-stream-prefix": "sat-scan-api"
          }
        }
  }
]
DEFINITION
}

resource "aws_security_group" "sat_scan_api_task_sg" {
  name   = "sat_scan_task_security_group"
  vpc_id = aws_vpc.sat_scan_vpc.id

  ingress {
    protocol        = "tcp"
    from_port       = 5000
    to_port         = 5000
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
  name = "sat-scan-cluster"
}

resource "aws_ecs_service" "ecs_api_service" {
  name            = "sat-scan-api-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.sat_scan_ecs_task_definition.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    security_groups = [aws_security_group.sat_scan_api_task_sg.id]
    subnets         = aws_subnet.sat_scan_private_subnet.*.id
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.sat_scan_lb_target_group.id
    container_name   = "sat-scan-api-family"
    container_port   = 5000
  }

  depends_on = [aws_lb_listener.sat_scan_lb_listener]
}

resource "aws_security_group" "sat_scan_db_sg" {
  name        = "sat_scan_db_sg"
  description = "Security group for RDS"

  vpc_id = aws_vpc.sat_scan_vpc.id

  // Restrict RDS access to private subnet (not accessible via internet), 
  // no inbound/outbound rules provided

  // Only allow traffic within sat scan web security group
  ingress {
    description     = "Allow PostgreSQL traffic from only the web security group"
    from_port       = "5432"
    to_port         = "5432"
    protocol        = "tcp"
    security_groups = [aws_security_group.sat_scan_web_sg.id]
  }

  tags = {
    Name = "sat_scan_db_sg"
  }
}

resource "aws_db_subnet_group" "sat_scan_db_subnet_group" {
  name        = "sat_scan_db_subnet_group"
  description = "DB subnet group"

  subnet_ids = [for subnet in aws_subnet.sat_scan_private_subnet : subnet.id]
}

resource "aws_db_instance" "sat_scan_database" {
  allocated_storage = var.settings.database.allocated_storage
  engine            = var.settings.database.engine
  engine_version    = var.settings.database.engine_version
  instance_class    = var.settings.database.instance_class
  db_name           = var.settings.database.db_name

  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.sat_scan_db_subnet_group.id
  vpc_security_group_ids = [aws_security_group.sat_scan_db_sg.id]

  skip_final_snapshot = var.settings.database.skip_final_snapshot
}

# Create bucket to hold uploaded routes, used during continuous deployments
resource "aws_s3_bucket" "sat-scan-route-config" {
  bucket = "sat-scan-route-config"
}


