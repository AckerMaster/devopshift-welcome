 # ------------------------ Python Test ------------------------ #
 
 Name: Liad Ackerman
 
 ID: 315487710

 # ------------------- How to run the script ------------------- #

 1. make sure to install all required modules from requirements.txt
 
 2. run "script.py", it will ask you for region, AMI, instance type & alb name.
 then it will generate a "terraform_test.tf" file with your inputs

 3. then you need to run "python_tf.py" to init, plan and apply the generated tf file.
 
 --> if not working - try to run MANUALLY "terraform init" and "terraform apply" in the terminal, it should work

 4. run "val_script.py" for it to create a json file with the requested info about
 the ec2 and alb. the data will be stored in a generated "aws_validation.json"