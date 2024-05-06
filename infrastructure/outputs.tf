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
