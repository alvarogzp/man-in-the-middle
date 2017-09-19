#!/usr/bin/env python


import app
import mitm


if __name__ == "__main__":
    args = app.parsed_args()

    print "Listening on", args.listen
    print "Connecting to", args.destination

    mitm.set_destination_endpoint(args.destination)
    mitm_server = args.server(args.listen, args.mitm_type)
    mitm_server.start_foreground()

    mitm_server.shutdown()
