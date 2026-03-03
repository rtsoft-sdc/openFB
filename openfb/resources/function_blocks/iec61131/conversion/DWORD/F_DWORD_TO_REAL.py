import logging
import struct


class F_DWORD_TO_REAL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                val = int(IN) if not isinstance(IN, int) else IN
                val = val & 0xFFFFFFFF
                result = struct.unpack('f', struct.pack('I', val))[0]
                return event_value, result
            except Exception:
                return event_value, 0.0

    def __del__(self):
        logging.info('F_DWORD_TO_REAL class destroyed')
