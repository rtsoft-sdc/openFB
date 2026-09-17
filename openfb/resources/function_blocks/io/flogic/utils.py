import json
import re

def normalize_fb_id(raw_id) -> str:
    if raw_id is None or raw_id.strip() == "":
        return ""
    block_name = raw_id.split(".")[-1]
    return block_name


def parse_register_value(params):
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
                    key = key.strip()
                    val = val.strip()
                    if val.isdigit():
                        val = int(val)
                    data[key] = val
        except Exception:
            data = None
    if not isinstance(data, dict):
        data = None

    return data

def get_host_port_unitid(data):
    input_data = parse_input_data_string(data)
    if input_data is None:
        status = "Invalid PARAMS"
        return None, None, None, status
                    
    if input_data.get("host") is not None:
        host = input_data.get("host", "")
        if ":" in host:
            host, port_str = host.split(":", 1)
            port = int(port_str)
        elif input_data.get("port") is not None:
            port = int(input_data.get("port", None))
        else:
            status = "Invalid PARAMS: Missing port"
            return None, None, None, status
                    
    unit_id = int(input_data.get("id", 1))
    return host, port, unit_id, "OK"

def get_addr_update_delay_mode(data):
    input_data = parse_input_data_string(data)
    if input_data is None:
        status = "Invalid PARAMS"
        return None, None, None, None, None, status

    address = input_data.get("addr")
    update_interval_str = input_data.get("update", "")
    start_delay_str = input_data.get("delay", "")
    mode = input_data.get("mode", "ind")

    update_interval = parse_time_to_seconds(update_interval_str) if update_interval_str else 0
    start_delay = parse_time_to_seconds(start_delay_str) if start_delay_str else 0

    return address, update_interval, start_delay, mode, "OK"

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


def normalize_IO_fb_id(raw_id) -> str:
    if raw_id is None or raw_id.strip() == "":
        return ""
    block_name = raw_id.split(".")[1]
    return block_name
    

def OPC_parse_input_data_string(data_string):
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
                    key = key.strip()
                    val = val.strip()
                    if val.isdigit():
                        val = int(val)
                    data[key] = val
        except Exception:
            data = None
    if not isinstance(data, dict):
        data = None

    return data