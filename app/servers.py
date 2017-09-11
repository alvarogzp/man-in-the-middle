import SocketServer

from mitm.config import KILL_THREADS_WHEN_MAIN_ENDS
from mitm.thread import Thread


class SimpleTCPServer(SocketServer.TCPServer):
    def start_foreground(self):
        self.serve_forever()


class ThreadedTCPServer(SocketServer.ThreadingTCPServer):
    daemon_threads = KILL_THREADS_WHEN_MAIN_ENDS

    def start_background(self):
        Thread(target=self.serve_forever).start()

    def start_foreground(self):
        self.serve_forever()
