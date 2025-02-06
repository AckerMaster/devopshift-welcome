module "outputdemo" {
  
  source = "./modules/outputdemo" 
  instance_type = "t2.micro"
  subnrt_id = "10.0.0.1/16"
  ami = "i0-3431512441fg"
  message = "hello class"

}

output "test" {
  value = module.outputdemo
}