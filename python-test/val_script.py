import boto3
import json

def load_terraform_output():
    with open("terraform.tfstate", "r") as f:
        state = json.load(f)
    return state

#getting ec2 info
def get_instance_details(instance_id):
    ec2_client = boto3.client("ec2")
    try:
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        instance = response["Reservations"][0]["Instances"][0]
        return {
            "instance_id": instance_id,
            "instance_state": instance["State"]["Name"],
            "public_ip": instance.get("PublicIpAddress", "not found")
        }
    except Exception as exc:
        print(f"error getting ec2 info: {exc}")
        return None

# getting alb info
def get_alb_details(load_balancer_name):
    elb_client = boto3.client("elbv2")
    try:
        response = elb_client.describe_load_balancers(Names=[load_balancer_name])
        alb = response["LoadBalancers"][0]
        return {
            "load_balancer_dns": alb["DNSName"]
        }

    except Exception as exc:
        print(f"error getting alb info: {exc}")
        return None

# validating and saving info into json file
def validate():
    state = load_terraform_output()
    instance_id = state["outputs"]["instance_id"]["value"]
    alb_dns = state["outputs"]["alb_dns"]["value"]
    load_balancer_name = alb_dns.split(".")[0]

    # getting the instance info from our previous func
    ec2_data = get_instance_details(instance_id)

    # getting the alb info from our previous func
    alb_data = get_alb_details(load_balancer_name)

    if ec2_data and alb_data:
        # putting the data together as we learned from Ofer
        validation_data = {**ec2_data, **alb_data}

        with open("aws_validation.json", "w") as f:
            json.dump(validation_data, f, indent=4)
        print("aws val data saved in 'aws_validation.json'")
    else:
        print("failed to get info from aws ..")

if __name__ == "__main__":
    validate()