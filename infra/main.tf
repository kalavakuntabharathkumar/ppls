terraform {
  required_version = ">= 1.6.0"
}
variable "environment" { type = string default = "dev" }
resource "null_resource" "paypulse_environment" {
  triggers = { environment = var.environment }
  provisioner "local-exec" {
    command = "echo Provisioning PayPulse environment: ${var.environment}"
  }
}
