import threading
import logging
from xml.etree import ElementTree as ETree

class ClientThread(threading.Thread):

    def __init__(self, connection, client_address, config_m):
        threading.Thread.__init__(self, name='{0}:{1}'.format(client_address[0], client_address[1]))

        self.config_m = config_m
        self.connection = connection
        self.client_address = client_address

    def run(self):
        try:
            logging.info('connection from {0}'.format(self.client_address))

            # Receive the data in small chunks and retransmit it
            while True:
                data = self.connection.recv(2048)
                logging.info('received {0}'.format(data))

                if data:
                    response = self.parse_request(data)
                    logging.info('sending response {0}'.format(response))
                    self.connection.sendall(response)

                else:
                    logging.info('no more data from {0}'.format(self.client_address))
                    break

        finally:
            # Clean up the connection
            self.connection.close()

        
    def remove_service_symbols(self, data):
        if "&apos;" in data:
            data = data.replace('&apos;', '')
            logging.error(f"After replacement: {data}")
        elif "&quote;" in data:
            data = data.replace('&quote;', '')
            logging.error(f"After replacement: {data}")
        return data
    
    def remove_name_sys(self, data_str):
        xml_data = ETree.fromstring(data_str)
        current_name = xml_data.find('FB')
        destination = xml_data.find('Connection')
        watcher = xml_data.find('Watch')
        if current_name is None and destination is None and watcher is None:
            return data_str
        elif watcher is not None:
            port_watch = watcher.get('Source')
            new_port_name = '.'.join(port_watch.split('.')[-1])
            xml_data.find('Watch').set('Source', new_port_name)
        elif destination is not None:
            destination = destination.get('Destination')
            destination = destination.split('.')[1:]
            logging.error(destination, data_str)
            destination = '.'.join(destination)
            logging.error(destination)

            xml_data.find('Connection').set('Destination', destination)
        else:
            current_name = current_name.get('Name')
            current_name = current_name.split('.')[-1]
            xml_data.find('FB').set("Name", current_name)
        data_str = ETree.tostring(xml_data, encoding='unicode')

        return data_str

    def parse_request(self, data):
        
        config_id_size = int(data[1:3].hex(), 16)
        if config_id_size == 0:
            data_str = data[6:].decode('utf-8')
            data_str = self.remove_service_symbols(data_str)
            response = self.config_m.parse_general(data_str)
        else:
            config_id = data[3: config_id_size + 3].decode('utf-8')
            data_str = data[config_id_size + 3 + 3:].decode('utf-8')
            data_str = self.remove_service_symbols(data_str)
            response = self.config_m.parse_configuration(data_str, config_id)

        return response
