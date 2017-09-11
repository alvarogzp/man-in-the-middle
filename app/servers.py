import SocketServer

from app.thread import Thread
from mitm.config import KILL_THREADS_WHEN_MAIN_ENDS


class SimpleTCPServer(SocketServer.TCPServer):
    def start_foreground(self):
        self.serve_forever()


class ThreadedTCPServer(SocketServer.ThreadingTCPServer):
    daemon_threads = KILL_THREADS_WHEN_MAIN_ENDS

    def start_background(self):
        Thread(target=self.serve_forever).start()

    def start_foreground(self):
        self.serve_forever()
