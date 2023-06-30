from django.core.management.base import BaseCommand

from chat.commands_controller import handle_input
from chat.commands_controller.command_handlers import exit_handler
import signal


def handle_signal(signum: int, *args):
    exit_handler()


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


class Command(BaseCommand):
    help = "start the client for chat app"

    def log(self, message):
        self.stdout.write(
            self.style.SUCCESS(
                str(message),
            ),
        )

    def log_error(self, message):
        self.stdout.write(
            self.style.ERROR(
                str(message),
            ),
        )

    def print(self, user_input):
        try:
            message = handle_input(user_input)
            if message:
                self.log(message)
        except Exception as e:
            self.log_error(str(e))

    def handle(self, *args, **options):
        self.print('help')

        while True:
            input_message = input('-> ')
            self.print(input_message)
