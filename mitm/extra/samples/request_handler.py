from mitm.core import BaseWithDestinationMitmRequestHandler
from mitm.extra.data_processor import stdout_server_base64_processor, stdout_client_base64_processor, \
    stdout_server_base64_out_socket, stdout_client_base64_out_socket, stdin_in_socket, ForwardDataProcessor, \
    DataProcessorGroup, DataProcessorOutSocket, UnformatAndRouteByEndpointDataProcessor, \
    base64_decode_and_endpoint_unformatter
from mitm.extra.socket_aggregator import BaseAggregatorMitmRequestHandler, MitmSocketAggregator
from mitm.extra.stream_forwarder import SocketStreamForwarder


class StdoutRedirectMitmRequestHandler(BaseAggregatorMitmRequestHandler):
    """Redirects data to the stdout in base64 format, expecting user to input modified data to be sent"""

    def get_mitm_socket_aggregator(self):
        server_socket = stdout_server_base64_out_socket
        client_socket = stdout_client_base64_out_socket

        recv_socket = stdin_in_socket

        send_socket_unformatter = base64_decode_and_endpoint_unformatter
        send_socket_processor = UnformatAndRouteByEndpointDataProcessor(send_socket_unformatter)
        send_socket = DataProcessorOutSocket(send_socket_processor)

        return MitmSocketAggregator(server_socket, client_socket, recv_socket, send_socket)


class StdoutViewMitmRequestHandler(BaseWithDestinationMitmRequestHandler):
    """Prints data to the stdout in base64 format for user to view what is being sent, but acts as a simple proxy"""

    def setup_mitm(self, server_socket, client_socket):
        server_socket_stdout_processor = stdout_server_base64_processor
        server_socket_forward_processor = ForwardDataProcessor(client_socket)
        server_socket_processor = DataProcessorGroup(server_socket_forward_processor, server_socket_stdout_processor)
        server_mitm_out_socket = DataProcessorOutSocket(server_socket_processor)

        client_socket_stdout_processor = stdout_client_base64_processor
        client_socket_forward_processor = ForwardDataProcessor(server_socket)
        client_socket_processor = DataProcessorGroup(client_socket_forward_processor, client_socket_stdout_processor)
        client_mitm_out_socket = DataProcessorOutSocket(client_socket_processor)

        self.forwarder_from_server = SocketStreamForwarder(server_socket, server_mitm_out_socket).forward()
        self.forwarder_from_client = SocketStreamForwarder(client_socket, client_mitm_out_socket).forward()

    def loop(self):
        self.forwarder_from_server.wait()
        self.forwarder_from_client.wait()


class SimpleMitmRequestHandler(BaseWithDestinationMitmRequestHandler):
    """Simple implementation that simply forwards data to the destination, acting as a mere proxy"""

    def setup_mitm(self, server_socket, client_socket):
        server_socket_processor = ForwardDataProcessor(client_socket)
        server_mitm_out_socket = DataProcessorOutSocket(server_socket_processor)

        client_socket_processor = ForwardDataProcessor(server_socket)
        client_mitm_out_socket = DataProcessorOutSocket(client_socket_processor)

        self.forwarder_from_server = SocketStreamForwarder(server_socket, server_mitm_out_socket).forward()
        self.forwarder_from_client = SocketStreamForwarder(client_socket, client_mitm_out_socket).forward()

    def loop(self):
        self.forwarder_from_server.wait()
        self.forwarder_from_client.wait()
