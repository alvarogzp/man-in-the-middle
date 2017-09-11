import SocketServer
import socket

from mitm.config import DESTINATION_ENDPOINT
from mitm.socket_stream_forwarder import SocketStreamForwarder


class BaseMitmRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        server_socket = self.connect_to_destination()
        aggregator = self.get_mitm_socket_aggregator(server_socket, self.request)
        self.forward(server_socket, self.request, aggregator)

    def connect_to_destination(self):
        return socket.create_connection(DESTINATION_ENDPOINT)

    def forward(self, server_socket, client_socket, aggregator):
        forwarder_from_server = SocketStreamForwarder(server_socket, aggregator.server_out_socket).forward()
        forwarder_from_client = SocketStreamForwarder(client_socket, aggregator.client_out_socket).forward()
        forwarder_from_aggregator = SocketStreamForwarder(aggregator.recv_socket,
                                                          aggregator.send_socket(server_socket, client_socket)
                                                          ).forward()
        forwarder_from_server.wait()
        forwarder_from_client.wait()
        forwarder_from_aggregator.wait()

    def get_mitm_socket_aggregator(self, server_socket, client_socket):
        raise NotImplementedError()
