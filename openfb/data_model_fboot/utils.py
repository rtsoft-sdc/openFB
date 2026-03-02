"""
1. TypeRegistry - centralized type information for all IEC 61499 types
2. TypeConverter - specialized type conversion engine
3. Utility functions for OpenFB operations
4. Backward-compatible type dictionaries (UA_TYPES, XML_4DIAC, UA_NODE)
"""

from opcua import ua
from dataclasses import dataclass
from typing import Dict, Any, Tuple, Set, Optional, Union
import os
import logging
from importlib.resources import files
import re

@dataclass
class TypeDef:
    ua_variant_type: ua.VariantType
    ua_object_id: int
    xml_4diac_type: str
    default_value: Any
    category: str
    bits: Optional[int] = None
    is_signed: Optional[bool] = None
    aliases: Tuple[str, ...] = ()
    
    def get_ua_node_id(self) -> ua.NodeId:
        return ua.NodeId(self.ua_object_id)


class TypeRegistry:
    
    GENERIC_IMPLIED: Dict[str, Tuple[str, ...]] = {
        'ANY': ('ANY_ELEMENTARY', 'ANY_MAGNITUDE', 'ANY_BIT', 'ANY_CHARS', 'ANY_DATE', 
                'ANY_INT', 'ANY_REAL', 'TIME', 'BOOL', 'BYTE', 'WORD', 'DWORD', 'LWORD',
                'SINT', 'INT', 'DINT', 'LINT', 'USINT', 'UINT', 'UDINT', 'ULINT',
                'REAL', 'LREAL', 'STRING', 'WSTRING', 'CHAR', 'WCHAR', 'DATE', 'DATE_AND_TIME', 'TIME_OF_DAY'),
        'ANY_ELEMENTARY': ('ANY_MAGNITUDE', 'ANY_BIT', 'ANY_CHARS', 'ANY_DATE'),
        'ANY_MAGNITUDE': ('ANY_INT', 'ANY_REAL', 'TIME'),
        'ANY_INTEGRAL': ('ANY_INT', 'ANY_BIT'),
        'ANY_NUM': ('ANY_INT', 'ANY_REAL'),
        'ANY_REAL': ('REAL', 'LREAL'),
        'ANY_INT': ('SINT', 'INT', 'DINT', 'LINT', 'USINT', 'UINT', 'UDINT', 'ULINT', 'ANY_SIGNED', 'ANY_UNSIGNED'),
        'ANY_UNSIGNED': ('USINT', 'UINT', 'UDINT', 'ULINT'),
        'ANY_SIGNED': ('SINT', 'INT', 'DINT', 'LINT'),
        'ANY_BIT': ('BOOL', 'BYTE', 'WORD', 'DWORD', 'LWORD'),
        'ANY_CHARS': ('ANY_CHAR', 'ANY_STRING'),
        'ANY_CHAR': ('CHAR', 'WCHAR'),
        'ANY_STRING': ('STRING', 'WSTRING'),
        'ANY_DATE': ('DATE_AND_TIME', 'DATE', 'TIME_OF_DAY'),
    }
    
    TYPES: Dict[str, TypeDef] = {
        'BOOL': TypeDef(ua.VariantType.Boolean, ua.ObjectIds.Boolean, 'Boolean', False, 'bool', aliases=('Boolean',)),
        'SINT': TypeDef(ua.VariantType.SByte, ua.ObjectIds.SByte, 'Integer', 0, 'integer', 8, True),
        'INT': TypeDef(ua.VariantType.Int16, ua.ObjectIds.Int16, 'Integer', 0, 'integer', 16, True),
        'DINT': TypeDef(ua.VariantType.Int32, ua.ObjectIds.Int32, 'Integer', 0, 'integer', 32, True),
        'LINT': TypeDef(ua.VariantType.Int64, ua.ObjectIds.Int64, 'Integer', 0, 'integer', 64, True),
        'USINT': TypeDef(ua.VariantType.Byte, ua.ObjectIds.Byte, 'Integer', 0, 'integer', 8, False),
        'UINT': TypeDef(ua.VariantType.UInt16, ua.ObjectIds.UInt16, 'Integer', 0, 'integer', 16, False),
        'UDINT': TypeDef(ua.VariantType.UInt32, ua.ObjectIds.UInt32, 'Integer', 0, 'integer', 32, False),
        'ULINT': TypeDef(ua.VariantType.UInt64, ua.ObjectIds.UInt64, 'Integer', 0, 'integer', 64, False),
        'BYTE': TypeDef(ua.VariantType.Byte, ua.ObjectIds.Byte, 'Integer', 0, 'integer', 8, False),
        'WORD': TypeDef(ua.VariantType.UInt16, ua.ObjectIds.UInt16, 'Integer', 0, 'integer', 16, False),
        'DWORD': TypeDef(ua.VariantType.UInt32, ua.ObjectIds.UInt32, 'Integer', 0, 'integer', 32, False),
        'LWORD': TypeDef(ua.VariantType.UInt64, ua.ObjectIds.UInt64, 'Integer', 0, 'integer', 64, False),
        'REAL': TypeDef(ua.VariantType.Float, ua.ObjectIds.Float, 'Float', 0.0, 'float'),
        'LREAL': TypeDef(ua.VariantType.Double, ua.ObjectIds.Double, 'Double', 0.0, 'float', aliases=('Double',)),
        'STRING': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', '', 'string', aliases=('WSTRING', 'CHAR', 'WCHAR', 'String')),
        'TIME': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', 'T#0s', 'time_date'),
        'DATE': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', 'D#1970-01-01', 'time_date'),
        'TIME_OF_DAY': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', 'TOD#00:00:00', 'time_date', aliases=('TOD',)),
        'DATE_AND_TIME': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', 'DT#1970-01-01-00:00:00', 'time_date', aliases=('DT',)),
        'ANY': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', '', 'string'),
        'ANY_ELEMENTARY': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', '', 'string'),
        'ANY_MAGNITUDE': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', 0, 'integer'),
        'ANY_NUM': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', 0, 'integer'),
        'ANY_REAL': TypeDef(ua.VariantType.Double, ua.ObjectIds.Double, 'Double', 0.0, 'float'),
        'ANY_INT': TypeDef(ua.VariantType.Int64, ua.ObjectIds.Int64, 'Integer', 0, 'integer'),
        'ANY_UNSIGNED': TypeDef(ua.VariantType.UInt64, ua.ObjectIds.UInt64, 'Integer', 0, 'integer', is_signed=False),
        'ANY_SIGNED': TypeDef(ua.VariantType.Int64, ua.ObjectIds.Int64, 'Integer', 0, 'integer', is_signed=True),
        'ANY_INTEGRAL': TypeDef(ua.VariantType.Int64, ua.ObjectIds.Int64, 'Integer', 0, 'integer'),
        'ANY_BIT': TypeDef(ua.VariantType.Byte, ua.ObjectIds.Byte, 'Integer', False, 'bool'),
        'ANY_CHARS': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', '', 'string'),
        'ANY_CHAR': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', '', 'string'),
        'ANY_STRING': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', '', 'string'),
        'ANY_DATE': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', 'DT#1970-01-01-00:00:00', 'time_date'),
    }
    
    @classmethod
    def resolve_type(cls, type_name: str) -> Optional[TypeDef]:
        if type_name in cls.TYPES:
            return cls.TYPES[type_name]
        for mapping in cls.TYPES.values():
            if type_name in mapping.aliases:
                return mapping
        return None
    
    @classmethod
    def get_default_value(cls, type_name: str) -> Any:
        mapping = cls.resolve_type(type_name)
        return mapping.default_value if mapping else 0
    
    @classmethod
    def get_ua_variant_type(cls, type_name: str) -> Optional[ua.VariantType]:
        mapping = cls.resolve_type(type_name)
        return mapping.ua_variant_type if mapping else None
    
    @classmethod
    def get_ua_node_id(cls, type_name: str) -> Optional[ua.NodeId]:
        mapping = cls.resolve_type(type_name)
        return mapping.get_ua_node_id() if mapping else None
    
    @classmethod
    def get_xml_type(cls, type_name: str) -> Optional[str]:
        mapping = cls.resolve_type(type_name)
        return mapping.xml_4diac_type if mapping else None
    
    @classmethod
    def get_category(cls, type_name: str) -> Optional[str]:
        mapping = cls.resolve_type(type_name)
        return mapping.category if mapping else None
    
    @classmethod
    def get_int_info(cls, type_name: str) -> Optional[Tuple[int, bool]]:
        mapping = cls.resolve_type(type_name)
        if mapping and mapping.bits is not None:
            return (mapping.bits, mapping.is_signed)
        return None
    
    @classmethod
    def is_integer_type(cls, type_name: str) -> bool:
        return cls.get_category(type_name) == 'integer'
    
    @classmethod
    def is_float_type(cls, type_name: str) -> bool:
        return cls.get_category(type_name) == 'float'
    
    @classmethod
    def is_bool_type(cls, type_name: str) -> bool:
        return cls.get_category(type_name) == 'bool'
    
    @classmethod
    def is_string_type(cls, type_name: str) -> bool:
        return cls.get_category(type_name) == 'string'
    
    @classmethod
    def is_time_date_type(cls, type_name: str) -> bool:
        return cls.get_category(type_name) == 'time_date'
    
    @classmethod
    def is_generic_type(cls, type_name: str) -> bool:
        return type_name in cls.GENERIC_IMPLIED
    
    @classmethod
    def get_implied_types(cls, generic_type: str, recursive: bool = True) -> Set[str]:
        
        if generic_type not in cls.GENERIC_IMPLIED:
            return set()
        
        result = set()
        to_process = list(cls.GENERIC_IMPLIED[generic_type])
        
        while to_process:
            type_name = to_process.pop(0)
            if type_name in result:
                continue
            result.add(type_name)
            
            if recursive and type_name in cls.GENERIC_IMPLIED:
                to_process.extend(cls.GENERIC_IMPLIED[type_name])
        
        return result
    
    @classmethod
    def is_type_compatible(cls, value_type: str, target_type: str) -> bool:
        if value_type == target_type:
            return True

        if target_type in cls._GENERIC_IMPLIED:
            implied = cls.get_implied_types(target_type, recursive=True)
            return value_type in implied
        
        value_mapping = cls.resolve_type(value_type)
        target_mapping = cls.resolve_type(target_type)
        if value_mapping and target_mapping:
            return value_mapping == target_mapping
        return False
    
    @classmethod
    def get_ua_types_dict(cls) -> Dict[str, ua.VariantType]:
        result = {}
        for type_name, mapping in cls.TYPES.items():
            result[type_name] = mapping.ua_variant_type
            for alias in mapping.aliases:
                result[alias] = mapping.ua_variant_type
        return result
    
    @classmethod
    def get_xml_4diac_dict(cls) -> Dict[str, str]:
        result = {}
        for type_name, mapping in cls.TYPES.items():
            result[type_name] = mapping.xml_4diac_type
            for alias in mapping.aliases:
                result[alias] = mapping.xml_4diac_type
        return result
    
    @classmethod
    def get_ua_node_dict(cls) -> Dict[ua.VariantType, ua.NodeId]:
        result = {}
        for mapping in cls.TYPES.values():
            if mapping.ua_variant_type not in result:
                result[mapping.ua_variant_type] = mapping.get_ua_node_id()
        return result


