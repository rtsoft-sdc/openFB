import socket
import logging
import sys
from openfb.communication import client_thread


class TcpServer:

    def __init__(self, ip, port, limit_connections, config_m):
        self.config_m = config_m

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = (ip, port)
        logging.info('TCP server starting up on %s port %s' % server_address)

        # Reuse the socket address
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.sock.bind(server_address)
        except socket.error as msg:
            logging.error('bind failed.')
            logging.error(msg)
            sys.exit()

        # Listen for incoming connections
        self.sock.settimeout(1.0)  
        self.active_threads = []
        self.sock.listen(limit_connections)

    def handle_client(self):
        # Wait for a connection
        try:
            connection, client_address = self.sock.accept()
            thread = client_thread.ClientThread(connection, client_address, self.config_m)
            thread.daemon = True  
            thread.start()
            self.active_threads.append(thread)
        except socket.timeout:
            return
        except OSError as e:
            if e.errno == 9: # closed from other thread
                logging.info("Socket has been closed, stopping server.")
                return
            
    def stop_server(self):
        
        try:
            self.sock.close()
        except Exception as e:
            logging.error("Exception while closing socket: {}".format(e))
            
        for thread in self.active_threads:
            if thread.is_alive():
                try:
                    thread.join(timeout=0.5)
                except Exception:
                    logging.error(f"error joining thread {thread.name}")
