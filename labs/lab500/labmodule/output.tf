module "ec2" {
  source       = "./modules/ec2"
  ami          = "ami-0c02fb55956c7d316"
  machine_type  = "t2.micro"
  machine_name  = "liad-vm"
}

output "print_machine_name" {
  value = module.ec2.print_machine_name
}

output "print_machine_type" {
  value = module.ec2.print_machine_type
}

output "print_ami" {
  value = module.ec2.print_ami
}

output "vm_public_ip" {
  value = module.ec2.vm_public_ip
}