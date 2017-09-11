#!/usr/bin/env python

from app.config import PUBLIC_ENDPOINT, DESTINATION_ENDPOINT
from app.servers import SimpleTCPServer
from mitm import set_destination_endpoint
from mitm.extra.samples import StdoutViewMitmRequestHandler

if __name__ == "__main__":
    set_destination_endpoint(DESTINATION_ENDPOINT)
    mitm_server = SimpleTCPServer(PUBLIC_ENDPOINT, StdoutViewMitmRequestHandler)
    mitm_server.start_foreground()

    mitm_server.shutdown()
