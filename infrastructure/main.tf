data "aws_availability_zones" "available_zones" {
  state = "available"
}

# -----------------------------------------
# General VPC Networking
# -----------------------------------------

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

resource "aws_security_group" "sat_scan_external_sg" {
  name        = "sat_scan_external_sg"
  description = "Security group for sat scan vpc"

  vpc_id = aws_vpc.sat_scan_vpc.id

  // Allow inbound traffic to ECS on TCP port 80
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
    Name = "sat_scan_external_sg"
  }
}


resource "aws_security_group" "sat_scan_internal_sg" {
  name        = "sat_scan_internal_sg"
  description = "Security group for internal sat scan vpc communication"

  vpc_id = aws_vpc.sat_scan_vpc.id

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
    Name = "sat_scan_internal_sg"
  }
}

# -----------------------------------------
# ECS Policy Definition
# -----------------------------------------

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

# -----------------------------------------
# API SETUP
# -----------------------------------------

resource "aws_lb" "default" {
  name    = "sat-scan-load-balancer"
  subnets = aws_subnet.sat_scan_public_subnet.*.id
  security_groups = [
    aws_security_group.sat_scan_internal_sg.id,
    aws_security_group.sat_scan_external_sg.id
  ]
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

resource "aws_cloudwatch_log_group" "sat-scan-api-log-group" {
  name = "sat-scan-api-log-group"

  tags = {
    Environment = "production"
    Application = "sat-scan-api"
  }
}

resource "aws_ecs_task_definition" "sat_scan_api_ecs_task_definition" {
  family                   = "sat-scan-api-family"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 1024
  memory                   = 2048

  execution_role_arn = aws_iam_role.ecsTaskExecutionRole.arn

  tags = {
    Environment = "production"
    Application = "sat-scan-api"
  }

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
    protocol  = "tcp"
    from_port = 5000
    to_port   = 5000
    security_groups = [
      aws_security_group.sat_scan_internal_sg.id,
      aws_security_group.sat_scan_external_sg.id
    ]
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

  tags = {
    Environment = "production"
    Application = "sat-scan-cluster"
  }
}

resource "aws_ecs_service" "ecs_api_service" {
  name            = "sat-scan-api-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.sat_scan_api_ecs_task_definition.arn
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

  tags = {
    Environment = "production"
  }
}

# -----------------------------------------
# Data Collector SETUP
# -----------------------------------------

resource "aws_s3_bucket" "sat_scan_data_collector_s3" {
  bucket        = "sat-scan-data-collector"
  force_destroy = true

  tags = {
    Environment = "production"
  }
}

module "lambda_function_in_vpc" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "data_collector_lambda"
  description   = "Sat Scan Data Collection Cron"
  handler       = "index.lambda_handler"
  runtime       = "python3.8"
  timeout       = 30

  create_package = false
  s3_existing_package = {
    bucket = aws_s3_bucket.sat_scan_data_collector_s3.bucket
    key    = "lambda_code.zip"
  }

  vpc_subnet_ids = aws_subnet.sat_scan_private_subnet.*.id
  vpc_security_group_ids = [
    aws_security_group.sat_scan_internal_sg.id,
    aws_security_group.sat-scan-mq-broker-sg.id
  ]
  attach_network_policy = true

  tags = {
    Environment = "production"
    Application = "sat-scan-data-collector"
  }
}

resource "aws_cloudwatch_event_rule" "data_collector_lambda_trigger" {
  name                = "data-collector-lambda-trigger"
  description         = "Fires every 12 hours"
  schedule_expression = "rate(12 hours)"
}

resource "aws_cloudwatch_event_target" "trigger_lambda_on_schedule" {
  rule      = aws_cloudwatch_event_rule.data_collector_lambda_trigger.name
  target_id = "lambda"
  arn       = module.lambda_function_in_vpc.lambda_function_arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_split_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_function_in_vpc.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.data_collector_lambda_trigger.arn
}

# -----------------------------------------
# Data Analyzer SETUP
# -----------------------------------------

resource "aws_ecr_repository" "data_analyzer_ecr_repo" {
  name         = "data-analyzer-ecr-repo"
  force_delete = true
}

