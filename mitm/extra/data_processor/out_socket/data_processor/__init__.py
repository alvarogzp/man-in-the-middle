class DataProcessor:
    def process(self, string):
        raise NotImplementedError()


class RouterDataProcessor(DataProcessor):
    def set_router(self, router):
        raise NotImplementedError()
