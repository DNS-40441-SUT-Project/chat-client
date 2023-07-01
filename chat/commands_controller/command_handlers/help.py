message = """
Welcome to chat client app!
please write your command to continue:            

# auth
login: <username> <password>
register: <username> <password>
logout

# online users
all_online_users

# group management
groups
create_group <group_name>
delete_group <group_pk>
add_member_to_group <group_pk> <member_username>
remove_member_from_group <group_pk> <member_username>

# wanna see this message again?
help

#health_check
connection_health_check

# bye bye?
exit
                """


def help_handler():
    return message
