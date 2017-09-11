import socket

from mitm import BaseMitmRequestHandler

destination_endpoint = None


def set_destination_endpoint(endpoint):
    global destination_endpoint
    destination_endpoint = endpoint


class BaseFixedDestinationMitmRequestHandler(BaseMitmRequestHandler):
    def connect_to_destination(self):
        assert destination_endpoint is not None
        return socket.create_connection(destination_endpoint)
