#!/usr/bin/env python


from app.args import parsed_args
from mitm import set_destination_endpoint


if __name__ == "__main__":
    args = parsed_args()

    print "Listening on", args.listen
    print "Connecting to", args.destination

    set_destination_endpoint(args.destination)
    mitm_server = args.server(args.listen, args.mitm_type)
    mitm_server.start_foreground()

    mitm_server.shutdown()