resource "aws_lb" "data-analyzer-lb" {
  name            = "data-analyzer-load-balancer"
  subnets         = aws_subnet.sat_scan_private_subnet.*.id
  security_groups = [aws_security_group.sat_scan_internal_sg.id]
}

resource "aws_lb_target_group" "data_analyzer_lb_target_group" {
  name        = "data-analyzer-lb-target-group"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.sat_scan_vpc.id
  target_type = "ip"

  health_check {
    path = "/health-check"
  }
}

resource "aws_lb_listener" "data_analyzer_lb_listener" {
  load_balancer_arn = aws_lb.data-analyzer-lb.id
  port              = "80"
  protocol          = "HTTP"

  default_action {
    target_group_arn = aws_lb_target_group.data_analyzer_lb_target_group.id
    type             = "forward"
  }
}

resource "aws_cloudwatch_log_group" "data-analyzer-log-group" {
  name = "data-analyzer-log-group"

  tags = {
    Environment = "production"
    Application = "sat-scan-data-analyzer"
  }
}


resource "aws_ecs_task_definition" "data_analyzer_ecs_task_definition" {
  family                   = "data-analyzer-family"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 1024
  memory                   = 2048

  execution_role_arn = aws_iam_role.ecsTaskExecutionRole.arn

  tags = {
    Environment = "production"
    Application = "sat-scan-data-analyzer"
  }

  container_definitions = <<DEFINITION
[
  {
    "image": "730335620736.dkr.ecr.us-east-2.amazonaws.com/data-analyzer-ecr-repo:latest",
    "cpu": 1024,
    "memory": 2048,
    "name": "data-analyzer-family",
    "networkMode": "awsvpc",
    "portMappings": [
      {
        "containerPort": 8000,
        "hostPort": 8000
      }
    ],
    "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
            "awslogs-group": "data-analyzer-log-group",
            "awslogs-region": "${var.aws_region}",
            "awslogs-stream-prefix": "data-analyzer"
          }
        }
  }
]
DEFINITION
}

resource "aws_security_group" "data_analyzer_task_sg" {
  name   = "data_analyzer_task_sg"
  vpc_id = aws_vpc.sat_scan_vpc.id

  ingress {
    protocol        = "tcp"
    from_port       = 8000
    to_port         = 8000
    security_groups = [aws_security_group.sat_scan_internal_sg.id]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ecs_service" "ecs_data_analyzer_service" {
  name            = "data-analyzer-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.data_analyzer_ecs_task_definition.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    security_groups = [aws_security_group.sat_scan_internal_sg.id]
    subnets         = aws_subnet.sat_scan_private_subnet.*.id
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.data_analyzer_lb_target_group.id
    container_name   = "data-analyzer-family"
    container_port   = 8000
  }

  depends_on = [aws_lb_listener.data_analyzer_lb_listener]

  tags = {
    Environment = "production"
  }
}


# -----------------------------------------
# RDS SETUP
# -----------------------------------------

