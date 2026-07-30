import json
import ast

def normalize_fb_id(raw_id) -> str:
    if not raw_id and not isinstance(raw_id, str):
        return ""
    s = raw_id.strip()
    if s.startswith("."):
        s = s[1:]
        # mayabe need to remove other dots
    return s


def parse_io_params(params): #startswith c-coil reg, h-holding reg, i-input reg, d-discrete input, without letter - deafult h
    
    if params.startswith('c'):
        addr, register = int(params[1:]), 'c'
    elif params.startswith('i'):
        addr, register = int(params[1:]), 'i'
    elif params.startswith('d'):
        addr, register = int(params[1:]), 'd'
    else:
        addr, register = int(params[1:]), 'h'
        
    return addr, register


def parse_input_data_string(data_string):
    data_string = str(data_string).strip()
    data = {}

    try:
        data = json.loads(data_string)
    except Exception:
        try:
            data = ast.literal_eval(data_string)
        except Exception:
            clean_str = data_string.strip("{}")
            for pair in clean_str.split(","):
                if ":" in pair:
                    key, val = pair.split(":", 1)
                    clean_key = key.strip().strip("'\"")
                    clean_val = val.strip().strip("'\"")
                    data[clean_key] = clean_val

    if not isinstance(data, dict):
        raise ValueError(f"Не удалось распознать формат PARAMS: '{data_string}'")

    host_port = data.get("host", "")
    if ':' in host_port:
        host, port_str = host_port.split(':', 1)
        port = int(port_str)
    else: #maybe no need and raise error
        host = host_port if host_port else "127.0.0.1"
        port = 502  # default
        
    unit_id = int(data.get("id", 1))

    return host, port, unit_id