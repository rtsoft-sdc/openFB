from openfb.opc_ua import client
from openfb.opc_ua import base
from opcua import Server
import threading
import logging
from opcua.ua.uaerrors import BadNoMatch
from opcua import ua

class UaPeer(Server, base.UaBase):

    def __init__(self, address, server_name='openfb'):
        Server.__init__(self)
        base.UaBase.__init__(self)

        logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s][%(threadName)-15s] %(message)s')

        self.set_endpoint(address)
        self.set_server_name(server_name)

        # setup our own namespace, not really necessary but should as spec
        self.uri = "urn:openfb:opcua-server"
        self.register_namespace(self.uri)

        self.root = self.get_root_node()

        self.lock = threading.Lock()
        self.client_dictionary = dict()

        self.start()

    def add_client(self, client_address):
        self.lock.acquire()
        if client_address not in self.client_dictionary:
            c = client.UaClient(client_address)
            self.client_dictionary[client_address] = c
        self.lock.release()

    def remove_client(self, client_address):
        self.lock.acquire()
        c = self.client_dictionary[client_address]
        c.disconnect()
        self.client_dictionary.pop(client_address)
        self.lock.release()

    def remove_all_clients(self):
        self.lock.acquire()
        for address, c in self.client_dictionary.items():
            c.disconnect()
        self.client_dictionary.clear()
        self.lock.release()

    def client_read(self, client_address, path):
        self.lock.acquire()
        val = self.client_dictionary[client_address].read(path)
        self.lock.release()
        return val

    def client_write(self, client_address, path, val):
        self.lock.acquire()
        self.client_dictionary[client_address].write(path, val)
        self.lock.release()

    def client_call_method(self, client_address, path, *args):
        self.lock.acquire()
        result = self.client_dictionary[client_address].call_method(path.copy(), *args)
        self.lock.release()
        return result
    
    def default_value(self, var_type, value_rank):
        if value_rank == 0 or value_rank == -1:  
            return {
                ua.VariantType.Boolean: False,
                ua.VariantType.Int16: 0,
                ua.VariantType.Int32: 0,
                ua.VariantType.Int64: 0,
                ua.VariantType.UInt16: 0,
                ua.VariantType.UInt32: 0,
                ua.VariantType.UInt64: 0,
                ua.VariantType.Float: 0.0,
                ua.VariantType.Double: 0.0,
                ua.VariantType.String: "",
            }.get(var_type, None)
        else:
            return []

    def create_typed_variable(self, path, index, var_name, var_type,
                            value_rank, dimensions=0, writable=True):

        my_obj = self.root.get_child(path)

        try:
            return my_obj.get_child(var_name)

        except BadNoMatch:
            my_var = my_obj.add_variable(
                index,
                var_name,
                self.default_value(var_type, value_rank),
                var_type
                )

            my_var.set_value_rank(value_rank)

            if value_rank >= 1:
                my_var.set_array_dimensions([dimensions])

            if writable:
                my_var.set_writable(True)
                sub = self.create_subscription(0, self.observer)
                sub.subscribe_data_change(my_var)

            return my_var
        