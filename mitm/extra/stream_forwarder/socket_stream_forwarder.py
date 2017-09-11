from mitm.extra.stream_forwarder.config import RECV_BUFFER
from mitm.extra.stream_forwarder.in_socket import InSocket
from mitm.extra.stream_forwarder.out_socket import OutSocket
from mitm.extra.stream_forwarder.thread import Thread


class SocketStreamForwarder:
    def __init__(self, in_socket, out_socket):
        """
        :type in_socket: InSocket
        :type out_socket: OutSocket
        """
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
