from opcua import ua
import os
import sys
import logging
from importlib.resources import files

UA_TYPES = {
            # Boolean
            'BOOL': ua.VariantType.Boolean,
            'Boolean': ua.VariantType.Boolean,
            # Signed integers
            'SINT': ua.VariantType.SByte,        # 8-bit signed (-128..127)
            'INT': ua.VariantType.Int16,         # 16-bit signed (-32768..32767)
            'DINT': ua.VariantType.Int32,        # 32-bit signed
            'LINT': ua.VariantType.Int64,        # 64-bit signed
            # Unsigned integers
            'USINT': ua.VariantType.Byte,        # 8-bit unsigned (0..255)
            'UINT': ua.VariantType.UInt16,       # 16-bit unsigned (0..65535)
            'UDINT': ua.VariantType.UInt32,      # 32-bit unsigned
            'ULINT': ua.VariantType.UInt64,      # 64-bit unsigned
            # Bitmasks
            'BYTE': ua.VariantType.Byte,         # 8-bit bitmask
            'WORD': ua.VariantType.UInt16,       # 16-bit bitmask
            'DWORD': ua.VariantType.UInt32,      # 32-bit bitmask
            'LWORD': ua.VariantType.UInt64,      # 64-bit bitmask
            # Floating point
            'REAL': ua.VariantType.Float,        # 32-bit float
            'LREAL': ua.VariantType.Double,      # 64-bit float
            # Strings
            'STRING': ua.VariantType.String,
            'WSTRING': ua.VariantType.String,
            'CHAR': ua.VariantType.String,
            'WCHAR': ua.VariantType.String,
            # Time and date
            'TIME': ua.VariantType.String,
            'DATE': ua.VariantType.String,
            'TIME_OF_DAY': ua.VariantType.String,
            'TOD': ua.VariantType.String,
            'DATE_AND_TIME': ua.VariantType.String,
            'DT': ua.VariantType.String,
            # Legacy / 4diac XML aliases
            'String': ua.VariantType.String,
            'Double': ua.VariantType.Double,
            'Integer': ua.VariantType.Int64,
            'Float': ua.VariantType.Float,
            # generic types
            'ANY': ua.VariantType.String,
            'ANY_ELEMENTARY': ua.VariantType.String,
            'ANY_MAGNITUDE': ua.VariantType.String,
            'ANY_NUM': ua.VariantType.String,
            'ANY_REAL': ua.VariantType.Double,
            'ANY_INT': ua.VariantType.Int64,
            'ANY_UNSIGNED': ua.VariantType.UInt64,
            'ANY_SIGNED': ua.VariantType.Int64,
            'ANY_INTEGRAL': ua.VariantType.Int64,
            'ANY_BIT': ua.VariantType.Byte,
            'ANY_CHARS': ua.VariantType.String,
            'ANY_CHAR': ua.VariantType.String,
            'ANY_STRING': ua.VariantType.String,
            'ANY_DATE': ua.VariantType.String,
            }

XML_4DIAC = {'String': 'String',
             'STRING': 'String',
             'WSTRING': 'String',
             'CHAR': 'String',
             'WCHAR': 'String',
             'Double': 'Double',
             'Integer': 'Integer',
             'SINT': 'Integer',
             'INT': 'Integer',
             'DINT': 'Integer',
             'LINT': 'Integer',
             'USINT': 'Integer',
             'UINT': 'Integer',
             'UDINT': 'Integer',
             'ULINT': 'Integer',
             'BYTE': 'Integer',
             'WORD': 'Integer',
             'DWORD': 'Integer',
             'LWORD': 'Integer',
             'Float': 'Float',
             'REAL': 'Float',
             'LREAL': 'Double',
             'BOOL': 'Boolean',
             'Boolean': 'Boolean',
             'TIME': 'String',
             'DATE': 'String',
             'TIME_OF_DAY': 'String',
             'TOD': 'String',
             'DATE_AND_TIME': 'String',
             'DT': 'String'}

UA_NODE = {ua.VariantType.Boolean: ua.NodeId(ua.ObjectIds.Boolean),
           ua.VariantType.SByte: ua.NodeId(ua.ObjectIds.SByte),
           ua.VariantType.Byte: ua.NodeId(ua.ObjectIds.Byte),
           ua.VariantType.Int16: ua.NodeId(ua.ObjectIds.Int16),
           ua.VariantType.UInt16: ua.NodeId(ua.ObjectIds.UInt16),
           ua.VariantType.Int32: ua.NodeId(ua.ObjectIds.Int32),
           ua.VariantType.UInt32: ua.NodeId(ua.ObjectIds.UInt32),
           ua.VariantType.Int64: ua.NodeId(ua.ObjectIds.Int64),
           ua.VariantType.UInt64: ua.NodeId(ua.ObjectIds.UInt64),
           ua.VariantType.Float: ua.NodeId(ua.ObjectIds.Float),
           ua.VariantType.Double: ua.NodeId(ua.ObjectIds.Double),
           ua.VariantType.String: ua.NodeId(ua.ObjectIds.String),
           ua.VariantType.DateTime: ua.NodeId(ua.ObjectIds.DateTime)}

