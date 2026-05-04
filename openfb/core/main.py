import logging
import logging.handlers
import os
import sys
import argparse
import glob
from importlib.resources import files

from openfb.communication import tcp_server
from openfb.core import manager

# If openFB used as a package set env var OPENFB_LOCAL_DIR with to resources folder 
if os.environ.get("OPENFB_LOCAL_DIR"):
    resource_dir = os.environ.get("OPENFB_LOCAL_DIR")
else:
    resource_dir = str(files("openfb.resources"))


def main():
    log_levels = {'ERROR': logging.ERROR,
                  'WARN': logging.WARN,
                  'INFO': logging.INFO,
                  'DEBUG': logging.DEBUG}

    address = '0.0.0.0'
    port_diac = 61499
    port_opc = 4840
    log_level = log_levels['INFO']

    fboot_path = os.path.join(resource_dir, 'data_model.fboot')
    unix_socket = "logger.sock"


    # build parser for application command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', metavar='address', nargs=1,
                        help="ip address to bind at (default: 0.0.0.0)")
    parser.add_argument('-p', metavar='port_diac', nargs=1, type=int,
                        help="port for the 4diac communication (default: 61499)")
    parser.add_argument('-u', metavar='port_opc', nargs=1, type=int,
                        help="port for the opc-ua communication (default: 4840)")
    parser.add_argument('-l', metavar='log_level', nargs=1,
                        help="logging level at the file resources/error_list.log, e.g. INFO, WARN or ERROR (default: ERROR)")
    parser.add_argument("-s", metavar="logging_socket", nargs=1, type=str,
                        help="Unix socket path for external logging collectors")
    parser.add_argument('-f', metavar='fboot_file', nargs=1, type=str, help="path to the .fboot file to run")
    args = parser.parse_args()

    if args.a is not None:
        address = args.a[0]
    if args.p is not None:
        port_diac = args.p[0]
    if args.u is not None:
        port_opc = args.u[0]
    if args.l is not None:
        log_level = log_levels[args.l[0]]
    if args.f is not None:
        fboot_path = args.f[0]
    if args.s is not None:
        unix_socket = args.s[0]


    # Configure the logging output
    log_path = os.path.join(resource_dir, 'error_list.log')
    if os.path.isfile(log_path):
        os.remove(log_path)

    handlers = [logging.StreamHandler(sys.stdout), logging.FileHandler(log_path)]
    if os.path.exists(unix_socket):
        unix_handler = logging.handlers.SysLogHandler(
            address=unix_socket, facility="local1"
        )
        handlers.append(unix_handler)

    logging.basicConfig(
        level=log_level,
        format="[%(asctime)s][%(levelname)s][%(threadName)s] %(message)s",
        handlers=handlers,
    )
    if log_level != logging.DEBUG:
        logging.getLogger("opcua").setLevel(logging.CRITICAL)

    # creates the 4diac manager
    m = manager.Manager()
    # sets the ua integration option
    m.build_ua_manager_fboot(address, port_opc, fboot_path)
    print("[INFO]\tOPCUA server is running on {0}:{1}".format(address, port_opc))

    # creates the tcp server to communicate with the 4diac
    hand = tcp_server.TcpServer(address, port_diac, 10, m)
    print("[INFO]\tOpenfb is up and running on {0}:{1}".format(address, port_diac))

    try:
        # handles every client
        while True:
            hand.handle_client()
    except KeyboardInterrupt:
        logging.info('interrupted server')
        m.manager_ua_fboot.stop_ua()
        hand.stop_server()

        sys.exit(0)

if __name__ == "__main__":
    main()