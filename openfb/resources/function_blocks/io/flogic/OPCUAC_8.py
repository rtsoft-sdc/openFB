import re
from openfb.resources.function_blocks.io.flogic.OpcuaChannel import OpcUaChannel
from openfb.resources.function_blocks.io.flogic.OpcUaChannelAdapter import OpcUaChannelAdapter
from openfb.resources.function_blocks.io.flogic.utils import normalize_fb_id
import logging
import asyncio
import time
import threading
import json
from openfb.resources.function_blocks.io.flogic.utils import normalize_IO_fb_id
from asyncua import Client, ua
import queue


class OPCUAC_8:
    def __init__(self):
        self.channel = None
        self.fb_registry = None
        self.client_thread = None
        self.loop = None
        self.client = None
        self.status = "Created"
        self.queue = queue.Queue()
        self.client_ready_event = threading.Event()
        self.adapter = None
        self.address = None
        self.fb_name = ""
        self.fb_prefix = ""

    def set_fb_registry_and_name(self, fb_registry, fb_name):
        self.fb_registry = fb_registry
        self.fb_name = str(fb_name)
        self.fb_prefix = self.fb_name.rpartition('.')[0] + "."
        
    def _find_fb_object(self, ioblock_id):
        if not self.fb_registry:
            return None
        targetid = self.fb_prefix + normalize_fb_id(ioblock_id)
        if not targetid:
            return None
        for val in self.fb_registry.values():
            fb_name = getattr(val, "fb_name", '')
            if fb_name == targetid:
                return getattr(val, 'fb_obj', None)
        return None    

    def _parse_params(self, params_raw: str):
        default_url = "opc.tcp://127.0.0.1:4840"
        default_mode = "async"
        default_poll = 0.1
        default_timeout = 5.0

        if not params_raw:
            return default_url, default_mode, default_poll, default_timeout

        if isinstance(params_raw, dict):
            return (
                params_raw.get("url", default_url),
                params_raw.get("mode", default_mode),
                float(params_raw.get("poll_period", default_poll)),
                float(params_raw.get("timeout", default_timeout))
            )

        params_str = str(params_raw).strip()

        if params_str.startswith("opc.tcp://"):
            return params_str, default_mode, default_poll, default_timeout

        try:
            data = json.loads(params_str)
            if isinstance(data, dict):
                return (
                    data.get("url", default_url),
                    data.get("mode", default_mode),
                    float(data.get("poll_period", default_poll)),
                    float(data.get("timeout", default_timeout))
                )
        except Exception:
            pass

        match = re.search(r"opc\.tcp://[^\s'\"}]+", params_str)
        if match:
            extracted_url = match.group(0)
            logging.warning(f"Extracted URL '{extracted_url}' from malformed PARAMS: '{params_str}'")
            return extracted_url, default_mode, default_poll, default_timeout

        logging.error(f"Failed to parse PARAMS '{params_raw}', using default URL '{default_url}'")
        return default_url, default_mode, default_poll, default_timeout

    def _run_client_loop(self, url: str, mode: str, poll_period: float, timeout: float, queue: queue.Queue):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.client = Client(url=url, timeout=timeout)

        async def setup_and_connect():
            await self.client.connect()
            queue.put(
                OpcUaChannel(
                opcua_client=self.client, 
                loop=self.loop, 
                mode=mode, 
                poll_period=poll_period)
            )
            self.client_ready_event.set()
        try:
            self.loop.run_until_complete(setup_and_connect())
            self.loop.run_forever()
        except Exception as e:
            logging.error(f"[OPC UA Master Thread] Connection error to {url}: {e}")
            self.status = f"ERROR: {str(e)}"
        finally:
            self.client_ready_event.set() # Сигнализируем в случае ошибки, чтобы не заблокировать поток
            if self.client:
                try:
                    self.loop.run_until_complete(self.client.disconnect())
                except Exception:
                    pass
            self.loop.close()

    def _stop_channel(self):
        if self.adapter:
            try:
                self.adapter.stop()
            except Exception as e:
                logging.error(f"Adapter stop error: {e}")
            self.adapter = None
            
        if self.channel:
            try:
                self.channel.stop()
            except Exception as e:
                logging.error(f"Channel stop error: {e}")
            self.channel = None

        if self.loop and self.loop.is_running():
            self.loop.call_soon_threadsafe(self.loop.stop)

        if self.client_thread and self.client_thread.is_alive():
            self.client_thread.join(timeout=2)

        self.client_thread = None
        self.loop = None
        self.client = None
        self.client_ready_event.clear()
        self.status = "STOPPED"

    def schedule(self, event_input_name, event_input_value, QI, PARAMS, 
                 IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7):
        
        if event_input_name == "MAP":

            if not QI:
                self._stop_channel()
                return event_input_value, None, False, "Disabled"

            try:
                url, mode, poll_period, timeout = self._parse_params(PARAMS)
                
                self._stop_channel()
                self.client_ready_event.clear()

                self.client_thread = threading.Thread(
                    target=self._run_client_loop,
                    args=(url, mode, poll_period, timeout, self.queue),
                    daemon=True
                )
                self.client_thread.start()
                self.channel = self.queue.get()
                
                if not self.client_ready_event.wait(timeout=timeout + 2.0) or not self.channel:
                    print(f"[ERROR] OPC UA Master failed to connect to {url} within timeout.")
                    return None, event_input_value, False, f"ERROR: failed to connect {url}"
                
                self.adapter = OpcUaChannelAdapter(self.channel)
                                
                io_list = [IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7]
                for io_block in io_list:
                    if not io_block:
                        continue

                    fb_obj = self._find_fb_object(io_block)
                    if fb_obj and hasattr(fb_obj, 'bind_channel'):
                        try:
                            fb_obj.bind_channel(self.adapter)
                        except Exception as e:
                            logging.error(f"opcua error:{e}")

                print(f"CONNECTED to {url} [{mode.upper()} mode]")
                self.status = f"OK"
                return event_input_value, None, True, self.status

            except Exception as e:
                self._stop_channel()
                self.status = f"ERROR: {str(e)}"
                return event_input_value, None, False, self.status

    def __del__(self):
        self._stop_channel()