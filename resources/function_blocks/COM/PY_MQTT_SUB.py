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

    def on_message(self, userdata, msg):
        content = str(msg.payload)
        logging.error(msg.topic+" "+content)
        self.msg = msg.payload.decode()
        self.client.disconnect()  # Disconnect after receiving the first message


    def schedule(self, event_input_name, event_input_value, QI, IP, PORT, TOPIC):
        'Write your code here.'
        status = "Idle"
        message = ''
        if event_input_name == 'INIT':
            "Write your handler for current event here."
            self.ip = IP
            self.port = int(PORT)
            self.topic = TOPIC
            # self.client.connect(self.ip, self.port)
            # self.client.subscribe(self.topic)
            # self.client.on_message = self.on_message
            status = 'Configured'
          
            return 1, event_input_value, QI, status, message

        elif event_input_name == 'REQ':
            "Write your handler for current event here."
            if QI == True:
                logging.error("I'M HERE GUYS")
                msg = subscribe.simple(self.topic,  port=self.port, msg_count=1, hostname=self.ip)
                message = msg.payload.decode()
                logging.error(message)
                status = "Received"
                return None, event_input_value, QI, status, message
            else:
                return None, event_input_value, QI, status, message
