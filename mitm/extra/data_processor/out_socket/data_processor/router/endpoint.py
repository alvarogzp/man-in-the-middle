from mitm.extra.data_processor.config import MESSAGE_ENDPOINT_SERVER, MESSAGE_ENDPOINT_CLIENT


class EndpointRouter:
    def __init__(self, server_socket, client_socket):
        self.server_socket = server_socket
        self.client_socket = client_socket

    def get(self, endpoint):
        if endpoint == MESSAGE_ENDPOINT_SERVER:
            return self.client_socket
        elif endpoint == MESSAGE_ENDPOINT_CLIENT:
            return self.server_socket
