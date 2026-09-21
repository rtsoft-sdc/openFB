import re
import logging
import asyncio
import threading
import json
import queue
from asyncua import Client
from openfb.resources.function_blocks.io.flogic.base.OpcuaChannel import OpcUaChannel
from openfb.resources.function_blocks.io.flogic.base.OpcUaChannelAdapter import OpcUaChannelAdapter
from openfb.resources.function_blocks.io.flogic.base.utils import normalize_fb_id
from openfb.resources.function_blocks.io.flogic.base.BaseProtocolFB import BaseProtocolFB


class BaseOpcUAClient(BaseProtocolFB):
    def __init__(self):
        super().__init__()
        self.client_thread = None
        self.loop = None
        self.client = None
        self.queue = queue.Queue()
        self.client_ready_event = threading.Event() 

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
            self.client_ready_event.set() # for not thread blocking
            if self.client:
                try:
                    self.loop.run_until_complete(self.client.disconnect())
                except Exception:
                    pass
            self.loop.close()

    def _execute(self, event_input_name, event_input_value, QI, PARAMS, 
                 io_blocks):
        
        if event_input_name == "MAP":
            if not QI:
                self.stop_channel()
                return event_input_value, None, False, "Disabled"
            try:
                url, mode, poll_period, timeout = self._parse_params(PARAMS)
                self.stop_channel()
                self.client_ready_event.clear()

                self.client_thread = threading.Thread(
                    target=self._run_client_loop,
                    args=(url, mode, poll_period, timeout, self.queue),
                    daemon=True
                )
                self.client_thread.start()
                self.channel = self.queue.get()
                
                if not self.client_ready_event.wait(timeout=timeout + 2.0) or not self.channel:
                    return None, event_input_value, False, f"ERROR: failed to connect {url}"
                
                self.adapter = OpcUaChannelAdapter(self.channel)
                self.bind_and_connect_channels(io_blocks)
                self.status = f"CONNECTED to {url} [{mode.upper()} mode]"
                return event_input_value, None, True, self.status

            except Exception as e:
                self.stop_channel()
                self.status = f"ERROR: {str(e)}"
                return event_input_value, None, False, self.status