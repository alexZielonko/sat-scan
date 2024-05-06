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

output "api_public_dns" {
  description = "The public DNS address of the Sat Scan API server"
  value       = aws_eip.sat_scan_api_eip[0].public_dns
  depends_on  = [aws_eip.sat_scan_api_eip]
}
