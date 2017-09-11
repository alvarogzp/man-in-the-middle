import sys

from mitm.aggregator import MitmSocketAggregator
from mitm.config import ENDPOINT_SERVER, ENDPOINT_CLIENT
from mitm.in_socket import InSocket
from mitm.out_socket import OutSocket
from mitm.out_socket.data_processor.format import FormatDataProcessor
from mitm.out_socket.data_processor.formatter.codec.base64 import Base64Codec
from mitm.out_socket.data_processor.formatter.decoder_unformatter import DecodeAndEndpointUnformatter
from mitm.out_socket.data_processor.formatter.encoder_formatter import EncodeAndEndpointFormatter
from mitm.out_socket.data_processor.forward import ForwardDataProcessor
from mitm.out_socket.data_processor.group import DataProcessorGroup
from mitm.out_socket.data_processor.unformat_and_route import UnformatAndRouteByEndpointDataProcessor
from mitm.request_handler.aggregator import BaseAggregatorMitmRequestHandler
from mitm.request_handler.base import BaseMitmRequestHandler
from mitm.socket_stream_forwarder import SocketStreamForwarder


class StdoutRedirectMitmRequestHandler(BaseAggregatorMitmRequestHandler):
    """Redirects data to the stdout in base64 format, expecting user to input modified data to be sent"""

    def get_mitm_socket_aggregator(self):
        server_socket_codec = Base64Codec()
        server_socket_formatter = EncodeAndEndpointFormatter(ENDPOINT_SERVER, server_socket_codec)
        server_socket_action = sys.stdout.write
        server_socket_processor = FormatDataProcessor(server_socket_formatter, server_socket_action)
        server_socket = OutSocket(server_socket_processor)

        client_socket_codec = Base64Codec()
        client_socket_formatter = EncodeAndEndpointFormatter(ENDPOINT_CLIENT, client_socket_codec)
        client_socket_action = sys.stdout.write
        client_socket_processor = FormatDataProcessor(client_socket_formatter, client_socket_action)
        client_socket = OutSocket(client_socket_processor)

        recv_socket = InSocket(sys.stdin)

        send_socket_codec = Base64Codec()
        send_socket_unformatter = DecodeAndEndpointUnformatter(send_socket_codec)
        send_socket_processor = UnformatAndRouteByEndpointDataProcessor(send_socket_unformatter)
        send_socket = OutSocket(send_socket_processor)

        return MitmSocketAggregator(server_socket, client_socket, recv_socket, send_socket)


class StdoutViewMitmRequestHandler(BaseMitmRequestHandler):
    """Prints data to the stdout in base64 format for user to view what is being sent, but acts as a simple proxy"""

    def setup_mitm(self, server_socket, client_socket):
        server_socket_stdout_codec = Base64Codec()
        server_socket_stdout_formatter = EncodeAndEndpointFormatter(ENDPOINT_SERVER, server_socket_stdout_codec)
        server_socket_stdout_action = sys.stdout.write
        server_socket_stdout_processor = FormatDataProcessor(server_socket_stdout_formatter, server_socket_stdout_action)
        server_socket_forward_processor = ForwardDataProcessor(client_socket)
        server_socket_processor = DataProcessorGroup(server_socket_forward_processor, server_socket_stdout_processor)
        server_mitm_out_socket = OutSocket(server_socket_processor)

        client_socket_stdout_codec = Base64Codec()
        client_socket_stdout_formatter = EncodeAndEndpointFormatter(ENDPOINT_CLIENT, client_socket_stdout_codec)
        client_socket_stdout_action = sys.stdout.write
        client_socket_stdout_processor = FormatDataProcessor(client_socket_stdout_formatter, client_socket_stdout_action)
        client_socket_forward_processor = ForwardDataProcessor(server_socket)
        client_socket_processor = DataProcessorGroup(client_socket_forward_processor, client_socket_stdout_processor)
        client_mitm_out_socket = OutSocket(client_socket_processor)

        self.forwarder_from_server = SocketStreamForwarder(server_socket, server_mitm_out_socket).forward()
        self.forwarder_from_client = SocketStreamForwarder(client_socket, client_mitm_out_socket).forward()

    def loop(self):
        self.forwarder_from_server.wait()
        self.forwarder_from_client.wait()


class SimpleMitmRequestHandler(BaseMitmRequestHandler):
    """Simple implementation that simply forwards data to the destination, acting as a mere proxy"""

    def setup_mitm(self, server_socket, client_socket):
        server_socket_processor = ForwardDataProcessor(client_socket)
        server_mitm_out_socket = OutSocket(server_socket_processor)

        client_socket_processor = ForwardDataProcessor(server_socket)
        client_mitm_out_socket = OutSocket(client_socket_processor)

        self.forwarder_from_server = SocketStreamForwarder(server_socket, server_mitm_out_socket).forward()
        self.forwarder_from_client = SocketStreamForwarder(client_socket, client_mitm_out_socket).forward()

    def loop(self):
        self.forwarder_from_server.wait()
        self.forwarder_from_client.wait()
