import re

from .command_handlers import *


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
