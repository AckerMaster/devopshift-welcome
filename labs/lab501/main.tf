variable "create_vpc" {
 type    = bool
 default = true
}

variable "create_ec2" {
 type    = bool
 default = true
}

variable "YOURNAME" {
  type = string
  default = "liad"
}

resource "aws_vpc" "custom_vpc" {
 count = var.create_vpc ? 1 : 0

 cidr_block = "10.0.0.0/16"

 tags = {
   Name = "${var.YOURNAME}-vpc"
 }
}

resource "aws_instance" "example" {
  count = var.create_ec2 ? 1 : 0

  ami           = "ami-0c02fb55956c7d316" # Ubuntu AMI
  instance_type = "t2.micro"

  subnet_id = var.create_vpc ? aws_subnet.custom_subnet[0].id : data.aws_subnet.default.id
  associate_public_ip_address = var.create_vpc ? true : false  # Ensures public IP only for custom VPC

  tags = {
    Name = "${var.YOURNAME}-ec2"
  }

  depends_on = [aws_vpc.custom_vpc]
}

resource "aws_subnet" "custom_subnet" {
 count = var.create_vpc ? 1 : 0

 vpc_id            = aws_vpc.custom_vpc[0].id
 cidr_block        = "10.0.1.0/24"
 map_public_ip_on_launch = true

 tags = {
   Name = "${var.YOURNAME}-subnet"
 }
}

data "aws_subnet" "default" {
  filter {
    name   = "default-for-az"
    values = ["true"]
  }

  filter {
    name   = "availability-zone"
    values = ["us-east-1a"]  # Change to your preferred AZ
  }
}

# OUTPUTS : please print to machine ip and [vpcid + subnetid] using the following "The following is your {VPCID} and {SUBNET}"

output "vpc_and_subnet_info" {
  value = var.create_vpc ? "The following is your VPC ID: ${aws_vpc.custom_vpc[0].id} and Subnet ID: ${aws_subnet.custom_subnet[0].id}" : "Using default VPC"
}

output "ec2_public_ip" {
  value = var.create_ec2 ? aws_instance.example[0].public_ip : "No EC2 instance created"
}