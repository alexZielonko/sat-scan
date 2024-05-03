terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws_region
}

data "aws_availability_zones" "available" {
  state = "available"
}

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

resource "aws_vpc" "sat_scan_vpc" {
  cidr_block           = var.vpc_cidr_block
  enable_dns_hostnames = true

  tags = {
    Name = "sat_scan_vpc"
  }
}

resource "aws_internet_gateway" "sat_scan_igw" {
  // Attaching the IGW to the vpc
  vpc_id = aws_vpc.sat_scan_vpc.id

  tags = {
    Name = "sat_scan_igw"
  }
}

resource "aws_subnet" "sat_scan_public_subnet" {
  count = var.subnet_count.public

  // Place the subnet into the "sat_scan_vpc" VPC
  vpc_id = aws_vpc.sat_scan_vpc.id

  cidr_block        = var.public_subnet_cidr_blocks[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "sat_scan_public_subnet${count.index}"
  }
}

resource "aws_subnet" "sat_scan_private_subnet" {
  count = var.subnet_count.private

  vpc_id = aws_vpc.sat_scan_vpc.id

  cidr_block        = var.private_subnet_cidr_blocks[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "sat_scan_private_subnet_${count.index}"
  }
}

resource "aws_route_table" "sat_scan_public_rt" {
  vpc_id = aws_vpc.sat_scan_vpc.id

  // Route with destination of 0.0.0.0/0 to acccess internet
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.sat_scan_igw.id
  }
}

resource "aws_route_table_association" "public" {
  count = var.subnet_count.public

  route_table_id = aws_route_table.sat_scan_public_rt.id

  subnet_id = aws_subnet.sat_scan_public_subnet[count.index].id
}

resource "aws_route_table" "sat_scan_private_rt" {
  vpc_id = aws_vpc.sat_scan_vpc.id
}


resource "aws_route_table_association" "private" {
  count = var.subnet_count.private

  route_table_id = aws_route_table.sat_scan_private_rt.id

  subnet_id = aws_subnet.sat_scan_private_subnet[count.index].id
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

resource "aws_security_group" "sat_scan_db_sg" {
  name        = "sat_scan_db_sg"
  description = "Security group for RDS"

  vpc_id = aws_vpc.sat_scan_vpc.id

  // Restrict RDS access to private subnet (not accessible via internet), 
  // no inbound/outbound rules provided

  // Allow traffic between EC2 security group to the DB security group
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

resource "aws_key_pair" "sat_scan_kp" {
  key_name = "sat_scan_kp"

  // Used as public key for SSH key
  // Key created in same directory as main.tf
  public_key = file("sat_scan_kp.pub")
}

// Create API EC2 Instance
resource "aws_instance" "sat_scan_api" {
  count = var.settings.api.count

  ami           = data.aws_ami.ubuntu.id
  instance_type = var.settings.api.instance_type

  subnet_id = aws_subnet.sat_scan_public_subnet[count.index].id
  key_name  = aws_key_pair.sat_scan_kp.key_name

  vpc_security_group_ids = [aws_security_group.sat_scan_web_sg.id]

  tags = {
    Name = "sat_scan_api${count.index}"
  }
}

// Create an Elastic IP for each API EC2 instance
resource "aws_eip" "sat_scan_api_eip" {
  count = var.settings.api.count

  instance = aws_instance.sat_scan_api[count.index].id

  // Place Elastic IP in the VPC
  vpc = true

  tags = {
    Name = "sat_scan_api_eip_${count.index}"
  }
}
