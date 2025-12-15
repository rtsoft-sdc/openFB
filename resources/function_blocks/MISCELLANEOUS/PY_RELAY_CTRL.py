import os 
import sys
import logging
from time import sleep

import pyhid_usb_relay as usbr



class PY_RELAY_CTRL:
    def __init__(self) -> None:
        self.relay = None

    def __del__(self):
        del self.relay

    def schedule(self, event_input_name, event_input_value, REL_NUM, STATE_ON):
        'Write your code here.'
        if event_input_name == 'INIT':
            num = 0
            state = "Relay connected"
            try:
                self.relay = usbr.find()
            except usbr.exceptions.DeviceNotFoundError:
                 self.relay = None
                 state = "Relay not found"
            
            if self.relay is not None:
                num = self.relay.num_relays

            return event_input_value, None, num, state 
        
        if event_input_name == 'REQ':
            state = "No relay"
            if self.relay is not None and REL_NUM is not None:
                if REL_NUM > self.relay.num_relays:
                    state = "Selected relay doesn't exist"
                elif REL_NUM <=0:
                    state = "Nums relay in range: [1 ... %d]" % self.relay.num_relays
                else:
                    if STATE_ON == self.relay[REL_NUM]:
                        rel_state = "enabled" if STATE_ON else "disabled"
                        state = f"Relay: {REL_NUM} is already {rel_state}"
                    else:
                        rel_state = "Enable" if STATE_ON else "Disable"
                        state = f"{rel_state} relay {REL_NUM}"
                        self.relay[REL_NUM] = STATE_ON
            else:
                state = "somehting wrong"
            return None, event_input_value+1, None, state