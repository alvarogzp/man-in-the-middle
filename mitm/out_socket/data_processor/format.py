class FormatDataProcessor:
    def __init__(self, formatter, action):
        self.formatter = formatter
        self.action = action

    def process(self, string):
        formatted_data = self.formatter.format(string)
        self.action(formatted_data)
