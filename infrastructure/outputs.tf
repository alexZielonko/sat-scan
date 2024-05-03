output "api_public_ip" {
  description = "The public IP address of the Sat Scan API"
  value       = aws_eip.sat_scan_api_eip[0].public_ip
  depends_on  = [aws_eip.sat_scan_api_eip]
}

output "api_public_dns" {
  description = "The public DNS address of the Sat Scan API server"
  value       = aws_eip.sat_scan_api_eip[0].public_dns
  depends_on  = [aws_eip.sat_scan_api_eip]
}

output "database_endpoint" {
  description = "The endpoint of the database"
  value       = aws_db_instance.sat_scan_database
  sensitive   = true
}

output "database_port" {
  description = "The port of the database"
  value       = aws_db_instance.sat_scan_database.port
}
