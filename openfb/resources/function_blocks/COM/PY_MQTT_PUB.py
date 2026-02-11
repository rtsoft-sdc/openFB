import logging
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe



class PY_MQTT_SUB:
    def __init__(self) -> None:
        self.port = '' 
        self.ip = ''
        self.topic = ''
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.msg = ''

    def __del__(self):
        # cleanup logic
        logging.debug("Close MQTT connection")
        try:
            self.client.disconnect()
        except Exception:
            logging.error(Exception)

    def schedule(self, event_input_name, event_input_value, QI, MSG, IP, PORT, TOPIC):
        pass