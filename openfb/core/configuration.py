from openfb.core import fb_resources
from openfb.core import fb
from openfb.core import fb_interface
from xml.etree import ElementTree as ETree
import logging
import datetime
import re
import inspect



class Configuration:

    def __init__(self, config_id, config_type, monitor=None, opc_mapping=None):

        self.monitor = monitor
        self.opc_mapping = opc_mapping
        self.fb_dictionary = dict()

        self.config_id = config_id

        self.create_fb('START', config_type, opc_mapping=self.opc_mapping)

    def get_fb(self, fb_name):
        fb_element = None
        try:
            # fb_name = fb_name.replace('.', '-')           
            fb_element = self.fb_dictionary[fb_name]
        except KeyError as error:
            logging.error('can not find that fb {0} get_fb'.format(fb_name))
            logging.error(error)

        return fb_element

    def set_fb(self, fb_name, fb_element):
        self.fb_dictionary[fb_name] = fb_element

    def exists_fb(self, fb_name):
        return fb_name in self.fb_dictionary

    def create_virtualized_fb(self, fb_name, fb_type, ua_update):
        logging.info('creating a virtualized (opc-ua) fb {0}...'.format(fb_name))

        self.create_fb(fb_name, fb_type, monitor=True)
        # sets the ua variables update method
        fb2update = self.get_fb(fb_name)
        fb2update.ua_variables_update = ua_update

    def create_fb(self, fb_name, fb_type, monitor=False, opc_mapping=None):
        #fixme: new types like iec61499::system::EMB_RES
        fb_type = fb_type.split('::')[-1]

        # fb_name = fb_name.replace('.', '-')
        logging.info(f'creating a new fb {fb_name} Type: {fb_type}...')
        fb_res = fb_resources.FBResources(fb_type)

        exists_fb = fb_res.exists_fb()
        if not exists_fb:
            # Downloads the fb definition and python code
            logging.warning('fb doesnt exists, needs to be downloaded ...')
            fb_res.download_fb()

        fb_definition, fb_obj = fb_res.import_fb()

        # check if if happened any importing error
        if fb_definition is not None:

            # Checking order and number or arguments of schedule function
            # Logs warning if order and number are not the same 
            scheduleArgs = inspect.getfullargspec(fb_obj.schedule).args
            if len(scheduleArgs) > 3:
                scheduleArgs = scheduleArgs[3:]
                scheduleArgs = [i.lower() for i in scheduleArgs]
                xmlArgs = []
                for child in fb_definition:
                    inputvars = child.find('InputVars')
                    if inputvars is None:
                        continue
                    varslist = inputvars.findall('VarDeclaration')
                    for xmlVar in varslist:
                        if xmlVar.get('Name') is not None:
                            xmlArgs.append(xmlVar.get('Name').lower())
                        else:
                            logging.error('Could not find mandatory "Name" attribute for variable. Please check {0}.fbt'.format(fb_name))

                if scheduleArgs != xmlArgs:
                    logging.warning('Argument names for schedule function of {0} do not match definition in {0}.fbt'.format(fb_name))
                    logging.warning('Ensure your variable arguments are the same as the input variables and in the same order')

            ## if it is a real FB, not a hidden one
            if monitor:
                fb_element = fb.FB(fb_name, fb_type, fb_obj, fb_definition, monitor=self.monitor, opc_mapping=opc_mapping)
            else:
                fb_element = fb.FB(fb_name, fb_type, fb_obj, fb_definition, opc_mapping=opc_mapping)

            self.set_fb(fb_name, fb_element)
            logging.info('created fb type: {0}, instance: {1}'.format(fb_type, fb_name))
            logging.info("List of existing blocks: %s" % self.fb_dictionary)
            # returns the both elements
            return fb_element, fb_definition
        else:
            logging.error('can not create the fb type: {0}, instance: {1}'.format(fb_type, fb_name))
            return None, None

    def create_connection(self, source, destination):
        logging.info(f'creating a new connection between {source} and {destination}...')

        source_attr = source.split(sep='.')
        destination_attr = destination.split(sep='.')
        source_fb = self.get_fb(source_attr[0]) if len(source_attr) == 2 else self.get_fb('.'.join(source_attr[:-1]))
        source_name = source_attr[1] if len(source_attr) == 2 else source_attr[-1]
        destination_fb = self.get_fb(destination_attr[0]) if len(destination_attr) == 2 else self.get_fb('.'.join(destination_attr[:-1]))
        destination_name = destination_attr[1] if len(destination_attr) == 2 else destination_attr[-1]

        connection = fb_interface.Connection(destination_fb, destination_name)
        source_fb.add_connection(source_name, connection)

        logging.info('connection created between {0} and {1}'.format(source, destination))

    def create_watch(self, source, destination):
        logging.debug('creating a new watch...')

        source_attr = source.split(sep='.')
        source_fb =  self.get_fb(source_attr[0]) if len(source_attr) == 2 else self.get_fb('.'.join(source_attr[:-1]))
        source_name = source_attr[1] if len(source_attr) == 2 else source_attr[-1]

        try:
            source_fb.set_attr(source_name, set_watch=True)
        except AttributeError as error:
            # check if the return if None
            logging.error(error)
            logging.error("don't forget to delete the watch when you delete a function block")

        logging.debug('watch created between {0} and {1}'.format(source, destination))

    def delete_watch(self, source, destination):
        logging.debug('deleting a new watch...')

        source_attr = source.split(sep='.')
        source_fb = self.get_fb(source_attr[0]) if len(source_attr) == 2 else self.get_fb('.'.join(source_attr[:-1]))
        source_name = source_attr[1] if len(source_attr) == 2 else source_attr[-1]

        try:
            source_fb.set_attr(source_name, set_watch=False)
        except AttributeError as error:
            # check if the return if None
            # logging.error(error)
            logging.error("don't forget to delete the watch when you delete a function block")

        logging.debug('watch deleted between {0} and {1}'.format(source, destination))

    def write_connection(self, source_value, destination):
        logging.debug('writing a connection...')
        logging.debug(f"SRC: {source_value} DST {destination}")
        destination_attr = destination.split(sep='.')
        destination_fb = self.get_fb(destination_attr[0]) if len(destination_attr) == 2 else self.get_fb('.'.join(destination_attr[:-1]))
        destination_name = destination_attr[1] if len(destination_attr) == 2 else destination_attr[-1]

        v_type, value, is_watch = destination_fb.read_attr(destination_name)

        # Verifies if is to write an event
        if source_value == '$e' or v_type=='Event':
            logging.info('writing an event...')
            if value is not None:
                # If the value is not None increment
                destination_fb.push_event(destination_name, value + 1)
            else:
                # If the value is None push 1
                destination_fb.push_event(destination_name, 1)

        # Writes a hardcoded value
        else:
            value_to_set = self.convert_type(source_value, v_type)
            
            if isinstance(value_to_set, tuple) and len(value_to_set) == 2:
                conv_value, promoted_type = value_to_set
                logging.info(f"Data conversion:\n SRC: {source_value}\nType:{v_type}\n Converted value: {conv_value} PromotedType:{promoted_type} DST:{destination_name}")
                destination_fb.set_attr(destination_name, new_value=conv_value, new_type=promoted_type)
            else:
                logging.info(f"Data conversion:\n SRC: {source_value}\nType:{v_type}\n Converted value: {value_to_set} DST:{destination_name}")
                destination_fb.set_attr(destination_name, new_value=value_to_set)

        logging.info('connection ({0}) configured with the value {1}'.format(destination, source_value))

    def read_watches(self, start_time):
        logging.debug('reading watches...')

        resources_xml = ETree.Element('Resource', {'name': self.config_id})

        for fb_name, fb_element in self.fb_dictionary.items():
            fb_xml, watches_len = fb_element.read_watches(start_time)

            if watches_len > 0:
                resources_xml.append(fb_xml)

        fb_watches_len = len(resources_xml.findall('FB'))
        return resources_xml, fb_watches_len

    def start_work(self):
        logging.info('starting the fb flow...')
        for fb_name, fb_element in self.fb_dictionary.items():
            if fb_name != 'START':
                try:
                    fb_element.start()
                    # check if the update_variables service is null
                    if fb_element.ua_variables_update is not None:
                        # updates the opc-ua variables
                        fb_element.ua_variables_update()
                except:
                    pass

        outputs = self.get_fb('START').fb_obj.schedule()
        self.get_fb('START').update_outputs(outputs)

    def stop_work(self):
        logging.info('stopping the fb flow...')
        for fb_name, fb_element in self.fb_dictionary.items():
            logging.debug("Stop block %s" %fb_name)
            if fb_name != 'START':
                fb_element.stop()


    @staticmethod
    def convert_type(value, value_type): # need to rework for WORD, DWORD, LWORD, maybe for time types AND LOGS
        converted_value = None

        try:
            if value_type == 'ANY' or value_type == 'String' or value_type == 'ANY_ELEMENTARY':
                return str(value)

            #value none ne rassmatrivaem

            if isinstance(value, str) and "#" in value:
                value = value.split("#", 1)[1]

            def parse_int(v):
                if isinstance(v, int):
                    return v
                if isinstance(v, bool):
                    return int(v)
                s = str(v).strip()
                if s.lower().startswith('0x'):
                    return int(s, 16)
                if re.fullmatch(r'[0-9a-fA-F]+h', s):
                    return int(s[:-1], 16)

                if re.fullmatch(r'[0-9a-fA-F]+', s) and any(c.isalpha() for c in s):
                    return int(s, 16)
                return int(float(s))

            def wrap_signed(val, bits):
                mask = (1 << bits) - 1
                v = val & mask
                sign_bit = 1 << (bits - 1)
                if v & sign_bit:
                    return v - (1 << bits)
                return v

            def wrap_unsigned(val, bits):
                mask = (1 << bits) - 1
                return val & mask

            # strs and time
            if value_type in ('WSTRING', 'STRING', 'TIME', 'DATE', 'TIME_OF_DAY', 'DATE_AND_TIME'):
                converted_value = value
                return converted_value

            if value_type == 'BOOL':
                if isinstance(value, bool):
                    return value
                if isinstance(value, str):
                    s = value.strip()
                    if s == 'TRUE':
                        return True
                    if s == 'FALSE':
                        return False

            if value_type in ('REAL', 'LREAL'):
                return float(value)

            int_types = {
                'SINT': (8, True), 'USINT': (8, False), 'BYTE': (8, False),
                'INT': (16, True), 'UINT': (16, False), 'WORD': (16, False),
                'DINT': (32, True), 'UDINT': (32, False), 'DWORD': (32, False),
                'LINT': (64, True), 'ULINT': (64, False), 'LWORD': (64, False)
            }

            if value_type in int_types:
                bits, signed = int_types[value_type]
                try:
                    iv = parse_int(value)
                except Exception: # mb remove 
                    logging.error('cant parse int')
                    ##### need return

                if signed:
                    minv = -(1 << (bits - 1))
                    maxv = (1 << (bits - 1)) - 1
                else:
                    minv = 0
                    maxv = (1 << bits) - 1

                if minv <= iv <= maxv:
                    return wrap_signed(iv, bits) if signed else wrap_unsigned(iv, bits)

                sizes = [8, 16, 32, 64]
                start_idx = sizes.index(bits) if bits in sizes else 0

                promoted = None
                for b in sizes[start_idx:]:
                    candidates = []
                    if iv >= 0 and not signed:
                        candidates = [(b, False), (b, True)]
                    else:
                        candidates = [(b, True), (b, False)]

                    for (cb, csigned) in candidates:
                        if csigned:
                            cmin = -(1 << (cb - 1))
                            cmax = (1 << (cb - 1)) - 1
                        else:
                            cmin = 0
                            cmax = (1 << cb) - 1

                        if cmin <= iv <= cmax:
                            for tname, (tb, tsigned) in int_types.items():
                                if tb == cb and tsigned == csigned:
                                    promoted = tname
                                    break
                            if promoted:
                                return iv, promoted

                return wrap_signed(iv, bits) if signed else wrap_unsigned(iv, bits)

            try:
                return int(value)
            except Exception:
                logging.error('cant covert')
        except:
            logging.error('cant convert')

        return converted_value
