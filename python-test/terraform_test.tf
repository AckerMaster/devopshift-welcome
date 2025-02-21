
provider "aws" {
  region = "us-east-1"
}

resource "random_string" "suffix" {
  length  = 4
  special = false
  upper   = false
}

resource "aws_instance" "web_server" {
  ami = "ami-0e1bed4f06a3b463d"
  instance_type = "t3.medium"
  availability_zone = "us-east-1a"
  subnet_id = aws_subnet.public[0].id
  associate_public_ip_address = true

  tags = {
    Name = "WebServer"
  }
}

resource "aws_lb" "application_lb" {
  name = "liad-alb"
  internal = false
  load_balancer_type = "application"
  security_groups = [aws_security_group.lb_sg.id]
  subnets = aws_subnet.public[*].id
}

resource "aws_security_group" "lb_sg" {
  name        = "lb_security_group_${random_string.suffix.result}"
  description = "Allow HTTP inbound traffic"

  vpc_id =aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]  # Allow all outgoing traffic
  }
}

resource "aws_lb_listener" "http_listener" {
  load_balancer_arn = aws_lb.application_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web_target_group.arn
  }
}

resource "aws_lb_target_group" "web_target_group" {
  name     = "web-target-group-${random_string.suffix.result}"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}

resource "aws_lb_target_group_attachment" "web_instance_attachment" {
  target_group_arn = aws_lb_target_group.web_target_group.arn
  target_id        = aws_instance.web_server.id
}

resource "aws_subnet" "public" {
  count = 2
  vpc_id = aws_vpc.main.id
  cidr_block = "10.0.${count.index}.0/24"
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}


resource "aws_internet_gateway" "main_gw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "MainInternetGateway"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main_gw.id
  }
}

resource "aws_route_table_association" "public_association" {
  count           = 2
  subnet_id       = aws_subnet.public[count.index].id
  route_table_id  = aws_route_table.public_rt.id
}



output "instance_id" {
  value = aws_instance.web_server.id
}

output "alb_dns" {
  value = aws_lb.application_lb.dns_name
}
