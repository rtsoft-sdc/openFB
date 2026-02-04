from openfb.opc_ua import peer
from xml.etree import ElementTree as ETree
from openfb.data_model_fboot import ua_object, monitor, utils, ua_method
import logging
import os
import sys
from openfb.core.configuration import Configuration

class UaManagerFboot(peer.UaPeer):

    class InvalidFbootState(Exception):
       pass

    def __init__(self, address, port, fboot_path, conf_dict=dict(), main_manager=None):
        self.address = address
        self.port = port
        self.fboot_path = fboot_path
        self.base_name = 'OPENFB OPC-UA'
        self.endpoint = 'opc.tcp://{0}:{1}'.format(address, port)

        peer.UaPeer.__init__(self, address=self.endpoint)

        self.folders = dict()
        self.ua_objects = dict()
        self.method_names = []
        self.method_inputs = None
        self.method_outputs = None
        self.opcua_method_name = None
        self.resources_running = set()
        self.opc_mapped_vars = {}

        self.config_dictionary = conf_dict
        self.main_manager = main_manager

    def __call__(self, config):
        # base idx for the opc-ua nodeId
        self.base_idx = 'ns=2;s={0}'.format(self.base_name)
        # creates the root object 'SmartObject'
        self.create_object(2, self.base_name, path=self.generate_path([(0, 'Objects')]))
        # creates the path to that object
        self.ROOT_LIST = [(0, 'Objects'), (2, self.base_name)]
        self.ROOT_PATH = self.generate_path(self.ROOT_LIST)
        # configuration (connection to 4diac code)
        self.config = config
        # create the monitor hardware variables
        self.monitor_hardware = monitor.MonitorSystem(self)
        self.monitor_hardware.start()
        # create function blocks folder
        folder_idx, folder_path, folder_list = utils.default_folder(self, self.base_idx, self.ROOT_PATH, self.ROOT_LIST, 'FunctionBlocks')
        self.folders['FunctionBlocks'] = {
            'idx': folder_idx,
            'path': folder_path,
            'path_list': folder_list
        }
        # create services folder 
        folder_idx, folder_path, folder_list = utils.default_folder(self, self.base_idx, self.ROOT_PATH, self.ROOT_LIST, 'OPC-UA_Methods')
        self.folders['OPC-UA_Methods'] = {
            'idx': folder_idx,
            'path': folder_path,
            'path_list': folder_list
        }

    def set_config_dictionary(self, conf_dict):
        self.config_dictionary = conf_dict

    def find_fb(self, fb_name):
        for conf in self.config_dictionary.values():
            for name, fb in conf.fb_dictionary.items():
                if name == fb_name:
                    return fb

    def save_fboot(self, requests):
        existing_resources = set()

        if os.path.exists(self.fboot_path):
            with open(self.fboot_path, 'r') as f:
                for line in f:
                    if ';' in line:
                        name = line.split(';', 1)[0]
                        if name:
                            existing_resources.add(name)

        mode = 'a' if existing_resources else 'w'
        file = open(self.fboot_path, mode)

        start_fb = None
        is_watch = False
        for request in requests:
            element = ETree.fromstring(request)
            for child in element:
                if child.tag == 'Watch':
                    is_watch = True
                    break

            if is_watch:
                is_watch = False
                continue

            if start_fb is None:
                for child in element:
                    start_fb = child.attrib['Name']
                if start_fb in existing_resources:
                    break
                file.write(';')
            else:
                file.write(f'{start_fb};')

            file.write(request)
            file.write('\n')

        file.close()
    
    def from_fboot(self):
        # Check if data model file exists and is not empty
        try:
            file = open(self.fboot_path, 'r')
        except FileNotFoundError:
            logging.error('Could not find fboot definition file. Awaiting deployment.')
        else:
            if os.stat(self.fboot_path).st_size == 0:
                logging.warning('Fboot definition file is empty. Awaiting deployment')
            else:
                try:
                    # Parse data model file
                    self.parse_fboot(file)
                except self.InvalidFbootState:
                    logging.error('Fboot definition file is in an invalid state. Awaiting deployment')
                else:
                    if len(self.method_names) != 0:
                        self.method = ua_method.UaMethod(self, self.folders.get('OPC-UA_Methods'), self.method_root)
                    for conf in self.config_dictionary.values():
                        conf.start_work()

    def parse_fboot(self, file):
        lines = file.readlines()
        file.close()
        # create function blocks - folders, objects and variables
        self.generate_function_blocks(lines)
        # create connections - write and create between variables and events
        self.generate_connections(lines)        

    import xml.etree.ElementTree as ET

    def validate_xml_with_details(self, xml_part):
        try:
            ETree.fromstring(xml_part)
            return True
        except ETree.ParseError as e:
            msg = str(e)
            logging.error({"ERROR in .fboot file": msg,"snippet": xml_part})
            return False

    def generate_function_blocks(self, lines):
        for line in lines:
            # Remove string/wstring entities
            line = line.replace("&quot;", "").replace("&apos;", "")
            # Remove start fb from line
            chunks = line.split(';')
            resource_name = chunks[0]
            
            if len(chunks) != 2:
                raise self.InvalidFbootState
            
            if self.validate_xml_with_details(chunks[1]) != True:
                raise self.InvalidFbootState
            
            if chunks[0] != "":
                self.resources_running.add(chunks[0])
                self.config = self.config_dictionary.get(chunks[0])
                if self.config is None:
                    self.config_dictionary[chunks[0]] = Configuration(chunks[0], "EMB_RES", monitor=self.main_manager.monitor)
                    self.config = self.config_dictionary.get(chunks[0])
                    self.main_manager.set_config(chunks[0], self.config)

            xml_element = ETree.fromstring(chunks[1])
            try:
                if xml_element.get('Action') == 'CREATE':
                    for child in xml_element:
                        #fixme: new types like iec61499::system::EMB_RES
                        try:
                            open_fb_type = (child.get('Type')).split('::')[-1]
                        except:
                            continue
                        
                        if child.tag == 'FB' and open_fb_type != 'EMB_RES':
                            root_path = utils.get_fb_files_path(open_fb_type)
                            if root_path == None:
                                raise self.InvalidFbootState
                            # Check fbt file
                            fb_file = open(os.path.join(root_path, '{0}.fbt'.format(open_fb_type)), 'r')
                            fb_name = child.get('Name')
                            opc_mapping = child.find('OpcMapping')
                            if opc_mapping is not None:
                                for var in opc_mapping.findall('Var'):
                                    if fb_name not in self.opc_mapped_vars:
                                        self.opc_mapped_vars[fb_name] = []
                                    self.opc_mapped_vars[fb_name].append({
                                        'Name': var.attrib['Name'],
                                        'Direction': var.attrib['Direction'],
                                        'Type': var.attrib['Type']
                                    })

                            self.parse_fbt(fb_name, fb_file)
                                   
            except KeyError:
                raise self.InvalidFbootState

    def generate_connections(self, lines):
        for line in lines:
            # Remove string/wstring entities
            line = line.replace("&quot;", "").replace("&apos;", "")
            # Remove start fb from line
            chunks = line.split(';')
            if len(chunks) != 2:
                raise self.InvalidFbootState
            if self.validate_xml_with_details(chunks[1]) != True:
                raise self.InvalidFbootState
            
            if chunks[0] != "":
                self.resources_running.add(chunks[0])
                self.config = self.config_dictionary.get(chunks[0])
                if self.config is None:
                    self.config_dictionary[chunks[0]] = Configuration(chunks[0], "EMB_RES", monitor=self.main_manager.monitor)
                    self.config = self.config_dictionary.get(chunks[0])
                    self.main_manager.set_config(chunks[0], self.config)

            xml_element = ETree.fromstring(chunks[1])
            try:
                if xml_element.get('Action') == 'CREATE':
                    for child in xml_element:
                        if child.tag == 'Connection':
                            if len(self.method_names) == 0 or ( not utils.any_element_in_string(self.method_names, child.get('Source')) \
                                                                and not utils.any_element_in_string(self.method_names, child.get('Destination'))):
                                self.config.create_connection(child.get('Source'), child.get('Destination'))
                            elif len(self.method_names) != 0:
                                if utils.any_element_in_string(self.method_names, child.get('Source')):
                                    # Save event name to be triggered
                                    self.method_event = child.get('Destination')
                                elif utils.any_element_in_string(self.method_names, child.get('Destination')):
                                    # save name of final fb to execute
                                    self.method_final_fb = child.get('Source').split('.')[0]
                elif xml_element.get('Action') == 'WRITE':
                    for child in xml_element:
                        if child.tag == 'Connection':
                            if len(self.method_names) == 0 or not utils.any_element_in_string(self.method_names, child.get('Destination')):
                                # Write connection
                                self.config.write_connection(child.get('Source'), child.get('Destination'))    
                            elif len(self.method_names) != 0 and utils.any_element_in_string(self.method_names, child.get('Destination')):
                                # Save wrapper info
                                info_type = child.get('Destination').split('.')[1]
                                if info_type == 'INPUT':
                                    self.method_inputs = child.get('Source')
                                elif info_type == 'OUTPUT':
                                    self.method_outputs = child.get('Source')
                                elif info_type == 'METHOD_NAME':
                                    self.opcua_method_name = child.get('Source')                   
            except KeyError:
                raise self.InvalidFbootState

    def parse_fbt(self, fb_name, file):
        xml_tree = ETree.parse(file.name)
        xml_root = xml_tree.getroot()
        if xml_root.get('OpcUa') == 'METHOD':
            # set flag to create ua_method
            self.method_names.append(fb_name)
            self.method_root = xml_root
        else:
            # add ua object to dictionary
            map_arr = []
            if fb_name in self.opc_mapped_vars:
                map_arr = self.opc_mapped_vars[fb_name]
            if not self.observer.is_class_instance_set():
                self.observer.set_class_instance(self.config)
            item = ua_object.UaObject(self, self.folders.get('FunctionBlocks'), fb_name, xml_root, opc_mapping=map_arr, root_path=self.ROOT_PATH, root_list=self.ROOT_LIST)
            self.ua_objects[fb_name] = item
        file.close()

    def stop_ua(self):
        # stops the monitor thread
        self.monitor_hardware.stop()
        # stops the configuration work
        self.config.stop_work()
        # stops the ua server
        self.stop()
          
