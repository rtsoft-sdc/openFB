import struct

class F_LWORD_TO_LREAL:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            val = int(IN) & 0xFFFFFFFFFFFFFFFF
            return event_value, struct.unpack('d', struct.pack('Q', val))[0]
