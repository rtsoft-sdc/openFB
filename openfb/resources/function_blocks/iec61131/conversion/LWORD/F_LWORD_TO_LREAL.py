import logging
import struct

class F_LWORD_TO_LREAL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN) & 0xFFFFFFFFFFFFFFFF
                return event_value, struct.unpack('d', struct.pack('Q', val))[0]

            except Exception as e:
                logging.error("Error in F_LWORD_TO_LREAL: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_LWORD_TO_LREAL class destroyed')
