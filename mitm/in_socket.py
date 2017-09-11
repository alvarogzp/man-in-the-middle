class InSocket:
    def __init__(self, rfile):
        self.rfile = rfile

    def recv(self, bufsize):
        return self.rfile.readline()
