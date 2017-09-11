from mitm import BaseMitmRequestHandler
from mitm.request_handler.fixed_destination import BaseFixedDestinationMitmRequestHandler
from mitm.socket_stream_forwarder import SocketStreamForwarder


class BaseAggregatorMitmRequestHandler(BaseFixedDestinationMitmRequestHandler):
    def setup_mitm(self, server_socket, client_socket):
        aggregator = self.get_mitm_socket_aggregator()

        self.forwarder_from_server = SocketStreamForwarder(server_socket, aggregator.server_out_socket).forward()
        self.forwarder_from_client = SocketStreamForwarder(client_socket, aggregator.client_out_socket).forward()
        self.forwarder_from_aggregator = SocketStreamForwarder(aggregator.recv_socket,
                                                               aggregator.send_socket(server_socket, client_socket)
                                                               ).forward()

    def loop(self):
        self.forwarder_from_server.wait()
        self.forwarder_from_client.wait()
        self.forwarder_from_aggregator.wait()

    def get_mitm_socket_aggregator(self):
        raise NotImplementedError()
