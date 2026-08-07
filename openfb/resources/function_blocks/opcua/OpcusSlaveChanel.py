import threading
import logging
import time
import asyncio
from asyncua import Server, ua

class OpcUaSlaveChannel():
    def __init__(self, opcua_server: Server, loop: asyncio.AbstractEventLoop, namespace_index: int):
        self.channel = opcua_server
        self.loop = loop
        self.namespace_index = namespace_index
        self.is_running = False #
        self.nodes_cached = {}
            
            
    #def _get_node(self, )