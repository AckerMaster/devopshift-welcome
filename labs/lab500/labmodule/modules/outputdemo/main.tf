variable "message" {}
variable "instance_type" {}
variable "subnrt_id" {}
variable "ami" {}


resource "aws_instance" "instance" {
  ami           = var.ami
  instance_type = var.instance_type
  subnet_id     = var.subnrt_id
}

