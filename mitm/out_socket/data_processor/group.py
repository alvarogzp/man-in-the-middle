from mitm.out_socket.data_processor import DataProcessor


class DataProcessorGroup(DataProcessor):
    def __init__(self, *processors):
        self.processors = processors

    def process(self, string):
        for processor in self.processors:
            processor.process(string)
