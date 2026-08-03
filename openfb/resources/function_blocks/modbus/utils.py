import json
import ast
import re

def normalize_fb_id(raw_id) -> str:
    if not raw_id and not isinstance(raw_id, str):
        return ""
    s = raw_id.strip()
    if s.startswith("."):
        s = s[1:]
        # mayabe need to remove other dots
    return s


def parse_register_value(params) -> tuple[str, int]:
    params = str(params).lower()
    if params.isdigit():
        return 'h', int(params)
    match = re.match(r'([hidc])(\d+)', params)
    if match:
        register_type, register_value = match.groups()
        return register_type, int(register_value)
    return None, None
    

def parse_input_data_string(data_string):
    data_string = str(data_string).strip()
    data = {}

    try:
        data = json.loads(data_string)
    except Exception:
        try:
            cut_str = data_string.strip("{}")
            for pair in cut_str.split(","):
                if ":" in pair:
                    key, val = pair.split(":", 1)
                    data[key] = val
        except Exception:
            data = None # somehow need to return parameters with none value
    if not isinstance(data, dict):
        data = None

    host_port = data.get("host", "")
    if ':' in host_port:
        host, port_str = host_port.split(':', 1)
        port = int(port_str)
    elif host_port:
        host = host_port
        port = 502
    else:
        host, port = None, None
        
    unit_id = int(data.get("id", 1))

    return host, port, unit_id


def parse_time_to_seconds(time_str):
    time_str = str(time_str).strip().lower()
    if time_str.isdigit():
        time_str += "mks"
    frequency = re.match(r"^([\d\.]+)\s*(hz|khz)$", time_str)
    if frequency:
        value, unit = frequency.groups()
        value = float(value)
        if unit == "hz":
            return 1.0 / value
        elif unit == "khz":
            return 1.0 / (value * 1000)
    else:
        time_match = re.match(r"^([\d\.]+)\s*(mks|ms|s)$", time_str)
        if time_match:
            value, unit = time_match.groups()
            value = float(value)
            if unit == "mks":
                return value / 1000000.0
            elif unit == "ms":
                return value / 1000.0
            elif unit == "s":
                return value
    return None