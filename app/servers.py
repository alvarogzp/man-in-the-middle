import SocketServer

import mitm


class SimpleTCPServer(SocketServer.TCPServer):
    def start_foreground(self):
        self.serve_forever()


class ThreadedTCPServer(SocketServer.ThreadingTCPServer):
    daemon_threads = mitm.KILL_THREADS_WHEN_MAIN_ENDS

    def start_background(self):
        mitm.Thread(target=self.serve_forever).start()

    def start_foreground(self):
        self.serve_forever()
