import sys

from mitm.aggregator import MitmSocketAggregator
from mitm.config import ENDPOINT_SERVER, ENDPOINT_CLIENT
from mitm.in_socket import InSocket
from mitm.out_socket import OutSocket
from mitm.out_socket.processor import FormatDataProcessor, UnformatAndRouteByEndpointDataProcessor
from mitm.out_socket.processor.formatter import EncodeAndEndpointFormatter, DecodeAndEndpointUnformatter
from mitm.out_socket.processor.formatter.codec import Base64Codec
from mitm.request_handler.base import BaseMitmRequestHandler


class SimpleMitmRequestHandler(BaseMitmRequestHandler):
    """Simple implementation that simply forwards data to the destination, acting as a mere proxy"""
    pass


class StdoutRedirectMitmRequestHandler(BaseMitmRequestHandler):
    """Redirects data to the stdout in base64 format, expecting user to input modified data to be sent"""

    def get_mitm_socket_aggregator(self, server_socket, client_socket):
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

    def get_mitm_socket_aggregator(self, server_socket, client_socket):
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
