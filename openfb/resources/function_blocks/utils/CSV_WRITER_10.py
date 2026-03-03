import csv
import logging
from pathlib import Path
import os


class CSV_WRITER_10:
    def __init__(self):
        self.file = None
        self.writer = None
        self.filename = None

    def _get_error_message(self, exc):
        """Get error message from exception"""
        if isinstance(exc, OSError):
            return os.strerror(exc.errno)
        return str(exc)
    
    def schedule(self, event_name, event_value, QI, FILE_NAME, SD_1, SD_2, SD_3, SD_4, SD_5, SD_6, SD_7, SD_8, SD_9, SD_10):
        if event_name == 'INIT':
            try:
                if QI:
                    if self.file is not None and not self.file.closed:
                        return event_value, None, False, "File already opened"

                    self.filename = FILE_NAME
                    Path(self.filename).parent.mkdir(parents=True, exist_ok=True)
                    self.file = open(self.filename, 'a', newline='', encoding='utf-8')
                    self.writer = csv.writer(self.file)
                    return event_value, None, True, "OK"
                else:
                    if self.file is not None and not self.file.closed:
                        self.file.close()
                    self.file = None
                    self.writer = None
                    return event_value, None, False, "OK"
            except OSError as e:
                return event_value, None, False, self._get_error_message(e)
            except Exception as e:
                return event_value, None, False, str(e)
        
        elif event_name == 'REQ':
            try:
                if QI:
                    if self.writer is None:
                        return None, event_value, False, "File not opened"

                    row = [SD_1, SD_2, SD_3, SD_4, SD_5, SD_6, SD_7, SD_8, SD_9, SD_10]
                    self.writer.writerow(row)
                    self.file.flush()
                    return None, event_value, True, "OK"
                else:
                    return None, event_value, False, "OK"
            except OSError as e:
                return None, event_value, False, self._get_error_message(e)
            except Exception as e:
                return None, event_value, False, str(e)
            
    def __del__(self):
        logging.info('CSV_WRITER class destroyed')
        if self.file and not self.file.closed:
            self.file.close()
