import boto3
import json

def load_terraform_output():
    with open("terraform.tfstate", "r") as f:
        state = json.load(f)
    return state


def get_instance_details(instance_id):
    ec2_client = boto3.client("ec2")
    try:
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        instance = response["Reservation"][0]["Instances"][0]
        return {
            "instance_id": instance_id,
            "instance_state": instance["State"]["Name"],
            "public_ip": instance.get("PublicIpAddress", "not found")
        }
    except Exception as exc:
        print(f"error getting ec2 info: {exc}")
        return None

def get_alb_details(load_balancer_name):
    elb_client = boto3.client("elbv2")
    try:
        response = elb_client.describe_load_balancers(Name=[load_balancer_name])
        alb = response["LoadBalancers"][0]
        return {
            "load_balancer_dns": alb["DNSName"]
        }

    except Exception as exc:
        print(f"error getting alb info: {exc}")
        return None