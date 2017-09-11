from mitm.extra.data_processor.out_socket.data_processor import DataProcessor
from mitm.extra.stream_forwarder import OutSocket


class DataProcessorOutSocket(OutSocket):
    def __init__(self, processor):
        """
        :type processor: DataProcessor
        """
        self.processor = processor

    def sendall(self, string):
        self.processor.process(string)