class IntegerConverter:
    
    SIGNED_CHAIN = ['SINT', 'INT', 'DINT', 'LINT']
    UNSIGNED_CHAIN = ['USINT', 'UINT', 'UDINT', 'ULINT']
    BITMASK_CHAIN = ['BYTE', 'WORD', 'DWORD', 'LWORD']
    BITMASK_SET = set(BITMASK_CHAIN)
    
    @staticmethod
    def parse_int(value: Any) -> int:
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, (int, float)):
            return int(value)
        s = str(value).strip()
        if s.lower().startswith('0x'):
            return int(s, 16)
        if re.fullmatch(r'[0-9a-fA-F]+h', s, re.IGNORECASE):
            return int(s[:-1], 16)
        if re.fullmatch(r'[0-9a-fA-F]+', s) and any(c.isalpha() for c in s):
            return int(s, 16)
        return int(float(s))
    
    @staticmethod
    def wrap(value: int, bits: int, is_signed: bool) -> int:
        mask = (1 << bits) - 1
        v = value & mask
        if is_signed and v & (1 << (bits - 1)):
            return v - (1 << bits)
        return v
    
    @staticmethod
    def fits(value: int, type_name: str) -> bool:
        int_info = TypeRegistry.get_int_info(type_name)
        if not int_info:
            return False
        bits, is_signed = int_info
        lo = -(1 << (bits - 1)) if is_signed else 0
        hi = (1 << (bits - 1)) - 1 if is_signed else (1 << bits) - 1
        return lo <= value <= hi
    
    @classmethod
    def find_fitting_type(cls, value: int, bits: int, is_signed: bool) -> Optional[str]:
        if is_signed:
            chains = [cls.SIGNED_CHAIN]
        else:
            chains = [cls.UNSIGNED_CHAIN, cls.BITMASK_CHAIN]
        for chain in chains:
            for type_name in chain:
                if cls.fits(value, type_name):
                    return type_name
        return None
    
    @classmethod
    def convert_to_int(cls, value: Any, target_type: str) -> Union[int, Tuple[int, str]]:
        int_info = TypeRegistry.get_int_info(target_type)
        if not int_info:
            logging.warning(f"Type {target_type} is not an integer type")
            return 0
        bits, is_signed = int_info
        try:
            iv = cls.parse_int(value)
        except (ValueError, TypeError) as e:
            logging.warning(f"Cannot parse {value!r} as integer: {e}")
            return 0
        if cls.fits(iv, target_type):
            return cls.wrap(iv, bits, is_signed)
        fitting_type = cls.find_fitting_type(iv, bits, is_signed)
        if fitting_type and fitting_type != target_type:
            logging.info(f"Value {iv} doesn't fit in {target_type}, promoting to {fitting_type}")
            fit_bits, fit_signed = TypeRegistry.get_int_info(fitting_type)
            return (cls.wrap(iv, fit_bits, fit_signed), fitting_type)
        return cls.wrap(iv, bits, is_signed)


