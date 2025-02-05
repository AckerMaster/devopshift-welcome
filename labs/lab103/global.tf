provider "aws" {
 region = var.region
}

variable "region" {
 default = "us-east-1"
}


variable "ami" {
 default = "ami-0ecc0e0d5986a576d"
 }
variable "vm_name" {
 default = "vm-liad"
}

variable "admin_username" {
 default = "admin-user"
}

variable "admin_password" {
 default = "Password123!"
}

variable "vm_size" {
 default = "t2.micro"
}

data "aws_ami" "selected_ami" {
  most_recent = true  # Fetches the latest version of the image
  owners      = ["self"]  # Filters only AMIs owned by your AWS account

  filter {
    name   = "name"
    values = ["terraform-workshop-image-do-not-delete"]
  }

  filter {
    name   = "state"
    values = ["available"]
  }
}

output "selected_ami_id" {
  value       = data.aws_ami.selected_ami.id
  description = "AMI ID that was dynamically selected based on filters"
}