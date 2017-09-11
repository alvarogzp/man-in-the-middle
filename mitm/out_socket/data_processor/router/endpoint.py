from mitm.config import ENDPOINT_SERVER, ENDPOINT_CLIENT


class EndpointRouter:
    def __init__(self, server_socket, client_socket):
        self.server_socket = server_socket
        self.client_socket = client_socket

    def get(self, endpoint):
        if endpoint == ENDPOINT_SERVER:
            return self.client_socket
        elif endpoint == ENDPOINT_CLIENT:
            return self.server_socket
