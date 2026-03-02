import datetime
import time

class TIMESTAMP_NS:
    def schedule(self, event_name, event_value, startDate):
        if event_name == 'REQ':
            if isinstance(startDate, str):
                date_str = startDate.replace('DT#', '')
                try:
                    start_dt = datetime.datetime.strptime(date_str, '%Y-%m-%d-%H:%M:%S')
                except:
                    start_dt = datetime.datetime(1970, 1, 1, 0, 0, 0)
            elif isinstance(startDate, datetime.datetime):
                start_dt = startDate
            else:
                start_dt = datetime.datetime(1970, 1, 1, 0, 0, 0)
            
            current_time = datetime.datetime.now()
            time_diff = current_time - start_dt
            timestamp_ns = int(time_diff.total_seconds() * 1_000_000_000)
            
            return event_value, timestamp_ns

    def __del__(self):
        print('class destroyed')
