import datetime
import logging
import time

class TIMESTAMP_NS:
    def schedule(self, event_name, event_value, startDate):
        if event_name == 'REQ':
            if isinstance(startDate, str):
                date_str = startDate.replace('DT#', '')
                try:
                    start_dt = datetime.datetime.strptime(date_str, '%Y-%m-%d-%H:%M:%S')
                except:
                    logging.error("Invalid date format for startDate: %s", startDate)
                    return event_value, None
            elif isinstance(startDate, datetime.datetime):
                start_dt = startDate
            else:
                return event_value, None
            
            current_time = datetime.datetime.now()
            time_diff = current_time - start_dt
            timestamp_ns = int(time_diff.total_seconds() * 1_000_000_000)
            
            return event_value, timestamp_ns

    def __del__(self):
        logging.info('class destroyed')
