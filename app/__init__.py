#!/usr/bin/env python

from app.config import PUBLIC_ENDPOINT
from app.servers import SimpleTCPServer
from mitm.request_handler.samples import StdoutRedirectMitmRequestHandler


if __name__ == "__main__":
    mitm_server = SimpleTCPServer(PUBLIC_ENDPOINT, StdoutRedirectMitmRequestHandler)
    mitm_server.start_foreground()

    mitm_server.shutdown()