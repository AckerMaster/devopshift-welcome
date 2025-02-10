servers_dict = {
    
    "Nginx": "Running",
    "Docker": "Not Running",
    "Terraform": "Running",
    "kubernetes": "Running",
    "AWS": "Not Running"
}


while True:
    user_input = input("Please Enter server name: ")
    try:
        print(f"{user_input} is {servers_dict[user_input]}")
        break
    except KeyError:
            print("Server is not recognized. type 'quit' to leave or 'list' for servers list")
    
    if (user_input == "quit"):
            print("Okay, Bye")
            break
    if (user_input == "list"):
        print("Current Servers are: ")
        for item in servers_dict:
            print(item)
        
