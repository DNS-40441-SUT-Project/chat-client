from ...utils import connection, poll_connection


def health_check():
    connection.send(path='health_check', data='health check request')
    return connection.receive()
