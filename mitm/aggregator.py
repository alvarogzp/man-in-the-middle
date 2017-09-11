from mitm.out_socket.data_processor.router import EndpointRouter


class MitmSocketAggregator:
    def __init__(self, server_socket, client_socket, recv_socket, send_socket):
        self.server_out_socket = server_socket
        self.client_out_socket = client_socket
        self.recv_socket = recv_socket
        self._send_socket = send_socket

    def send_socket(self, server_socket, client_socket):
        self._send_socket.processor.set_router(EndpointRouter(server_socket, client_socket))
        return self._send_socket
