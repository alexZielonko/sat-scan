variable "aws_region" {
  default = "us-east-2"
}


variable "vpc_cidr_block" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

// EC2 and RDS configuration settings
variable "settings" {
  description = "Configuration settings"
  type        = map(any)
  default = {
    "database" = {
      allocated_storage   = 20            // storage in gigabytes
      engine              = "postgres"    // engine type
      engine_version      = "16.1"        // engine version
      instance_class      = "db.t3.micro" // rds instance type
      db_name             = "sat_scan_db" // database name
      skip_final_snapshot = true
    },
    "api" = {
      count         = 1          // the number of EC2 instances
      instance_type = "t2.micro" // the EC2 instance
    }
  }
}

variable "public_subnet_cidr_blocks" {
  description = "Available CIDR blocks for public subnets"
  type        = list(string)
  default = [
    "10.0.1.0/24",
    "10.0.2.0/24",
    "10.0.3.0/24",
    "10.0.4.0/24"
  ]
}

// This variable contains the CIDR blocks for
// the public subnet. I have only included 4 
// for this tutorial, but if you need more you
// would add them here
variable "private_subnet_cidr_blocks" {
  description = "Available CIDR blocks for private subnets"
  type        = list(string)
  default = [
    "10.0.101.0/24",
    "10.0.102.0/24",
    "10.0.103.0/24",
    "10.0.104.0/24",
  ]
}

// This variable contains your local IP address. This
// is used when setting up the SSH rule on the
// web security group
variable "local_ip" {
  description = "Local IP address"
  type        = string
  sensitive   = true
}

// This variable contains the database master user
// We will be storing this in a secrets file
variable "db_username" {
  description = "Database master user"
  type        = string
  sensitive   = true
}

// This variable contains the database master password
// We will be storing this in a secrets file
variable "db_password" {
  description = "Database master user password"
  type        = string
  sensitive   = true
}