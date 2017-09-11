from mitm.extra.stream_forwarder import InSocket


class FileInSocket(InSocket):
    def __init__(self, rfile):
        self.rfile = rfile

    def recv(self, bufsize):
        return self.rfile.readline()
