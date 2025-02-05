provider "aws" {
  region = var.region
}

variable "region" {
  default = "us-east-1"
}


data "aws_instances" "yaniv_vm" {
  filter {
    name   = "tag:Name"
    values = ["yaniv-vm"]
  }
}

data "aws_instance" "yaniv_vm_details" {
  instance_id = tolist(data.aws_instances.yaniv_vm.ids)[0]
}

output "lecturer_public_ip" {
  value       = data.aws_instance.yaniv_vm_details.public_ip
  description = "Public IP address of the lecturer's VM"
}