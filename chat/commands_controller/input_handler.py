import re

from .command_handlers import *
from ..data import LoggedInUser


def handle_input(message):
    if re.search('^help$', message):
        return help_handler()
    if re.search('^error$', message):
        return error_handler()
    if re.search('^exit$', message):
        # todo: run logout before it
        return exit_handler()
    if re.search('^connection_health_check$', message):
        return health_check()
    if re.search('^connection_health_check_enc$', message):
        return health_check_enc()
    if re.search('^message to (\S+)$', message):
        other_user = re.match('^message to (\S+)$', message).group(1)
        print('please input message')
        message = input()
        message_to_user(other_user, message)
    if re.search('^login (\S+) (\S+)$', message):
        username = re.match('^login (\S+) (\S+)$', message).group(1)
        password = re.match('^login (\S+) (\S+)$', message).group(2)
        try:
            LoggedInUser.login(username, password)
        except LoggedInUser.Exceptions.ALREADY_LOGGED_IN:
            print('You are already logged in. please first log out.')
        else:
            print('You are logged in!')
