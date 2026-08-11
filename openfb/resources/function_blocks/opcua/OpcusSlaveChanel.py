import os
import threading
import logging
import time
import asyncio
from asyncua import Server, ua
from dataclasses import dataclass, field

# @dataclass
# class MinAndMax:
#     min: int
#     max: int
    
#     @classmethod
#     def from_dict(cls, config, default_min=0, default_max=0):
#         if not isinstance(config, dict):
#             config = {}
#         return cls(
#             min=config.get("min", default_min),
#             max=config.get("max", default_max)
#         )

@dataclass
class TCPConfig:
    tcpBufSize: int = 65536
    tcpMaxMsgSize: int = 16777216
    tcpMaxChunks: int = 32
    
    @classmethod
    def from_dict(cls, config):
        return cls(
            tcpBufSize=config.get("tcpBufSize", 65536),
            tcpMaxMsgSize=config.get("tcpMaxMsgSize", 16777216),
            tcpMaxChunks=config.get("tcpMaxChunks", 32)
        )
###################################################################################
#define later
###################################################################################        
@dataclass
class SubscriptionConfig:
    maxSubscriptions: int
    maxSubscriptionPerSession: int
    publishingIntervalLimits: list
    lifeTimeCountLimits: list
    keepAliveCountLimits: list
    maxNotificationsPerPublish: int
    enableRetransmissionQueue: bool
    maxRetransmissionQueueSize: int
    maxEventsPerNode: int #######################################
    maxMonitoredItems: int
    maxMonitoredItemsPerSubscription: int
    samplingIntervalLimits: list
    queueSizeLimits: list
    maxPublishReqPerSession: int
     
    @classmethod 
    def from_dict(cls, config):
        return cls(
            maxSubscriptions=config.get("maxSubscriptions", 100),
            maxSubscriptionPerSession=config.get("maxSubscriptionPerSession", 10),
            publishingIntervalLimits=config.get("publishingIntervalLimits", [100, 10000]),
            lifeTimeCountLimits=config.get("lifeTimeCountLimits", [1, 100]),
            keepAliveCountLimits=config.get("keepAliveCountLimits", [1, 100]),
            maxNotificationsPerPublish=config.get("maxNotificationsPerPublish", 100),
            enableRetransmissionQueue=config.get("enableRetransmissionQueue", True),
            maxRetransmissionQueueSize=config.get("maxRetransmissionQueueSize", 100),
            maxEventsPerNode=config.get("maxEventsPerNode", 10),
            maxMonitoredItems=config.get("maxMonitoredItems", 1000),
            maxMonitoredItemsPerSubscription=config.get("maxMonitoredItemsPerSubscription", 100),
            samplingIntervalLimits=config.get("samplingIntervalLimits", [10, 60000]),
            queueSizeLimits=config.get("queueSizeLimits", [1, 100]),
            maxPublishReqPerSession=config.get("maxPublishReqPerSession", 10)
        )
    
@dataclass
class SecurityConfig:
    pkiStore: str
    encryptionOn: bool
    authAnonymous: bool
    authCertificate: bool
    authPassword: bool
    userName: str
    passwordHash: str
    
    @staticmethod
    def from_dict(config):
        return SecurityConfig(
            pkiStore=config.get("pkiStore", "./pki"),
            encryptionOn=config.get("encryptionOn", True),
            authAnonymous=config.get("authAnonymous", True),
            authCertificate=config.get("authCertificate", False),
            authPassword=config.get("authPassword", False),
            userName=config.get("userName", ""),
            passwordHash=config.get("passwordHash", "")
        )
    
@dataclass
class ServerConfig:
    serverUrls: list
    tcpEnabled: bool
    tcp: TCPConfig = field(default_factory=TCPConfig)
    
    maxSecureChannels: int
    maxSecureTokenLifetime: int
    maxSessions: int
    maxSessionTimeout: int
    subscriptionEnabled: bool
    
    subscription: SubscriptionConfig = field(default_factory=SubscriptionConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    
    @classmethod
    def load_config(cls, filename):
        try:
            import json
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls(
                serverUrls=data.get("serverUrls", []),
                tcpEnabled=data.get("tcpEnabled", True),
                tcp=TCPConfig.from_dict(data.get("tcp", {})),
                maxSecurityChannels=data.get("maxSecurityChannels", 10),
                maxSecureTokenLifetime=data.get("maxSecureTokenLifetime", 60000),
                maxSessions=data.get("maxSessions", 100),
                maxSessionTimeout=data.get("maxSessionTimeout", 3600000),
                subscriptionEnabled=data.get("subscriptionEnabled", True),
                
                subscription=SubscriptionConfig(**data.get("subscription", {})),
                security=SecurityConfig(**data.get("security", {}))
            )
        except Exception as e:
            logging.error(f"Failed to load server configuration: {e}")
            return cls()
        


class ServerConfigManager:
    def __init__(self, config: ServerConfig):
        self.config = config
        self.server = Server()
        
    async def setup(self):
        if not self.config.tcpEnabled:
            logging.warning("TCP is disabled in the server configuration.")
            return
        await self.server.init()
        for url in self.config.serverUrls:
            self.server.set_endpoint(url)
            logging.info(f"server endpoint set: {url}")
            

        self.server.limits.max_message_size = self.config.tcp.tcpMaxMsgSize
        self.server.limits.max_chunk_count = self.config.tcp.tcpMaxChunks
        self.server.limits.max_recv_buffer = self.config.tcp.tcpBufSize
        self.server.limits.max_send_buffer = self.config.tcp.tcpBufSize

        self.server.iserver.max_connections = self.config.maxSecureChannels
        self.server.iserver.isession.max_connections = self.config.maxSessions

        self.server.iserver.max_session_timeout_ms = self.config.maxSessionTimeout
        
        subscription_config = self.config.subscription
        self.server.iserver.max_subscriptions = subscription_config.maxSubscriptions
        self.server.iserver.max_lifetime_count = subscription_config.lifeTimeCountLimits.max
        self.server.iserver.max_keep_alive_count = subscription_config.keepAliveCountLimits.max
        self.server.iserver.max_unacked_messages_per_subscription = subscription_config.maxRetransmissionQueueSize        
        self.server.iserver.max_monitored_item_queue_size = subscription_config.queueSizeLimits.max

        
        security_config = self.config.security
        policies = []
        if security_config.encryptionOn:
            cert_path = os.path.join(security_config.pkiStore, "server_cert.pem")
            key_path = os.path.join(security_config.pkiStore, "server_key.pem")
            if os.path.exists(cert_path) and os.path.exists(key_path):
                await self.server.load_certificate(cert_path)
                await self.server.load_private_key(key_path)
                policies.extend([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt, ua.SecurityPolicyType.Basic256Sha256_Sign])
            else:
                policies.append(ua.SecurityPolicyType.NoSecurity)
        else:
            policies.append(ua.SecurityPolicyType.NoSecurity)
            
        self.server.set_security_policy(policies)
        
    def user_manager(self, iserver, user_name, password, certificate) -> bool:
        auth_creds = self.config.security
        if auth_creds.authAnonymous:
            return True
        
        if auth_creds.userName and auth_creds.passwordHash:
            if user_name == auth_creds.userName and password == auth_creds.passwordHash:
                return True
            