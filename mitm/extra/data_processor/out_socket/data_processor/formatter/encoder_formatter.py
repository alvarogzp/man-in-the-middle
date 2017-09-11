from mitm.extra.data_processor.config import MESSAGE_ENDPOINT_SEPARATOR


class EncodeAndEndpointFormatter:
    def __init__(self, endpoint, codec):
        self.endpoint = endpoint
        self.codec = codec

    def format(self, string):
        return self.endpoint + MESSAGE_ENDPOINT_SEPARATOR + self.codec.encode(string) + '\n'
