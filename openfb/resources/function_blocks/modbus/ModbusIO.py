import logging
from openfb.resources.function_blocks.modbus.utils import parse_register_value, get_addr_update_delay_mode
import concurrent.futures
import time

logger = logging.getLogger(__name__)

THREAD_POOL = concurrent.futures.ThreadPoolExecutor(max_workers=10)

class ModbusIO:
    
    def __init__(self):
        self.channel = None
        self.unit_id = 1
        self.register_value = None
        self.register_type = None
        self.QO = False
        self.status = "Created"
        self.updated = False
        self.output_value = None
        
        self.update_interval = 0
        self.delay = 0
        self.mode = "ind"
        
        self.start_timestamp = None
        self.last_update_timestamp = None
        self.is_async_running = False

    def bind_channel(self, channel):
        self.channel = channel
        
    def update_register(self, params):
        new_register_type, new_register_value = parse_register_value(params)
        
        if new_register_type is None or new_register_value is None:
            self.QO = False
            self.status = f"Invalid PARAMS: {params}"
            return False
        
        is_initial = self.register_value is None
        if (self.register_type, self.register_value) != (new_register_type, new_register_value):
            if not is_initial:
                self.updated = True
            self.register_type, self.register_value = new_register_type, new_register_value
            
        self.QO = True
        self.status = "OK"
        return True  
        
    def _init_block(self, QI, PARAMS):
        if not QI or not PARAMS:
            self.QO = False
            self.status = "Disabled"
            return False

        if self.channel is None:
            self.QO = False
            self.status = "Channel not bound"
            return False

        register, self.update_interval, self.delay, self.mode, self.status = get_addr_update_delay_mode(PARAMS)
        ###
        if register is None:
            register = PARAMS
        ###
        if not register:
            return False
        self.register_type, self.register_value = parse_register_value(register)
        self.start_timestamp = time.time() + self.delay
        return self.update_register(register)

    def _check_ready(self, QI):
        if not QI:
            self.status = "Disabled"
            return False
        if self.channel is None:
            self.status = "Not initialized"
            return False
        return True
    
    def _should_exec(self):
        now = time.monotonic()
        if self.delay == 0 and self.update_interval == 0:
            return True
        if self.start_timestamp is not None and (now - self.start_timestamp < self.delay):
            self.status = "delayed"
            return False
        
        if self.update_interval > 0:
            if (now - self.last_update_timestamp) < self.update_interval:
                self.status = "waiting"
                return False
        return True
    
    def exec_io(self, io_func, *args, **kwargs):
        if not self.QO:
            self.status = "Not ready"
            return None
        if not self._should_exec():
            return self.output_value
        
        now = time.monotonic()
        if self.mode == "sync":
            self.last_update_timestamp = now
            return io_func(*args, **kwargs)
            
        elif self.mode == "ind":
            if self.is_async_running:
                self.status = "async running"
                return self.output_value
            self.is_async_running = True
            self.last_update_timestamp = now
            def async_task():
                try:
                    result = io_func(*args, **kwargs)
                    if isinstance(result, bool):
                        self.status = "OK" if result else "IO error"
                        self.output_value = result
                    elif result is not None:
                        self.output_value = result
                        self.status = "OK"
                except Exception as e:
                    self.status = f"Exception: {str(e)}"
                finally:
                    self.is_async_running = False
            THREAD_POOL.submit(async_task)
            return self.output_value
        
        return None