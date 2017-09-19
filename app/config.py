import mitm
from app.servers import ThreadedTCPServer, SimpleTCPServer

LISTEN_ADDRESS = ""

DEFAULT_PUBLIC_PORT = "8080"
DEFAULT_DESTINATION = "www.google.com:80"

MITM_TYPES = {
    "proxy": mitm.SimpleMitmRequestHandler,
    "spy": mitm.StdoutViewMitmRequestHandler,
    "mitm": mitm.StdoutRedirectMitmRequestHandler,
}
DEFAULT_MITM_TYPE = "spy"

BACKGROUND_SERVER = ThreadedTCPServer
FOREGROUND_SERVER = SimpleTCPServer
