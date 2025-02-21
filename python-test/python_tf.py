import os
from python_terraform import Terraform

def run_tf():
    try:
        tf = Terraform(working_dir = ".")
        print("initializing terraform..")
        init_return_code, init_stdout, init_stderr = tf.init()
        print(init_stdout)

        if init_return_code != 0:
            print(f"terraform init failed: {init_stderr}")
            return

        print("planning terraform..")
        plan_return_code, plan_stdout, plan_stderr = tf.plan()
        print(plan_stdout)

        if plan_return_code != 0:
            print(f"terraform plan failed: {plan_stderr}")
            return

        print("applying terraform..")
        apply_return_code, apply_stdout, apply_stderr = tf.apply(skip_plan=True)
        print(apply_stdout)

        if apply_return_code != 0:
            print(f"terraform apply failed: {apply_stderr}")
            return

        print("terraform applyed without issues")

        output = tf.output()
        
        instance_info = output.get("instance_id", {})
        instance_id = instance_info.get("value", "not found")

        alb_info = output.get("alb_dns", {})
        alb_dns = alb_info.get("value", "not found")

        print(f"the ec2 instance id is: {instance_id}")
        print(f"the alb dns is: {alb_dns}")

    except Exception as exc:
        print(f"an error happened: {exc}")


if __name__ == "__main__":
    run_tf()