XML_NODE = {ua.ObjectIds.Boolean: 'Boolean',
            ua.ObjectIds.SByte: 'Integer',
            ua.ObjectIds.Byte: 'Integer',
            ua.ObjectIds.Int16: 'Integer',
            ua.ObjectIds.UInt16: 'Integer',
            ua.ObjectIds.Int32: 'Integer',
            ua.ObjectIds.UInt32: 'Integer',
            ua.ObjectIds.Int64: 'Integer',
            ua.ObjectIds.UInt64: 'Integer',
            ua.ObjectIds.Float: 'Float',
            ua.ObjectIds.Double: 'Double',
            ua.ObjectIds.String: 'String',
            ua.ObjectIds.DateTime: 'String'}

# If openFB used as a package set env var OPENFB_LOCAL_DIR with to resources folder 
if os.environ.get("OPENFB_LOCAL_DIR"):
    resource_dir = os.environ.get("OPENFB_LOCAL_DIR")
else:
    resource_dir = str(files("openfb.resources"))


def default_folder(ua_peer, obj_idx, obj_path, path_list, folder_name):
    # creates the methods folder
    folder_idx = '{0}:{1}'.format(obj_idx, folder_name)
    browse_name = '2:{0}'.format(folder_name)
    ua_peer.create_folder(obj_path, folder_idx, browse_name)
    # path for the methods folder
    folder_list = path_list + [(2, folder_name)]
    folder_path = ua_peer.generate_path(folder_list)
    return folder_idx, folder_path, folder_list


def default_property(ua_peer, obj_idx, obj_path, property_name, property_value):
    prop_idx = '{0}.{1}'.format(obj_idx, property_name)
    browse_name = '2:{0}'.format(property_name)
    ua_peer.create_property(obj_path, prop_idx, browse_name, property_value)


def default_object(ua_peer, obj_idx, obj_path, path_list, obj_name):
    browse_name = '2:{0}'.format(obj_name)
    ua_peer.create_object(obj_idx, browse_name, path=obj_path)
    # sets the path for the device object
    new_list = path_list + [(2, obj_name)]
    new_path = ua_peer.generate_path(new_list)
    return new_list, new_path


def parse_fb_description(fb_xml):
    input_events_xml, output_events_xml, input_vars_xml, output_vars_xml = None, None, None, None
    for item in fb_xml:
        # gets the events and vars
        if item.tag == 'InterfaceList':
            # Iterates over the interface list
            # to find the inputs/outputs
            for interface in item:
                # Input events
                if interface.tag == 'EventInputs':
                    input_events_xml = interface
                # Output events
                elif interface.tag == 'EventOutput':
                    output_events_xml = interface
                # Input variables
                elif interface.tag == 'InputVars':
                    input_vars_xml = interface
                # Output variables
                elif interface.tag == 'OutputVars':
                    output_vars_xml = interface

    return input_events_xml, output_events_xml, input_vars_xml, output_vars_xml


def any_element_in_string(array, string):
    for element in array:
        if element in string:
            return True

    return False


def get_fb_files_path(fb_name):
    root_fbs_path = os.path.join(resource_dir, 'function_blocks')
    try:
        #fixme: new types like iec61499::system::EMB_RES
        fb_name = fb_name.split('::')[-1]
        path = next(scan_match(fb_name, root_fbs_path))
    except Exception as e:
        logging.error("[ERROR] FB does not exist. name {0} path {1}".format(fb_name, root_fbs_path))
        # sys.exit(0)
        return None

    if "__pycache__" in path:
        path = path.replace('/__pycache__', '')
    return path


def scan_match(fb_name, dir):
    for entry in os.scandir(dir):
        if entry.is_dir():
            yield from scan_match(fb_name, entry.path)
        elif entry.name.split('.')[0] == fb_name:
            yield dir


class UaInterface:

    def from_xml(self, item_xml):
        raise NotImplementedError

    def from_fb(self, fb, optional_fb_xml):
        raise NotImplementedError

    def save_xml(self, xml_set):
        raise NotImplementedError
