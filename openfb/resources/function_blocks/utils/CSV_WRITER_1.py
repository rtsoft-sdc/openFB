#перепроверить

class CSV_WRITER_1:
    def __init__(self):
        self.file = None
        self.writer = None
        self.filename = None
    
    def schedule(self, event_name, event_value, QI, FILE_NAME=None, SD_1=None):
        if not QI:
            return event_value, False, "QI=False"
        
        if event_name == 'INIT':
            try:
                self.filename = FILE_NAME
                Path(self.filename).parent.mkdir(parents=True, exist_ok=True)
                self.file = open(self.filename, 'a', newline='', encoding='utf-8')
                self.writer = csv.writer(self.file)
                return event_value, True, "OK"
            except Exception as e:
                return event_value, False, f"INIT_ERROR: {e}"
        
        elif event_name == 'REQ':
            if self.writer is None:
                return event_value, False, "NOT_INITIALIZED"
            
            try:
                if isinstance(SD_1, (list, tuple)):
                    row = SD_1
                elif hasattr(SD_1, '__dict__'):
                    row = list(vars(SD_1).values())
                else:
                    row = [SD_1]
                
                self.writer.writerow(row)
                self.file.flush()
                return event_value, True, "OK"
            except Exception as e:
                return event_value, False, f"WRITE_ERROR: {e}"
    
    def __del__(self):
        if self.file and not self.file.closed:
            self.file.close()