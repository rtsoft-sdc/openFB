import logging
import struct

class F_REAL_TO_DWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                f = float(IN)
                return event_value, struct.unpack('I', struct.pack('f', f))[0]

            except Exception as e:
                logging.error("Error in F_REAL_TO_DWORD: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_REAL_TO_DWORD class destroyed')
