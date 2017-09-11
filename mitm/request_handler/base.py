import SocketServer
import socket

from mitm.config import DESTINATION_ENDPOINT


class BaseMitmRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        server_socket = self.connect_to_destination()
        self.setup_mitm(server_socket, self.request)
        self.loop()

    def connect_to_destination(self):
        return socket.create_connection(DESTINATION_ENDPOINT)

    def setup_mitm(self, server_socket, client_socket):
        raise NotImplementedError()

    def loop(self):
        raise NotImplementedError()
