import sys

from mitm.extra.data_processor.config import MESSAGE_ENDPOINT_SERVER, MESSAGE_ENDPOINT_CLIENT, \
    MESSAGE_ENDPOINT_SEPARATOR
from mitm.extra.data_processor.in_socket.file import FileInSocket
from mitm.extra.data_processor.out_socket import DataProcessorOutSocket
from mitm.extra.data_processor.out_socket.data_processor import RouterDataProcessor
from mitm.extra.data_processor.out_socket.data_processor.format import FormatAndDoDataProcessor
from mitm.extra.data_processor.out_socket.data_processor.formatter.codec.base64 import Base64Codec
from mitm.extra.data_processor.out_socket.data_processor.formatter.decoder_unformatter import \
    DecodeAndEndpointUnformatter
from mitm.extra.data_processor.out_socket.data_processor.formatter.encoder_formatter import EncodeAndEndpointFormatter
from mitm.extra.data_processor.out_socket.data_processor.forward import ForwardDataProcessor
from mitm.extra.data_processor.out_socket.data_processor.group import DataProcessorGroup
from mitm.extra.data_processor.out_socket.data_processor.router.endpoint import EndpointRouter
from mitm.extra.data_processor.out_socket.data_processor.unformat_and_route import \
    UnformatAndRouteByEndpointDataProcessor


base64_codec = Base64Codec()

server_base64_formatter = EncodeAndEndpointFormatter(MESSAGE_ENDPOINT_SERVER, base64_codec)
client_base64_formatter = EncodeAndEndpointFormatter(MESSAGE_ENDPOINT_CLIENT, base64_codec)


stdout_write = sys.stdout.write

stdout_server_base64_processor = FormatAndDoDataProcessor(server_base64_formatter, stdout_write)
stdout_client_base64_processor = FormatAndDoDataProcessor(client_base64_formatter, stdout_write)


stdout_server_base64_out_socket = DataProcessorOutSocket(stdout_server_base64_processor)
stdout_client_base64_out_socket = DataProcessorOutSocket(stdout_client_base64_processor)


stdin_in_socket = FileInSocket(sys.stdin)


base64_decode_and_endpoint_unformatter = DecodeAndEndpointUnformatter(base64_codec)
