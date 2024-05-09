output "database_port" {
  description = "The port of the database"
  value       = aws_db_instance.sat_scan_database.port
}

output "database_endpoint" {
  description = "The endpoint of the database"
  value       = aws_db_instance.sat_scan_database
  sensitive   = true
}

output "load_balancer_ip" {
  value = aws_lb.default.dns_name
}

output "ec2_dns" {
  description = "Public DNS address of the EC2 instance (~jumpbox)"
  value       = aws_eip.sat_scan_api_eip[0].public_dns
  depends_on  = [aws_eip.sat_scan_api_eip]
}

output "mq_broker" {
  description = "Connection information for MQ Broker"
  value       = aws_mq_broker.sat-scan-mq-broker
  sensitive   = true
}
