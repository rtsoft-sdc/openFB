"""
1. TypeRegistry - centralized type information for all IEC 61499 types
2. TypeConverter - specialized type conversion engine
3. Utility functions for OpenFB operations
4. Backward-compatible type dictionaries (UA_TYPES, XML_4DIAC, UA_NODE)
"""

from dataclasses import dataclass
import datetime
from importlib.resources import files
import logging
import os
import re
from typing import Any
from opcua import ua


@dataclass
class TypeDef:
    ua_variant_type: ua.VariantType
    ua_object_id: int
    xml_4diac_type: str
    default_value: Any
    category: str
    bits: int | None = None
    is_signed: bool | None = None
    aliases: tuple[str, ...] = ()
    
    def get_ua_node_id(self) -> ua.NodeId:
        return ua.NodeId(self.ua_object_id)


class TypeRegistry:
    
    GENERIC_IMPLIED: dict[str, tuple[str, ...]] = {
        'ANY': ('ANY_ELEMENTARY', 'ANY_MAGNITUDE', 'ANY_BIT', 'ANY_CHARS', 'ANY_DATE', 
                'ANY_INT', 'ANY_REAL', 'TIME', 'BOOL', 'BYTE', 'WORD', 'DWORD', 'LWORD',
                'SINT', 'INT', 'DINT', 'LINT', 'USINT', 'UINT', 'UDINT', 'ULINT',
                'REAL', 'LREAL', 'STRING', 'WSTRING', 'CHAR', 'WCHAR', 'DATE', 'DATE_AND_TIME', 'TIME_OF_DAY'),
        'ANY_ELEMENTARY': ('ANY_MAGNITUDE', 'ANY_BIT', 'ANY_CHARS', 'ANY_DATE'),
        'ANY_MAGNITUDE': ('ANY_INT', 'ANY_REAL', 'TIME'),
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
    
    TYPES: dict[str, TypeDef] = {
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
        'ANY_BIT': TypeDef(ua.VariantType.Byte, ua.ObjectIds.Byte, 'Integer', False, 'bool'),
        'ANY_CHARS': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', '', 'string'),
        'ANY_CHAR': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', '', 'string'),
        'ANY_STRING': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', '', 'string'),
        'ANY_DATE': TypeDef(ua.VariantType.String, ua.ObjectIds.String, 'String', 'DT#1970-01-01-00:00:00', 'time_date'),
    }
    
    @classmethod
    def resolve_type(cls, type_name: str) -> TypeDef | None:
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
    def get_ua_variant_type(cls, type_name: str) -> ua.VariantType | None:
        mapping = cls.resolve_type(type_name)
        return mapping.ua_variant_type if mapping else None
    
    @classmethod
    def get_ua_node_id(cls, type_name: str) -> ua.NodeId | None:
        mapping = cls.resolve_type(type_name)
        return mapping.get_ua_node_id() if mapping else None
    
    @classmethod
    def get_xml_type(cls, type_name: str) -> str | None:
        mapping = cls.resolve_type(type_name)
        return mapping.xml_4diac_type if mapping else None
    
    @classmethod
    def get_category(cls, type_name: str) -> str | None:
        mapping = cls.resolve_type(type_name)
        return mapping.category if mapping else None
    
    @classmethod
    def get_int_info(cls, type_name: str) -> tuple[int, bool] | None:
        mapping = cls.resolve_type(type_name)
        if mapping and mapping.bits is not None:
            return (mapping.bits, mapping.is_signed)
        return None
    
    @classmethod
    def is_integer_type(cls, type_name: str) -> bool:
        return cls.get_category(type_name) == 'integer'
    
    @classmethod
    def is_generic_type(cls, type_name: str) -> bool:
        return type_name in cls.GENERIC_IMPLIED
    
    @classmethod
    def get_implied_types(cls, generic_type: str, recursive: bool = True) -> set[str]:
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

        if target_type in cls.GENERIC_IMPLIED:
            implied = cls.get_implied_types(target_type, recursive=True)
            return value_type in implied
        
        value_mapping = cls.resolve_type(value_type)
        target_mapping = cls.resolve_type(target_type)
        if value_mapping and target_mapping:
            return value_mapping == target_mapping
        return False
    
    @classmethod
    def get_ua_types_dict(cls) -> dict[str, ua.VariantType]:
        result = {}
        for type_name, mapping in cls.TYPES.items():
            result[type_name] = mapping.ua_variant_type
            for alias in mapping.aliases:
                result[alias] = mapping.ua_variant_type
        return result
    
    @classmethod
    def get_xml_4diac_dict(cls) -> dict[str, str]:
        result = {}
        for type_name, mapping in cls.TYPES.items():
            result[type_name] = mapping.xml_4diac_type
            for alias in mapping.aliases:
                result[alias] = mapping.xml_4diac_type
        return result
    
    @classmethod
    def get_ua_node_dict(cls) -> dict[ua.VariantType, ua.NodeId]:
        result = {}
        for mapping in cls.TYPES.values():
            if mapping.ua_variant_type not in result:
                result[mapping.ua_variant_type] = mapping.get_ua_node_id()
        return result

    @classmethod
    def get_canonical_name(cls, type_name: str) -> str | None:
        if type_name in cls.TYPES:
            return type_name
        for canonical_name, mapping in cls.TYPES.items():
            if type_name in mapping.aliases:
                return canonical_name
        return None


class IntegerConverter:
    
    SIGNED_CHAIN = ['SINT', 'INT', 'DINT', 'LINT']
    UNSIGNED_CHAIN = ['USINT', 'UINT', 'UDINT', 'ULINT']
    BITMASK_CHAIN = ['BYTE', 'WORD', 'DWORD', 'LWORD']
    
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
    def find_fitting_type(cls, value: int, is_signed: bool) -> str | None:
        chains = [cls.SIGNED_CHAIN] if is_signed else [cls.UNSIGNED_CHAIN, cls.BITMASK_CHAIN]
        for chain in chains:
            for type_name in chain:
                if cls.fits(value, type_name):
                    return type_name
        return None
    
    @classmethod
    def convert_to_int(cls, value: Any, target_type: str) -> int | tuple[int, str]:
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
        fitting_type = cls.find_fitting_type(iv, is_signed)
        if fitting_type and fitting_type != target_type:
            logging.debug(f"Value {iv} doesn't fit in {target_type}, promoting to {fitting_type}")
            fit_bits, _ = TypeRegistry.get_int_info(fitting_type)
            return cls.wrap(iv, fit_bits, is_signed), fitting_type
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
            return bool(value)
            
        return str(value).strip().upper() == 'TRUE'


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
    
    @staticmethod
    def _parse_iec_literal(value: Any) -> tuple[str | None, Any]:
        s = str(value).strip()
        if '#' not in s or len(parts := s.split('#', 1)) != 2:
            return None, value
        
        type_prefix = parts[0].strip().upper()
        literal_value = parts[1].strip()
        
        prefix_map = {
            'BOOL': 'BOOL',
            'SINT': 'SINT', 'INT': 'INT', 'DINT': 'DINT', 'LINT': 'LINT',
            'USINT': 'USINT', 'UINT': 'UINT', 'UDINT': 'UDINT', 'ULINT': 'ULINT',
            '16': 'LWORD', 
            'REAL': 'REAL', 'LREAL': 'LREAL',
            'STRING': 'STRING', 'WSTRING': 'STRING',
            'CHAR': 'CHAR', 'WCHAR': 'CHAR',
            'TIME': 'TIME', 'T': 'TIME',
            'DATE': 'DATE', 'D': 'DATE',
            'TIME_OF_DAY': 'TIME_OF_DAY', 'TOD': 'TIME_OF_DAY',
            'DATE_AND_TIME': 'DATE_AND_TIME', 'DT': 'DATE_AND_TIME',
        }
        
        inferred_type = prefix_map.get(type_prefix)
        return (inferred_type, literal_value) if inferred_type else (None, value)
    
    @classmethod
    def _convert_scalar(cls, value: Any, target_type: str, source_type: str | None) -> Any | tuple[Any, str]:
        inferred_source_type, extracted_value = cls._parse_iec_literal(value)
        working_value = extracted_value
        source_type = source_type or inferred_source_type
        mapping = TypeRegistry.resolve_type(target_type)
        if not mapping:
            logging.error(f"Unknown type: {target_type}")
            return working_value
        
        canonical_target = TypeRegistry.get_canonical_name(target_type) or target_type
        
        if TypeRegistry.is_generic_type(canonical_target):
            if source_type and TypeRegistry.is_type_compatible(source_type, canonical_target):
                match TypeRegistry.get_category(source_type):
                    case 'integer': return cls._int_converter.convert_to_int(working_value, source_type)
                    case 'float': return cls._float_converter.convert_to_float(working_value, source_type)
                    case 'bool': return cls._bool_converter.convert_to_bool(working_value)
                    case 'string': return cls._string_converter.convert_to_string(working_value)
                    case 'time_date': return cls._timedate_converter.convert_to_time_date(working_value, source_type)
            
            if isinstance(working_value, (bool, int, float)):
                return working_value
            if isinstance(working_value, str):
                try:
                    return float(working_value) if '.' in working_value else int(working_value)
                except (ValueError, TypeError):
                    return working_value
            
            return TypeRegistry.get_default_value(canonical_target)
        
        try:
            match TypeRegistry.get_category(canonical_target):
                case 'bool': return cls._bool_converter.convert_to_bool(working_value)
                case 'integer': return cls._int_converter.convert_to_int(working_value, canonical_target)
                case 'float': return cls._float_converter.convert_to_float(working_value, canonical_target)
                case 'string': return cls._string_converter.convert_to_string(working_value)
                case 'time_date': return cls._timedate_converter.convert_to_time_date(working_value, canonical_target)
                case _:
                    logging.warning(f"No converter for category: {mapping.category}")
                    return working_value
        except Exception as e:
            logging.error(f"Error converting value={working_value!r} to {target_type}: {e}", exc_info=True)
            return TypeRegistry.get_default_value(canonical_target)
    
    @classmethod
    def _parse_string_array(cls, strarr: str) -> list[str]:
        if len(strarr) >= 2:
            inner = strarr[1:-1].strip()
        else:
            return []
        elements = [v.strip() for v in inner.split(',')] if inner else []
        parsed_values = []
        for elem in elements:
            match = re.fullmatch(r'(\d+)\(([^()]+)\)', elem)
            if match:
                count = int(match.group(1))
                val = match.group(2)
                parsed_values.extend([val] * count)
            else:
                parsed_values.append(elem)
        return parsed_values
    
    @classmethod
    def convert(cls, value: Any, target_type: str, source_type: str | None = None) -> Any | tuple[Any, str]:
        if value == '*':
            return None
        canonical_target = TypeRegistry.get_canonical_name(target_type) or target_type
        is_array = canonical_target.startswith('arr_')
        scalar_target = canonical_target[4:] if is_array else canonical_target
        if is_array:
            if isinstance(value, str):
                array_values = cls._parse_string_array(value)
            elif isinstance(value, list):
                array_values = value
        else:
            array_values = value
                         
        if is_array:
            return [cls._convert_scalar(item, scalar_target, source_type) for item in array_values]
        return cls._convert_scalar(value, scalar_target, source_type)
        
UA_TYPES = TypeRegistry.get_ua_types_dict()
XML_4DIAC = TypeRegistry.get_xml_4diac_dict()
UA_NODE = TypeRegistry.get_ua_node_dict()

resource_dir = os.environ.get("OPENFB_LOCAL_DIR") or str(files("openfb.resources"))


def default_folder(ua_peer, obj_idx, obj_path, path_list, folder_name):
    # creates the methods folder
    folder_idx = '{0}.{1}'.format(obj_idx, folder_name)
    browse_name = '2:{0}'.format(folder_name)
    ua_peer.create_folder(obj_path, folder_idx, browse_name)
    folder_list = path_list + [(2, folder_name)]
    return folder_idx, ua_peer.generate_path(folder_list), folder_list


def default_property(ua_peer, obj_idx, obj_path, property_name, property_value):
    prop_idx = f"{obj_idx}.{property_name}"
    browse_name = f"2:{property_name}"
    ua_peer.create_property(obj_path, prop_idx, browse_name, property_value)


def default_object(ua_peer, obj_idx, obj_path, path_list, obj_name):
    browse_name = f"2:{obj_name}"
    ua_peer.create_object(obj_idx, browse_name, path=obj_path)
    new_list = path_list + [(2, obj_name)]
    return new_list, ua_peer.generate_path(new_list)


def parse_fb_description(fb_xml):
    input_events_xml = output_events_xml = input_vars_xml = output_vars_xml = None
    for item in fb_xml:
        if item.tag == 'InterfaceList':
            for interface in item:
                match interface.tag:
                    case 'EventInputs': input_events_xml = interface
                    case 'EventOutput': output_events_xml = interface
                    case 'InputVars': input_vars_xml = interface
                    case 'OutputVars': output_vars_xml = interface
    return input_events_xml, output_events_xml, input_vars_xml, output_vars_xml


def get_fb_files_path(fb_name):
    root_fbs_path = os.path.join(resource_dir, 'function_blocks')
    try:
        fb_name = fb_name.split('::')[-1]
        path = next(scan_match(fb_name, root_fbs_path))
    except Exception:
        logging.error(f"[ERROR] FB does not exist. name {fb_name} path {root_fbs_path}")
        return None

    return path.replace('/__pycache__', '') if "__pycache__" in path else path


def scan_match(fb_name, directory):
    for entry in os.scandir(directory):
        if entry.is_dir():
            yield from scan_match(fb_name, entry.path)
        elif entry.name.split('.')[0] == fb_name:
            yield directory


class UaInterface:
    def from_xml(self, item_xml): raise NotImplementedError
    def from_fb(self, fb, optional_fb_xml): raise NotImplementedError
    def save_xml(self, xml_set): raise NotImplementedError


SIGNED_INT = {'SINT', 'INT', 'DINT', 'LINT'}
UNSIGNED_INT = {'USINT', 'UINT', 'UDINT', 'ULINT'}
BITMASK = {'BYTE', 'WORD', 'DWORD', 'LWORD'}
ALL_INT = SIGNED_INT | UNSIGNED_INT | BITMASK
REAL_T = {'REAL', 'LREAL'}
GENERIC_T = {
    'ANY', 'ANY_ELEMENTARY', 'ANY_MAGNITUDE', 'ANY_NUM',
    'ANY_REAL', 'ANY_INT', 'ANY_UNSIGNED', 'ANY_SIGNED', 
    'ANY_BIT', 'ANY_CHARS', 'ANY_CHAR',
    'ANY_STRING', 'ANY_DATE',
}


def strip_prefix(s: str, prefix: str) -> str:
    return s[len(prefix):] if s.startswith(prefix) else s


def format_concrete_value(ctype: str, val: Any) -> str:
    if isinstance(val, list):
        return f"[{', '.join(format_concrete_value(ctype, v) for v in val)}]"
    match ctype:
        case 'BOOL':
            if isinstance(val, (bool, int, float)):
                return 'TRUE' if val else 'FALSE'            
            return 'TRUE' if str(val).strip().upper() == 'TRUE' else 'FALSE'

        case _ if ctype in ALL_INT:
            try: return str(int(val))
            except (ValueError, TypeError): return str(val)

        case _ if ctype in REAL_T:
            try: return str(float(val))
            except (ValueError, TypeError): return str(val)

        case 'STRING' | 'CHAR': return f"'{val}'"
        case 'WSTRING' | 'WCHAR': return f'"{val}"'

        case 'TIME':
            if isinstance(val, datetime.timedelta): return f"T#{val.total_seconds()}s"
            if isinstance(val, datetime.datetime): return f"T#{val.timestamp()}s"
            return f"T#{strip_prefix(str(val), 'T#')}"

        case 'DATE':
            if isinstance(val, (datetime.datetime, datetime.date)):
                return f"D#{val.year:04d}-{val.month:02d}-{val.day:02d}"
            return f"D#{strip_prefix(str(val), 'D#')}"

        case 'TIME_OF_DAY' | 'TOD':
            if isinstance(val, (datetime.datetime, datetime.time)):
                return f"TOD#{val.hour:02d}:{val.minute:02d}:{val.second:02d}"
            return f"TOD#{strip_prefix(str(val), 'TOD#')}"

        case 'DATE_AND_TIME' | 'DT':
            if isinstance(val, datetime.datetime):
                dt_str = f"{val.year:04d}-{val.month:02d}-{val.day:02d}-{val.hour:02d}:{val.minute:02d}:{val.second:02d}"
                if val.microsecond:
                    dt_str += f".{val.microsecond // 1000:03d}"
                return f"DT#{dt_str}"
            s = str(val)
            for prefix in ('DT#', 'DATE_AND_TIME#'):
                s = strip_prefix(s, prefix)
            return f"DT#{s}"

        case _: return f"'{val}'" if isinstance(val, str) else str(val)


def infer_concrete_type(val: Any) -> str:
    if isinstance(val, bool): return 'BOOL'
    if isinstance(val, datetime.datetime): return 'DATE_AND_TIME'
    if isinstance(val, datetime.date): return 'DATE'
    if isinstance(val, datetime.time): return 'TIME_OF_DAY'
    if isinstance(val, datetime.timedelta): return 'TIME'
    if isinstance(val, float): return 'LREAL'
    if isinstance(val, int):
        if -128 <= val <= 127: return 'SINT'
        if 0 <= val <= 255: return 'USINT'
        if -32768 <= val <= 32767: return 'INT'
        if 0 <= val <= 65535: return 'UINT'
        if -2147483648 <= val <= 2147483647: return 'DINT'
        if 0 <= val <= 4294967295: return 'UDINT'
        return 'LINT' if val < 0 else 'ULINT'
    
    s = str(val)
    if '#' in s:
        match s.split('#', 1)[0].strip().upper():
            case 'T': return 'TIME'
            case 'D': return 'DATE'
            case 'TOD': return 'TIME_OF_DAY'
            case 'DT': return 'DATE_AND_TIME'
    return 'CHAR' if len(s) == 1 else 'STRING'


def infer_any_bit_type(val: Any) -> tuple[str, Any]:
    if isinstance(val, bool): return 'BOOL', val
    if isinstance(val, int):
        if 0 <= val <= 1: return 'BOOL', bool(val)
        if 0 <= val <= 0xFF: return 'BYTE', val
        if 0 <= val <= 0xFFFF: return 'WORD', val
        if 0 <= val <= 0xFFFFFFFF: return 'DWORD', val
        return ('LWORD', val) if 0 <= val <= 0xFFFFFFFFFFFFFFFF else ('LWORD', val & 0xFFFFFFFFFFFFFFFF)

    s = str(val).strip()
    su = s.upper()
    if su in ('TRUE', 'FALSE'): return 'BOOL', su

    if '#' in su:
        pfx, _, rest = su.partition('#')
        if pfx in {'BOOL', 'BYTE', 'WORD', 'DWORD', 'LWORD'}: return pfx, rest
        if pfx == '16':
            try: return infer_any_bit_type(int(rest, 16))
            except ValueError: pass
    try:
        return infer_any_bit_type(int(su, 16) if su.startswith('0X') else int(su))
    except ValueError:
        return 'LWORD', s


def format_value_for_watch(vtype: str, val: Any) -> str:
    if isinstance(val, list):
        return f"[{', '.join(format_value_for_watch(vtype, item) for item in val)}]"
    if vtype == 'ANY_BIT':
        concrete, norm_val = infer_any_bit_type(val)
        return f"{concrete}#{format_concrete_value(concrete, norm_val)}"
    
    if vtype not in GENERIC_T:
        return format_concrete_value(vtype, val)

    concrete = infer_concrete_type(val)
    formatted = format_concrete_value(concrete, val)
    return formatted if concrete in ('TIME', 'DATE', 'TIME_OF_DAY', 'DATE_AND_TIME') else f"{concrete}#{formatted}"