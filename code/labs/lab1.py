servers_dict = {
    
    "Nginx": "Running",
    "Docker": "Not Running",
    "Terraform": "Running",
    "kubernetes": "Running",
    "AWS": "Not Running"
}


while True:
    try:
        x = input("Please Enter server name: ")
        print(f"{x} is {servers_dict[x]}")
        break
    except:
        if x == "quit":
            print("Okay, Bye")
            break
        if x == "list":
            print("Current Servers are: ")
            for item in servers_dict:
                print(item)
        else:
            print("Server is not recognized. type 'quit' to leave or 'list' for servers list")