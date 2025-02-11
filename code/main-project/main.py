from log import setup_logging

# logger
logger = setup_logging()

# servers list and status
servers_dict = {
    
    "Nginx": "Running",
    "Docker": "Not Running",
    "Terraform": "Running",
    "Kubernetes": "Running",
    "AWS": "Not Running"
}

# converting servers name to lower case
new_servers_dict = { key.strip().lower() : value for key, value in servers_dict.items()}

# asking for user input until completion
while True:
    user_input = input("Please Enter server name: ")
    user_input = user_input.strip().lower()
    logger.info(f"The user chose: {user_input}")
    try:
        print(f"{user_input} is {new_servers_dict[user_input]}")
        break
    except KeyError:
            print("Server is not recognized. type 'quit' to leave or 'list' for servers list")
            logger.error("Invalid Input from user")
    
    if (user_input == "quit"):
            print("Okay, Bye")
            logger.info(f"The user chose to quit")
            break
    if (user_input == "list"):
        print("Current Servers are: ")
        logger.info(f"The user chose to view all servers")
        for item in new_servers_dict:
            print(item)
        



#---------------------------------------------------------------------#
#----------------------- Another main function -----------------------#
#---------------------------------------------------------------------#

# servers = {"nginx": True, "docker" : False}

# def get_server_status(server_name: str) -> bool:
    
#     try:
#         return servers[server_name]
#     except KeyError:
#         logger.error("This server does not exist")
#     return False 
        
# while True:
#     server_name = input("Please Enter server name: ")
#     server_name = server_name.lower()
#     status = get_server_status(server_name)
#     logger.info(f"Server status is {str(status)}")
