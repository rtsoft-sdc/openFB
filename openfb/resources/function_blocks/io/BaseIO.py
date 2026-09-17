import time
import concurrent.futures
from typing import Any, Optional
from openfb.resources.function_blocks.io.AbstractChannel import AbstractChannel

THREAD_POOL = concurrent.futures.ThreadPoolExecutor(max_workers=10)

class BaseIO:
    def __init__(self, datatype: str): # e.g. datatype "IX"
        self.channel: Optional[AbstractChannel] = None
        self.datatype = datatype
        self.address: Any = None
        
        self.QO = False
        self.status = "Created"
        self.output_value = None
        
        self.update_interval = 0.0
        self.delay = 0.0
        self.mode = "sync" # or "ind"
        
        self.start_timestamp = None
        self.last_update_timstamp = None
        self.is_async_running = False
                
    def bind_channel(self, channel: AbstractChannel):
        self.channel = channel
    
    def _init_block(self, QI, PARAMS): # maybe remake (parse_IO_params) for improved versatility
        if not QI or not PARAMS:
            self.QO = False
            self.status = "Disabled"
            return False
        
        self.PARAMS = PARAMS        
        self.address, self.update_interval, self.delay, self.mode, self.status = self.channel.parse_IO_params(PARAMS)
        self.start_timestamp = time.monotonic() + self.delay
        self.QO = True
        self.status = "OK"
        return True
    
    def _check_ready(self, QI):
        if not QI or not self.channel:
            self.QO = False
            self.status = "Not ready"
            return False
        return True
    
    def _should_exec(self):
        now = time.monotonic()
        if self.delay > 0 and self.start_timestamp and (now < self.start_timestamp):
            self.status = "Delayed"
            return False
        
        if self.update_interval > 0:
            if (now - self.last_update_timstamp < self.update_interval):
                self.status = "Waiting"
                return False
        return True
    
    def execute_read(self):
        if not self.QO or not self._should_exec():
            return self.output_value
        
        def _do_read():
            return self.channel.read_data(self.address, self.datatype)
        return self._run_io_task(_do_read)
    
    def execute_write(self, value):
        if not self.QO or not self._should_exec():
            return False
        def _do_write():
            return self.channel.write_data(self.address, value, self.datatype)
        result = self._run_io_task(_do_write)
        return bool(result)
    
    def _run_io_task(self, io_func):
        now = time.monotonic()
        if self.mode == "sync":
            self.last_update_timestamp = now
            try:
                res = io_func()
                self.status = "OK" if res is not None else "IO Error"
                return res
            except Exception as e:
                self.status = f"Error: {str(e)}"
                return None

        elif self.mode == "ind":
            if self.is_async_running:
                self.status = "async running"
                return self.output_value
            
            self.is_async_running = True
            self.last_update_timestamp = now

            def async_task():
                try:
                    res = io_func()
                    if isinstance(res, bool):
                        self.status = "OK" if res else "IO error"
                    elif res is not None:
                        self.output_value = res
                        self.status = "OK"
                except Exception as e:
                    self.status = f"Exception: {str(e)}"
                finally:
                    self.is_async_running = False

            THREAD_POOL.submit(async_task)
            return self.output_value