class FloatConverter:

    @staticmethod
    def convert_to_float(value: Any, target_type: str) -> float:
        s = str(value).strip().upper()
        if s in ('TRUE', '1'):
            return 1.0
        if s in ('FALSE', '0'):
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError) as e:
            logging.warning(f"Cannot convert {value!r} to {target_type}: {e}, returning 0.0")
            return 0.0


class BoolConverter:
    
    @staticmethod
    def convert_to_bool(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(int(value))
        s = str(value).strip().upper()
        if s in ('TRUE', '1', 'YES', 'T', 'Y', 'ON'):
            return True
        if s in ('FALSE', '0', 'NO', 'F', 'N', 'OFF', ''):
            return False
        try:
            return bool(int(float(s)))
        except (ValueError, TypeError):
            return bool(value)


class StringConverter:
    @staticmethod
    def convert_to_string(value: Any) -> str:
        return str(value)


class TimeDateConverter:
    
    @staticmethod
    def convert_to_time_date(value: Any, target_type: str) -> str:
        s = str(value).strip()
        if not s:
            default = TypeRegistry.get_default_value(target_type)
            logging.debug(f"Empty value for {target_type}, using default: {default}")
            return default
        return s


class TypeConverter:
    
    _int_converter = IntegerConverter()
    _float_converter = FloatConverter()
    _bool_converter = BoolConverter()
    _string_converter = StringConverter()
    _timedate_converter = TimeDateConverter()
    
    @classmethod
    def convert(cls, value: Any, target_type: str, source_type: Optional[str] = None) -> Union[Any, Tuple[Any, str]]:
        mapping = TypeRegistry.resolve_type(target_type)
        if not mapping:
            logging.error(f"Unknown type: {target_type}")
            return value
        canonical_type = mapping.iec_name
        try:
            if TypeRegistry.is_bool_type(canonical_type):
                return cls._bool_converter.convert_to_bool(value)
            elif TypeRegistry.is_integer_type(canonical_type):
                return cls._int_converter.convert_to_int(value, canonical_type)
            elif TypeRegistry.is_float_type(canonical_type):
                return cls._float_converter.convert_to_float(value, canonical_type)
            elif TypeRegistry.is_string_type(canonical_type):
                return cls._string_converter.convert_to_string(value)
            elif TypeRegistry.is_time_date_type(canonical_type):
                return cls._timedate_converter.convert_to_time_date(value, canonical_type)
            else:
                logging.warning(f"No converter for category: {mapping.category}")
                return value
        except Exception as e:
            logging.error(f"Error converting value={value!r} to {target_type}: {e}", exc_info=True)
            return TypeRegistry.get_default_value(canonical_type)
    
    @classmethod
    def batch_convert(cls, values: Dict[str, Any], type_map: Dict[str, str]) -> Dict[str, Any]:
        result = {}
        for name, value in values.items():
            target_type = type_map.get(name, 'STRING')
            result[name] = cls.convert(value, target_type)
        return result

UA_TYPES = TypeRegistry.get_ua_types_dict()
XML_4DIAC = TypeRegistry.get_xml_4diac_dict()
UA_NODE = TypeRegistry.get_ua_node_dict()

XML_NODE = {
    ua.ObjectIds.Boolean: 'Boolean',
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
    ua.ObjectIds.DateTime: 'String',
}



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
