#!/usr/bin/env python

import SocketServer
import socket
import sys
import threading

PUBLIC_ENDPOINT = ('', 4141)

DESTINATION_ENDPOINT = ('127.0.0.1', 4747)
RECV_BUFFER = 4096
KILL_THREADS_WHEN_MAIN_ENDS = True

ENDPOINT_SERVER = 'S'
ENDPOINT_CLIENT = 'C'
MESSAGE_ENDPOINT_SEPARATOR = ':'


class Thread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self.daemon = KILL_THREADS_WHEN_MAIN_ENDS


class ThreadedTCPServer(SocketServer.ThreadingTCPServer):
    daemon_threads = KILL_THREADS_WHEN_MAIN_ENDS

    def start_background(self):
        Thread(target=self.serve_forever).start()

    def start_foreground(self):
        self.serve_forever()


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


class SocketStreamForwarder:
    def __init__(self, in_socket, out_socket):
        self.in_socket = in_socket
        self.out_socket = out_socket
        self.thread = Thread(target=self.forward_loop)

    def forward(self):
        self.thread.start()
        return self

    def forward_loop(self):
        try:
            read = self._read()
            while read:
                self._write(read)
                read = self._read()
        except:
            pass

    def _read(self):
        return self.in_socket.recv(RECV_BUFFER)

    def _write(self, read):
        self.out_socket.sendall(read)

    def wait(self):
        self.thread.join()


class MitmSocketAggregator:
    def __init__(self, server_socket, client_socket, recv_socket, send_socket):
        self.server_out_socket = server_socket
        self.client_out_socket = client_socket
        self.recv_socket = recv_socket
        self._send_socket = send_socket

    def send_socket(self, server_socket, client_socket):
        self._send_socket.processor.set_router(EndpointRouter(server_socket, client_socket))
        return self._send_socket


class InSocket:
    def __init__(self, rfile):
        self.rfile = rfile

    def recv(self, bufsize):
        return self.rfile.readline()


class OutSocket:
    def __init__(self, processor):
        self.processor = processor

    def sendall(self, string):
        self.processor.process(string)


class FormatDataProcessor:
    def __init__(self, formatter, action):
        self.formatter = formatter
        self.action = action

    def process(self, string):
        formatted_data = self.formatter.format(string)
        self.action(formatted_data)


class EncodeAndEndpointFormatter:
    def __init__(self, endpoint, codec):
        self.endpoint = endpoint
        self.codec = codec

    def format(self, string):
        return self.endpoint + MESSAGE_ENDPOINT_SEPARATOR + self.codec.encode(string) + '\n'


class DecodeAndEndpointUnformatter:
    def __init__(self, codec):
        self.codec = codec

    def unformat(self, string):
        string = self.remove_trailing_newline(string)
        endpoint, encoded_string = self.split_by_separator(string)
        decoded_string = self.codec.decode(encoded_string)
        return (endpoint, decoded_string)

    def remove_trailing_newline(self, string):
        if string[-1] == '\n':
            string = string[:-1]
        return string

    def split_by_separator(self, string):
        return string.split(MESSAGE_ENDPOINT_SEPARATOR, 1)


class Base64Codec:
    def encode(self, string):
        return string.encode("base64").replace("\n", "")

    def decode(self, string):
        return string.decode("base64")


class UnformatAndRouteByEndpointDataProcessor:
    def __init__(self, unformatter):
        self.unformatter = unformatter

    def set_router(self, router):
        self.router = router

    def process(self, string):
        endpoint, text = self.unformatter.unformat(string)
        self.router.get(endpoint).sendall(text)


class EndpointRouter:
    def __init__(self, server_socket, client_socket):
        self.server_socket = server_socket
        self.client_socket = client_socket

    def get(self, endpoint):
        if endpoint == ENDPOINT_SERVER:
            return self.client_socket
        elif endpoint == ENDPOINT_CLIENT:
            return self.server_socket


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


if __name__ == "__main__":
    mitm_server = SocketServer.TCPServer(PUBLIC_ENDPOINT, StdoutRedirectMitmRequestHandler)
    mitm_server.serve_forever()

    mitm_server.shutdown()
