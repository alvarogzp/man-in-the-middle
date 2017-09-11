class UnformatAndRouteByEndpointDataProcessor:
    def __init__(self, unformatter):
        self.unformatter = unformatter

    def set_router(self, router):
        self.router = router

    def process(self, string):
        endpoint, text = self.unformatter.unformat(string)
        self.router.get(endpoint).sendall(text)
