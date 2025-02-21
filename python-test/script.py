from jinja2 import Template

ami_options = {
    "ubuntu": "ami-0e1bed4f06a3b463d",
    "amazon-linux": "ami-053a45fff0a704a47"
}

instance_types = {
    "small": "t3.small",
    "medium": "t3.medium"
}

region = input("please enter AWS region: ").strip().lower()
if region != "us-east-1":
    print("invalid region. using default 'us-east-1'")
    region = "us-east-1"

# the user choises
ami_choise = input("please chose AMI [ubuntu / amazon-linux]: ").strip().lower()
instance_type_choise = input("please chose instance type [small / medium]: ").strip().lower()
availability_zone = "us-east-1a"
load_balancer_name = input("please enter ALB name: ").strip().lower()

ami = ami_options.get(ami_choise, "ami-0e1bed4f06a3b463d") # setting default in case something goes wrong
instance_type = instance_types.get(instance_type_choise, "t3.small") # same here

terraform_template = Template("""
provider "aws" {
  region = "{{ region }}"
}

resource "aws_instance" "web_server" {
  ami = "{{ ami }}"
  instance_type = "{{ instance_type }}"
  availability_zone = "{{ availability_zone }}"

  tags = {
    Name = "WebServer"
  }
}

resource "aws_lb" "application_lb" {
  name = "{{ load_balancer_name }}"
  internal = false
  load_balancer_type = "application"
  security_groups = [aws_security_group.lb_sg.id]
  subnets = aws_subnet.public[*].id
}

resource "aws_security_group" "lb_sg" {
  name        = "lb_security_group"
  description = "Allow HTTP inbound traffic"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
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
  name     = "web-target-group"
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

""")

# creating the tf file using the inputs fron the user
tf_file = terraform_template.render(
    region = region,
    ami = ami,
    instance_type = instance_type,
    availability_zone = availability_zone,
    load_balancer_name = load_balancer_name
)

#writing into the file
with open("terraform_test.tf", "w") as f:
    f.write(tf_file)

print(" created terraform file based on your input, check 'terraform_test.tf")

