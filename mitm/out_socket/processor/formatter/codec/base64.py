class Base64Codec:
    def encode(self, string):
        return string.encode("base64").replace("\n", "")

    def decode(self, string):
        return string.decode("base64")
