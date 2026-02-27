import struct

class F_LREAL_TO_LWORD:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            f = float(IN)
            return event_value, struct.unpack('Q', struct.pack('d', f))[0]
