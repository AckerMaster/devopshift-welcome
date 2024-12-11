provider "aws" {
  region = var.region
}

variable "region" {
  default = "us-west-2"
}


variable "ami" {
  default = "ami-04feae287ec8b0244"
  
}
variable "vm_name" {
  default = "vm-[YOURNAME]"
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