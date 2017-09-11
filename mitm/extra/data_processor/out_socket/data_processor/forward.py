from mitm.extra.data_processor.out_socket.data_processor import DataProcessor


class ForwardDataProcessor(DataProcessor):
    def __init__(self, socket):
        self.socket = socket

    def process(self, string):
        self.socket.sendall(string)
