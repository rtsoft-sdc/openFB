import logging
import struct

class F_LREAL_TO_LWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                f = float(IN)
                return event_value, struct.unpack('Q', struct.pack('d', f))[0]

            except Exception as e:
                logging.error("Error in F_LREAL_TO_LWORD: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_LREAL_TO_LWORD class destroyed')
