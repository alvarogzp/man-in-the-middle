import SocketServer


class BaseMitmRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        server_socket = self.connect_to_destination()
        self.setup_mitm(server_socket, self.request)
        self.loop()

    def connect_to_destination(self):
        raise NotImplementedError()

    def setup_mitm(self, server_socket, client_socket):
        raise NotImplementedError()

    def loop(self):
        raise NotImplementedError()
