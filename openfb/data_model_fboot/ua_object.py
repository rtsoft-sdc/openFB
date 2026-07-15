from opcua import ua
from openfb.data_model_fboot import utils
import logging
import uuid


class UaObject:

    class InvalidFbtState(Exception):
        pass

    def __init__(self, ua_server, ua_folder, fb_name, xml_root, opc_mapping=None, root_path=None, root_list=None):
        self.ua_server = ua_server
        self.ua_folder = ua_folder
        self.fb_name = fb_name
        self.xml_root = xml_root
        self.fb_type = xml_root.get('Name')
        self.opc_ua_type = xml_root.get('OpcUa')
        self.folders = dict()
        self.ua_vars = dict()
        self.mapped_ua_vars = opc_mapping
        self.ua_write_callback_handles = []
        # create object
        fb_node_name = fb_name.split('.')[-1]
        self.obj_idx = '{0}.{1}'.format(ua_folder.get('idx'), fb_node_name)
        self.obj_path_list, self.obj_path = utils.default_object(ua_server, 
                                                                self.obj_idx, 
                                                                ua_folder.get('path'), 
                                                                ua_folder.get('path_list'), 
                                                                fb_node_name)
        try:
            self.populate_interface_items()
        except self.InvalidFbtState:
            logging.error('Invalid function block definition, check {0}.fbt for mistakes'.format(self.fb_name))
        
        self.ua_server.config.create_virtualized_fb(self.fb_name, self.fb_type, self.update_variables)
        # creates required connections
        self.set_up_connections()


    def populate_interface_items(self):
        if self.mapped_ua_vars:
            for var in self.mapped_ua_vars:
                try:
                    var_idx = '{0}.{1}'.format(self.obj_idx, var["Name"])
                    ua_var = self.ua_server.create_typed_variable(self.obj_path,
                                                        var_idx,
                                                        var['Name'], 
                                                        var['Type'], 
                                                        -1)
                    self.ua_vars[var['Name']] = ua_var
                    self.subscribe_to_ua_write(ua_var, var["Name"])
                except KeyError:
                    raise self.InvalidFbtState


    def set_up_connections(self):
        if self.opc_ua_type == 'DEVICE.SENSOR':
            self.ua_server.config.create_connection('{0}.{1}'.format('START', 'COLD'),
                                              '{0}.{1}'.format(self.fb_name, 'INIT'))
            # creates the fb that runs the device in loop
            sleep_fb_name = str(uuid.uuid4())
            self.ua_server.config.create_fb(sleep_fb_name, 'SLEEP')
            self.ua_server.config.create_connection('{0}.{1}'.format(self.fb_name, 'INIT_O'),
                                                '{0}.{1}'.format(sleep_fb_name, 'SLEEP'))
            self.ua_server.config.create_connection('{0}.{1}'.format(sleep_fb_name, 'SLEEP_O'),
                                                '{0}.{1}'.format(self.fb_name, 'READ'))
            self.ua_server.config.create_connection('{0}.{1}'.format(self.fb_name, 'READ_O'),
                                                '{0}.{1}'.format(sleep_fb_name, 'SLEEP'))
        else:
            fb = self.ua_server.config.get_fb(self.fb_name)
            if fb.output_events is not None and fb.output_connections is not None:
                for conn_name in fb.output_connections:
                    conns = fb.output_connections[conn_name]
                    for conn in conns:
                        self.ua_server.config.create_connection('{0}.{1}'.format(conn.destination_fb.fb_name, conn.value_name), 
                                                    '{0}.{1}'.format(self.fb_name, conn_name))

    def subscribe_to_ua_write(self, ua_var, var_name):
        status, handle = self.ua_server.iserver.aspace.add_datachange_callback(
            ua_var.nodeid,
            ua.AttributeIds.Value,
            lambda _handle, data_value: self.update_fb_input(var_name, data_value))

        if status.is_good():
            self.ua_write_callback_handles.append(handle)
        else:
            logging.warning('Could not subscribe to OPC-UA writes for %s.%s: %s',
                            self.fb_name, var_name, status)

    def update_fb_input(self, var_name, data_value):
        value = data_value.Value.Value
        fb = self.ua_server.config.get_fb(self.fb_name)
        fb.set_attr(var_name, new_value=value)
        logging.info('Updated %s.%s from an OPC-UA write', self.fb_name, var_name)

    def update_variables(self):
        # gets the function block
        fb = self.ua_server.find_fb(self.fb_name)
        # iterates over the variables dict
        for var_name, var_ua in self.ua_vars.items():
            # reads the variable value
            v_type, value, _ = fb.read_attr(var_name)
            try:
                # writes the value inside the opc-ua variable
                value = ua.Variant(value, var_ua.get_data_type_as_variant_type())
                var_ua.set_value(value)

            except Exception as error:
                # reports the error
                logging.error('Error writing the value in the opc-ua server.')
                logging.error(error)
                if v_type == 'STRING':
                    # writes the value as a string
                    var_ua.set_value(str(value))
                    # writes the solution
                    logging.error('Error solved writing the variable as string.')
                        
    
    
