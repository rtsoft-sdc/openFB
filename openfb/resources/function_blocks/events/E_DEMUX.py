class E_DEMUX:
    def schedule(self, event_name, event_value, K):
        if event_name == 'EI' and K in range(4):
            return tuple(event_value if i == K else None for i in range(4))
    
    def __del__(self):
        print('E_DEMUX class destroyed')