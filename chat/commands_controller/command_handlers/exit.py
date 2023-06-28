from ...utils import connection, poll_connection


def exit_handler():
    connection.close()
    poll_connection.close()
    exit(0)
