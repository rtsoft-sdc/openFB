import threading
import logging
import time
import json
import asyncio
from asyncua import Client, ua
import re

# later move to common utils
OPCUA_TYPE_MAPPING = {
    "IX": ua.VariantType.Boolean,
    "IB": ua.VariantType.Byte,
    "IW": ua.VariantType.UInt16,
    "ID": ua.VariantType.UInt32,
    "IL": ua.VariantType.UInt64,
    "IR": ua.VariantType.Float,
    "ILR": ua.VariantType.Double,
    "IStr": ua.VariantType.String,
    "IWStr": ua.VariantType.String,
    
    "QX": ua.VariantType.Boolean,
    "QB": ua.VariantType.Byte,
    "QW": ua.VariantType.UInt16,
    "QD": ua.VariantType.UInt32,
    "QL": ua.VariantType.UInt64,
    "QR": ua.VariantType.Float,
    "QLR": ua.VariantType.Double,
    "QStr": ua.VariantType.String,
    "QWStr": ua.VariantType.String,
}

class SubscriptionHandler:
    def __init__(self, cached_dict) -> None:
        self._cached_dict = cached_dict
        
    def datachange_notification(self, node, val, data):
        node_id = node.nodeid.to_string()
        if node_id in self._cached_dict:
            self._cached_dict[node_id] = val
            logging.info(f"data change notification {node_id}: {val}")
        else:
            logging.info(f"unknown node: {node_id}")

class OpcUaMasterChannel:
    def __init__(self, opcua_client: Client, loop: asyncio.AbstractEventLoop, mode: str = "ind", poll_period: float = 1.0):
        self.opcua_client = opcua_client
        self.loop = loop
        self.subscription = None
        self.subscribed_paths = set()
        self.nodes_cache = {}
        self.cached_values = {}
        self.subscription_handler = SubscriptionHandler(self.cached_values)
        self.path_to_nodeid = {}

        self.is_running = True # true
        self.mode = mode
        self.poll_interval = poll_period
        
    @staticmethod
    def _normalize_node_id(nodeid: str):
        s = nodeid.strip().lstrip(',')
        match  = re.match(r"^(\d+):([isgb]=.+)$", s, re.IGNORECASE)
        if match:
            ns, id = match.groups()
            return f"ns={ns};{id}"
        return s
    
    @staticmethod
    def _is_node_id(path_or_nodeid: str):
        s = path_or_nodeid.strip().lstrip(',')
        return bool(re.match(r"^(ns=\d+;|^\d+:)[isgb]=", s, re.IGNORECASE))

    @staticmethod
    def _parse_browse_path(browse_path: str) -> list:
        parts = [p.strip() for p in str(browse_path).split('/') if p.strip()]
        return [f"0:{p}" if ':' not in p else p for p in parts]

    async def _async_resolve_path(self, browse_path: str):
        if browse_path in self.nodes_cache:
            return self.nodes_cache[browse_path]

        formatted_parts = self._parse_browse_path(browse_path)

        try:
            node = await self.opcua_client.nodes.root.get_child(formatted_parts)
        except Exception:
            if formatted_parts and formatted_parts[0] in ('0:Objects', 'Objects'):
                node = await self.opcua_client.nodes.objects.get_child(formatted_parts[1:])
            else:
                raise

        node_id_str = node.nodeid.to_string()

        self.nodes_cache[browse_path] = node
        self.path_to_nodeid[browse_path] = node_id_str

        logging.info(f"Resolved '{browse_path}' -> Real NodeId: {node_id_str}")
        return node

    async def init_subscription(self):
        if self.mode == "ind" and not self.subscription:
            period_ms = int(self.poll_interval * 1000)
            self.subscription = await self.opcua_client.create_subscription(period_ms, self.subscription_handler)

    def _sync_get_node(self, target_path_or_nodeid: str):
        normalized_target = target_path_or_nodeid.strip()
        if target_path_or_nodeid in self.nodes_cache:
            return self.nodes_cache[target_path_or_nodeid]

        if self._is_node_id(normalized_target): #if ,2:s..
            nodeid = self._normalize_node_id(normalized_target)
            node = self.opcua_client.get_node(nodeid)
            self.nodes_cache[normalized_target] = node
            self.path_to_nodeid[normalized_target] = node.nodeid.to_string() ##
            return node
        
        try:
            future = asyncio.run_coroutine_threadsafe(
                self._async_resolve_path(target_path_or_nodeid), self.loop
            )
            return future.result(timeout=5.0)

        except Exception as e:
            raise

    async def async_get_node(self, node_id):
        if node_id not in self.nodes_cache:
            if self._is_node_id(node_id):
                canon_id = self._normalize_node_id(node_id)
                node = self.opcua_client.get_node(canon_id)
            else:
                node = await self._async_resolve_path(node_id)
            
            self.nodes_cache[node_id] = node
            self.path_to_nodeid[node_id] = node.nodeid.to_string()
            
        return self.nodes_cache[node_id]

    def read_value(self, browse_path: str, block_type: str):
        try:
            node = self._sync_get_node(browse_path)
            node_id_str = self.path_to_nodeid[browse_path]

            if self.mode == "ind":
                if browse_path not in self.subscribed_paths:
                    asyncio.run_coroutine_threadsafe(
                        self._async_subscribe_node(node, browse_path, node_id_str), 
                        self.loop
                    ).result()

                default_val = False if "X" in block_type else 0
                return self.cached_values.get(node_id_str, default_val)
            else:
                future = asyncio.run_coroutine_threadsafe(node.read_value(), self.loop)
                return future.result()

        except Exception as e:
            logging.error(f"Error reading value from node {browse_path}: {e}")
            return False if "X" in block_type else 0

    async def _async_subscribe_node(self, node, browse_path: str, node_id_str: str):
        if not self.subscription:
            period_ms = max(int(self.poll_interval * 1000), 10)
            self.subscription = await self.opcua_client.create_subscription(period_ms, self.subscription_handler)

        await self.subscription.subscribe_data_change(node)
        self.subscribed_paths.add(browse_path)

        val = await node.read_value()
        self.cached_values[node_id_str] = val

    def write_value(self, browse_path: str, value, block_type: str = "QX"):

        try:
            node = self._sync_get_node(browse_path)
            variant_type = OPCUA_TYPE_MAPPING.get(block_type)
            if variant_type is None:
                logging.error(f"Unsupported block type for writing: {value}")
                return False

            data_value = ua.DataValue(ua.Variant(value, variant_type))            
            future = asyncio.run_coroutine_threadsafe(node.write_value(data_value), self.loop)

            if self.mode == "req":
                future.result()  
            return True

        except Exception as e:
            logging.error(f"Error writing value to node {browse_path}: {e}")
            return False

    def stop(self):
        self.is_running = False
