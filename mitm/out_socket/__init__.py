class OutSocket:
    def __init__(self, processor):
        self.processor = processor

    def sendall(self, string):
        self.processor.process(string)
