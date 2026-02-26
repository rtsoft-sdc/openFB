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
    def convert_type(value, value_type):
        print(value, " ----- ", value_type)
        INT_INFO = {
            'SINT': (8, True),   'USINT': (8, False),  'BYTE':  (8, False),
            'INT':  (16, True),  'UINT':  (16, False),  'WORD':  (16, False),
            'DINT': (32, True),  'UDINT': (32, False),  'DWORD': (32, False),
            'LINT': (64, True),  'ULINT': (64, False),  'LWORD': (64, False),
        }
        STRING_T   = {'STRING', 'WSTRING', 'CHAR', 'WCHAR'}
        TIMEDATE_T = {'TIME', 'DATE', 'TIME_OF_DAY', 'TOD', 'DATE_AND_TIME', 'DT'}
        REAL_T     = {'REAL', 'LREAL'}
        ALL_CONCRETE = STRING_T | TIMEDATE_T | REAL_T | set(INT_INFO) | {'BOOL'}

        TD_PREFIX = {'T': 'TIME', 'D': 'DATE', 'TOD': 'TIME_OF_DAY', 'DT': 'DATE_AND_TIME'}

        SIGNED_CHAIN   = ['SINT', 'INT', 'DINT', 'LINT']
        UNSIGNED_CHAIN = ['USINT', 'UINT', 'UDINT', 'ULINT']
        BITMASK_CHAIN  = ['BYTE', 'WORD', 'DWORD', 'LWORD']
        BITMASK_SET    = set(BITMASK_CHAIN)

        GEN_FAM = {
            'ANY':            {'bool', 'int', 'real', 'string', 'char', 'time', 'date'},
            'ANY_ELEMENTARY': {'bool', 'int', 'real', 'bit', 'string', 'char', 'time', 'date'},
            'ANY_MAGNITUDE':  {'int', 'real', 'time'},
            'ANY_NUM':        {'int', 'real'},
            'ANY_INTEGRAL':   {'int', 'bit'},
            'ANY_REAL':       {'real'},
            'ANY_INT':        {'int'},
            'ANY_UNSIGNED':   {'unsigned'},
            'ANY_SIGNED':     {'signed'},
            'ANY_BIT':        {'bool', 'bit'},
            'ANY_CHARS':      {'string', 'char'},
            'ANY_CHAR':       {'char'},
            'ANY_STRING':     {'string'},
            'ANY_DATE':       {'date'},
        }

        def _parse_int(v):
            if isinstance(v, bool):
                return int(v)
            if isinstance(v, (int, float)):
                return int(v)
            s = str(v).strip()
            if s.lower().startswith('0x'):
                return int(s, 16)
            if re.fullmatch(r'[0-9a-fA-F]+h', s):
                return int(s[:-1], 16)
            if re.fullmatch(r'[0-9a-fA-F]+', s) and any(c.isalpha() for c in s):
                return int(s, 16)
            return int(float(s))

        def _wrap(val, bits, signed):
            mask = (1 << bits) - 1
            v = val & mask
            if signed and v & (1 << (bits - 1)):
                return v - (1 << bits)
            return v

        def _fits(val, tname):
            bits, signed = INT_INFO[tname]
            lo = -(1 << (bits - 1)) if signed else 0
            hi = (1 << (bits - 1)) - 1 if signed else (1 << bits) - 1
            return lo <= val <= hi

        def _to_bool(v):
            if isinstance(v, bool):
                return v
            if isinstance(v, (int, float)):
                return bool(int(v))
            s = str(v).strip().upper()
            if s in ('TRUE', '1', 'YES', 'T', 'Y', 'ON'):
                return True
            if s in ('FALSE', '0', 'NO', 'F', 'N', 'OFF', ''):
                return False
            # Try to convert to number
            try:
                num_val = float(s)
                return bool(int(num_val))
            except (ValueError, TypeError):
                pass
            return bool(v)

        def _to_int(v, tname):
            bits, signed = INT_INFO[tname]
            iv = _parse_int(v)

            if _fits(iv, tname):
                return _wrap(iv, bits, signed)

            if tname in BITMASK_SET:
                primary, secondary = BITMASK_CHAIN, UNSIGNED_CHAIN
            elif signed:
                primary, secondary = SIGNED_CHAIN, UNSIGNED_CHAIN
            else:
                primary, secondary = UNSIGNED_CHAIN, SIGNED_CHAIN

            for chain in (primary, secondary):
                for t in chain:
                    tb, ts = INT_INFO[t]
                    if tb >= bits and _fits(iv, t):
                        return (_wrap(iv, tb, ts), t)

            return _wrap(iv, bits, signed)

        def _to_concrete(v, ctype):
            print("!!!!!!", ctype)
            if ctype == 'BOOL':
                return _to_bool(v)
            if ctype in REAL_T:
                # Handle boolean values in REAL type
                s = str(v).strip().upper()
                if s in ('TRUE', '1'):
                    return 1.0
                if s in ('FALSE', '0'):
                    return 0.0
                try:
                    return float(v)
                except (ValueError, TypeError):
                    return 0.0
            if ctype in INT_INFO:
                bits, sgn = INT_INFO[ctype]
                return _wrap(_parse_int(v), bits, sgn)
            return str(v)

        def _pick_signed(iv):
            for t in SIGNED_CHAIN:
                if _fits(iv, t):
                    return t
            return 'LINT'

        def _pick_unsigned(iv):
            for t in UNSIGNED_CHAIN:
                if _fits(iv, t):
                    return t
            return 'ULINT'

        def _pick_int(iv):
            for b in (8, 16, 32, 64):
                for t in SIGNED_CHAIN:
                    if INT_INFO[t][0] == b and _fits(iv, t):
                        return t
                for t in UNSIGNED_CHAIN:
                    if INT_INFO[t][0] == b and _fits(iv, t):
                        return t
            return 'LINT'

        def _pick_bit(iv):
            if 0 <= iv <= 1:
                return 'BOOL'
            for t in BITMASK_CHAIN:
                if _fits(iv, t):
                    return t
            return 'LWORD'

        def _select_int(iv, fam):
            if 'int' in fam:
                return _pick_int(iv)
            if 'signed' in fam and 'unsigned' not in fam:
                return _pick_signed(iv)
            if 'unsigned' in fam and 'signed' not in fam:
                return _pick_unsigned(iv)
            if 'bit' in fam:
                return _pick_bit(iv)
            return None

        # generics
        def _infer(raw, fam):
           
            if isinstance(raw, bool):
                if fam & {'bool', 'bit'}:
                    return raw, 'BOOL'
                if fam & {'int', 'signed', 'unsigned'}:
                    return int(raw), 'USINT'
                return raw, 'BOOL'

            if isinstance(raw, float):
                if 'real' in fam:
                    return raw, 'LREAL'
                if fam & {'int', 'signed', 'unsigned', 'bit'}:
                    iv = int(raw)
                    t = _select_int(iv, fam)
                    if t:
                        if t == 'BOOL':
                            return bool(iv), 'BOOL'
                        return _wrap(iv, *INT_INFO[t]), t
                return raw, 'LREAL'

            if isinstance(raw, int):
                t = _select_int(raw, fam)
                if t:
                    if t == 'BOOL':
                        return bool(raw), 'BOOL'
                    return _wrap(raw, *INT_INFO[t]), t
                if 'real' in fam:
                    return float(raw), 'LREAL'
                return raw, 'LINT'

            s = str(raw).strip()

            if fam & {'bool', 'bit'} and s.upper() in ('TRUE', 'FALSE'):
                return _to_bool(s), 'BOOL'

            if 'real' in fam and ('.' in s or 'e' in s.lower()):
                try:
                    return float(s), 'LREAL'
                except ValueError:
                    pass

            if fam & {'int', 'signed', 'unsigned', 'bit'}:
                try:
                    iv = _parse_int(s)
                    t = _select_int(iv, fam)
                    if t:
                        if t == 'BOOL':
                            return bool(iv), 'BOOL'
                        return _wrap(iv, *INT_INFO[t]), t
                except (ValueError, TypeError):
                    pass

            # time / date 
            if 'time' in fam and 'string' not in fam and 'char' not in fam:
                return s, 'TIME'
            if 'date' in fam and 'string' not in fam and 'char' not in fam:
                return s, 'DATE'

            # char / string
            if 'char' in fam and len(s) == 1:
                return s, 'CHAR'
            if 'string' in fam:
                return s, 'STRING'

            return s, 'STRING'

        try:
            raw = value
            hint = None  # concrete type extracted from value prefix

            if isinstance(value, str) and '#' in value:
                pfx, _, rest = value.partition('#')
                pu = pfx.strip().upper()

                if pu in ALL_CONCRETE:
                    hint, raw = pu, rest
                elif pu in TD_PREFIX:
                    hint, raw = TD_PREFIX[pu], rest
                elif pfx.strip().isdigit():
                    raw = ('0x' + rest) if int(pfx.strip()) == 16 else rest
                else:
                    raw = rest

            # concrete types
            if value_type in STRING_T:
                return str(raw)

            if value_type in TIMEDATE_T:
                # Handle empty values after prefix removal
                s = str(raw).strip()
                if not s:
                    # Return default based on type
                    if value_type in ('DATE_AND_TIME', 'DT'):
                        return 'DT#1970-01-01-00:00:00'
                    if value_type == 'TIME':
                        return 'T#0s'
                    if value_type == 'DATE':
                        return 'D#1970-01-01'
                    if value_type in ('TIME_OF_DAY', 'TOD'):
                        return 'TOD#00:00:00'
                return s

            if value_type == 'BOOL':
                return _to_bool(raw)

            LEGACY = {
                'String': 'STRING', 'Boolean': 'BOOL',
                'Integer': 'LINT', 'Float': 'REAL', 'Double': 'LREAL',
            }
            if value_type in LEGACY:
                return _to_concrete(raw, LEGACY[value_type])

            if value_type in REAL_T:
                s = str(raw).strip().upper()
                if s in ('TRUE', '1', 'True', 'true'):
                    return 1.0
                if s in ('FALSE', '0', 'False', 'false'):
                    return 0.0
                try:
                    return float(raw)
                except (ValueError, TypeError):
                    logging.warning(f'Cannot convert {raw!r} to REAL, returning 0.0')
                    return 0.0

            if value_type in INT_INFO:
                return _to_int(raw, value_type)

            # generics
            if value_type in GEN_FAM:
                if hint:
                    return (_to_concrete(raw, hint), hint)
                return _infer(raw, GEN_FAM[value_type])

            try:
                return int(value)
            except (ValueError, TypeError):
                return str(value)

        except Exception as e:
            logging.error(f'Cannot convert value={value!r} to type={value_type}: {e}')
            return None
