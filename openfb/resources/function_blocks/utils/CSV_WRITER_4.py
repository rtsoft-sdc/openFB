import csv
from pathlib import Path
import logging


class CSV_WRITER_4:
    def __init__(self):
        self.file = None
        self.writer = None
        self.filename = None
    
    def schedule(self, event_name, event_value, QI, FILE_NAME, SD_1, SD_2, SD_3, SD_4):
        if event_name == 'INIT':
            if not QI:
                if self.file and not self.file.closed:
                    self.file.close()
                    self.file = None
                    self.writer = None
                return event_value, None, False, "QI=False"
            
            try:
                self.filename = FILE_NAME
                Path(self.filename).parent.mkdir(parents=True, exist_ok=True)
                if self.file and not self.file.closed:
                    self.file.close()
                self.file = open(self.filename, 'a', newline='', encoding='utf-8')
                self.writer = csv.writer(self.file)
                return event_value, None, True, "OK"
            except Exception as e:
                return event_value, None, False, f"INIT_ERROR: {e}"
        
        elif event_name == 'REQ':
            if not QI:
                return None, event_value, False, "QI=False"
            
            if self.writer is None:
                return None, event_value, False, "NOT_INITIALIZED"
            
            try:
                row = [SD_1, SD_2, SD_3, SD_4]
                self.writer.writerow(row)
                self.file.flush()
                return None, event_value, True, "OK"
            except Exception as e:
                return None, event_value, False, f"WRITE_ERROR: {e}"
            
    def __del__(self):
        logging.info('CSV_WRITER class destroyed')
        if self.file and not self.file.closed:
            self.file.close()
