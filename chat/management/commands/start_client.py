import threading

from django.conf import settings
from django.core.management.base import BaseCommand

from chat.commands_controller import handle_input
from chat.request_handlers import handle_poll_input
from chat.utils import poll_connection


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
            self.log(message)
        except Exception as e:
            self.log_error(str(e))

    def handle_poll_requests(self):
        self.log('initiating handle poll requests')
        while True:
            message = poll_connection.recieve_decrypted(private_key=settings.PRIVATE_KEY)
            handle_poll_input(message)

    def handle(self, *args, **options):
        threading.Thread(target=self.handle_poll_requests)
        self.print('help')

        while True:
            input_message = input('-> ')
            self.print(input_message)
