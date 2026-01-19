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

    address = 'localhost'
    port_diac = 61499
    port_opc = 4840
    log_level = log_levels['ERROR']
    n_samples = 10
    secs_sample = 20
    monitor = [n_samples, secs_sample]
    agent = False

    fboot_path = os.path.join(resource_dir, 'data_model.fboot')
    unix_socket = "logger.sock"


    # build parser for application command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', metavar='address', nargs=1,
                        help="ip address to bind at (default: localhost)")
    parser.add_argument('-p', metavar='port_diac', nargs=1, type=int,
                        help="port for the 4diac communication (default: 61499)")
    parser.add_argument('-u', metavar='port_opc', nargs=1, type=int,
                        help="port for the opc-ua communication (default: 4840)")
    parser.add_argument('-l', metavar='log_level', nargs=1,
                        help="logging level at the file resources/error_list.log, e.g. INFO, WARN or ERROR (default: ERROR)")
    parser.add_argument("-s", metavar="logging_socket", nargs=1, type=str,
                        help="Unix socket path for external logging collectors")
    parser.add_argument('-g', action='store_true',
                        help="sets on the self-organizing agent")
    parser.add_argument('-m', metavar='monitor', nargs='*', help="activates the behavioral anomaly detection feature. If no paramters are specified, the default values are 10 samples for initial training, each sample with 20 seconds (approximately 3m20s). As an example, you can specify paramters the following way (-m 5 10) meaning 10 samples for training with 10 seconds each sample.")
    parser.add_argument('-f', metavar='fboot_file', nargs=1, type=str, help="path to the .fboot file to run")
    args = parser.parse_args()

    if args.a != None:
        address = args.a[0]
    if args.p != None:
        port_diac = args.p[0]
    if args.u != None:
        port_opc = args.u[0]
    if args.l != None:
        log_level = log_levels[args.l[0]]
    agent = args.g
    if args.m != None:
        if len(args.m) == 2:
            monitor = [int(args.m[0]), int(args.m[1])]
        elif len(args.m) == 1 or len(args.m) > 2:
            print("For the monitoring functionality, please specify 2 arguments or none!")
            exit(2)
    else:
        monitor = None
    if args.f != None:
        fboot_path = args.f[0]
    if args.s != None:
        unix_socket = args.s[0]
    ##############################################################
    # remove all files in monitoring folder
    monitoring_path = os.path.join(resource_dir, 'monitoring', '')
    if os.path.exists(monitoring_path):
        files = glob.glob("{0}*".format(monitoring_path))
        for f in files:
            os.remove(f)
    ##############################################################

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
    m = manager.Manager(monitor=monitor)
    # sets the ua integration option
    m.build_ua_manager_fboot(address, port_opc, fboot_path)

    # creates the tcp server to communicate with the 4diac
    hand = tcp_server.TcpServer(address, port_diac, 10, m)

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