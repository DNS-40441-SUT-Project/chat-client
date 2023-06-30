import re

from .command_handlers import *
from ..data import LoggedInUser


def handle_input(message):
    if re.search('^help$', message):
        return help_handler()
    if re.search('^error$', message):
        return error_handler()
    if re.search('^exit$', message):
        return exit_handler()
    if re.search('^all_online_users$', message):
        return get_online_users()
    if re.search('^connection_health_check$', message):
        return health_check()
    if re.search('^message to (\S+)$', message):
        other_user = re.match('^message to (\S+)$', message).group(1)
        print('please input message')
        message = input()
        message_to_user(other_user, message)
    if re.search('^login (\S+) (\S+)$', message):
        username = re.match('^login (\S+) (\S+)$', message).group(1)
        password = re.match('^login (\S+) (\S+)$', message).group(2)
        return LoggedInUser.login(username, password)
    if re.search('^register (\S+) (\S+)$', message):
        username = re.match('^register (\S+) (\S+)$', message).group(1)
        password = re.match('^register (\S+) (\S+)$', message).group(2)
        return handle_register(username, password)
    if re.search('^logout$', message):
        return handle_logout()
