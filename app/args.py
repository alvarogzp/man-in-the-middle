import argparse

from app.config import DEFAULT_PUBLIC_PORT, DEFAULT_DESTINATION, MITM_TYPES, DEFAULT_MITM_TYPE, FOREGROUND_SERVER, \
    BACKGROUND_SERVER, LISTEN_ADDRESS


def parsed_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--listen", default=DEFAULT_PUBLIC_PORT, type=_listen)
    parser.add_argument("-d", "--destination", default=DEFAULT_DESTINATION, type=_destination)
    parser.add_argument("-t", "--mitm-type", default=DEFAULT_MITM_TYPE, type=_mitm_type)
    parser.add_argument("-b", "--background", default=FOREGROUND_SERVER, action="store_const", const=BACKGROUND_SERVER, dest="server")
    return parser.parse_args()


def _listen(port):
    return LISTEN_ADDRESS, int(port)


def _destination(destination_string):
    address, port = destination_string.split(":")
    return address, int(port)


def _mitm_type(type_key):
    return MITM_TYPES[type_key]
