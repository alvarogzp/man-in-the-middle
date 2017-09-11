from mitm.config import MESSAGE_ENDPOINT_SEPARATOR


class DecodeAndEndpointUnformatter:
    def __init__(self, codec):
        self.codec = codec

    def unformat(self, string):
        string = self.remove_trailing_newline(string)
        endpoint, encoded_string = self.split_by_separator(string)
        decoded_string = self.codec.decode(encoded_string)
        return (endpoint, decoded_string)

    def remove_trailing_newline(self, string):
        if string[-1] == '\n':
            string = string[:-1]
        return string

    def split_by_separator(self, string):
        return string.split(MESSAGE_ENDPOINT_SEPARATOR, 1)