resource "aws_security_group" "sat_scan_db_sg" {
  name        = "sat_scan_db_sg"
  description = "Security group for RDS"

  vpc_id = aws_vpc.sat_scan_vpc.id

  // Restrict RDS access to private subnets (not accessible via internet),
  // no inbound/outbound rules provided
  ingress {
    description = "Allow PostgreSQL traffic from only the web security group"
    from_port   = "5432"
    to_port     = "5432"
    protocol    = "tcp"
    security_groups = [
      # EC2 - Migration support
      aws_security_group.sat_scan_internal_sg.id,
      # API - All CRUD access
      aws_security_group.sat_scan_api_task_sg.id
    ]
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

  tags = {
    Environment = "production"
  }
}

# Create bucket to hold uploaded routes, used during continuous deployments
resource "aws_s3_bucket" "sat-scan-route-config" {
  bucket        = "sat-scan-route-config"
  force_destroy = true

  tags = {
    Environment = "production"
  }
}

# -----------------------------------------
# EC2 SETUP
# -----------------------------------------

// Create a data object called "ubuntu" that holds the latest
// Ubuntu 20.04 server AMI
data "aws_ami" "ubuntu" {
  // We want the most recent AMI
  most_recent = "true"

  // We are filtering through the names of the AMIs. We want the 
  // Ubuntu 20.04 server
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  // We are filtering through the virtualization type to make sure
  // we only find AMIs with a virtualization type of hvm
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  // This is the ID of the publisher that created the AMI. 
  // The publisher of Ubuntu 20.04 LTS Focal is Canonical 
  // and their ID is 099720109477
  owners = ["099720109477"]
}

resource "aws_key_pair" "sat_scan_kp" {
  key_name = "sat_scan_kp"

  // Used as public key for SSH key
  // Key created in same directory as main.tf
  public_key = file("sat_scan_kp.pub")
}

// Create API EC2 Instance
resource "aws_instance" "sat_scan_ec2" {
  count = var.settings.api.count

  ami           = data.aws_ami.ubuntu.id
  instance_type = var.settings.api.instance_type

  subnet_id = aws_subnet.sat_scan_public_subnet[count.index].id
  key_name  = aws_key_pair.sat_scan_kp.key_name

  vpc_security_group_ids = [aws_security_group.sat_scan_internal_sg.id]

  tags = {
    Environment = "production"
  }
}

// Create an Elastic IP for each API EC2 instance
resource "aws_eip" "sat_scan_api_eip" {
  count = var.settings.api.count

  instance = aws_instance.sat_scan_ec2[count.index].id
}

# -----------------------------------------
# Amazon MQ Broker Setup
# -----------------------------------------


resource "aws_security_group" "sat-scan-mq-broker-sg" {
  name        = "sat_scan_mq_broker_sg"
  description = "Security group for Amazon MQ"

  vpc_id = aws_vpc.sat_scan_vpc.id

  // Restrict MQ Broker access to private subnets (not accessible via internet),
  // no inbound/outbound rules provided
  ingress {
    description = "Allow traffic from internal SG"
    from_port   = "5671"
    to_port     = "5671"
    protocol    = "tcp"
    security_groups = [
      aws_security_group.data_analyzer_task_sg.id,
      aws_security_group.sat_scan_internal_sg.id,
    ]
  }

  tags = {
    Environment = "production"
    Name        = "sat_scan_mq_broker_sg"
  }
}

resource "aws_mq_broker" "sat-scan-mq-broker" {
  broker_name = "sat-scan-mq-broker"

  count              = 1
  engine_type        = "RabbitMQ"
  engine_version     = "3.12.13"
  storage_type       = "ebs"
  host_instance_type = "mq.t3.micro"
  security_groups = [
    aws_security_group.sat-scan-mq-broker-sg.id,
    aws_security_group.sat_scan_internal_sg.id,
    aws_security_group.data_analyzer_task_sg.id
  ]

  subnet_ids = [element(aws_subnet.sat_scan_private_subnet.*.id, count.index)]

  user {
    username = var.mq_username
    password = var.mq_password
  }

  logs {
    general = true
  }

  tags = {
    Environment = "production"
  }
}

# -----------------------------------------
# Grafana Cloud Integration
# -----------------------------------------

data "aws_iam_policy_document" "trust_grafana" {
  statement {
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${var.grafana_account_id}:root"]
    }
    actions = ["sts:AssumeRole"]
    condition {
      test     = "StringEquals"
      variable = "sts:ExternalId"
      values   = [var.grafana_cloud_external_id]
    }
  }
}
resource "aws_iam_role" "grafana_labs_cloudwatch_integration" {
  name        = var.grafana_cloud_iam_role_name
  description = "Role used by Grafana CloudWatch integration."
  # Allow Grafana Labs' AWS account to assume this role.
  assume_role_policy = data.aws_iam_policy_document.trust_grafana.json

  # This policy allows the role to discover metrics via tags and export them.
  inline_policy {
    name = var.grafana_cloud_iam_role_name
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = [
            "tag:GetResources",
            "cloudwatch:GetMetricData",
            "cloudwatch:ListMetrics",
            "apigateway:GET",
            "aps:ListWorkspaces",
            "autoscaling:DescribeAutoScalingGroups",
            "dms:DescribeReplicationInstances",
            "dms:DescribeReplicationTasks",
            "ec2:DescribeTransitGatewayAttachments",
            "ec2:DescribeSpotFleetRequests",
            "shield:ListProtections",
            "storagegateway:ListGateways",
            "storagegateway:ListTagsForResource"
          ]
          Resource = "*"
        }
      ]
    })
  }
}
