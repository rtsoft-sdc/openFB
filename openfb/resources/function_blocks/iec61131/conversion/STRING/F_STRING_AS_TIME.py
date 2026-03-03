import logging
import re
from datetime import timedelta


class F_STRING_AS_TIME:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            try:
                s = str(IN).strip().upper()
                pattern = r'T#((?:\d+D)?(?:\d+H)?(?:\d+M)?(?:\d+S)?(?:\d+MS)?(?:\d+US)?(?:\d+NS)?)'
                match = re.match(pattern, s)
                if not match:
                    return event_value, None
                
                time_str = match.group(1)
                days = hours = minutes = seconds = milliseconds = microseconds = nanoseconds = 0
                
                if 'D' in time_str:
                    days = int(re.search(r'(\d+)D', time_str).group(1))
                if 'H' in time_str:
                    hours = int(re.search(r'(\d+)H', time_str).group(1))
                if 'M' in time_str and 'MS' not in time_str:
                    minutes = int(re.search(r'(\d+)M(?!S)', time_str).group(1))
                if 'S' in time_str and 'MS' not in time_str and 'US' not in time_str and 'NS' not in time_str:
                    seconds = int(re.search(r'(\d+)S(?!$)', time_str).group(1) if re.search(r'(\d+)S(?!$)', time_str) else 0)
                if 'MS' in time_str:
                    milliseconds = int(re.search(r'(\d+)MS', time_str).group(1))
                if 'US' in time_str:
                    microseconds = int(re.search(r'(\d+)US', time_str).group(1))
                if 'NS' in time_str:
                    nanoseconds = int(re.search(r'(\d+)NS', time_str).group(1))
                
                td = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds, 
                            milliseconds=milliseconds, microseconds=microseconds)
                return event_value, td

            except Exception as e:
                logging.error("Error in F_STRING_AS_TIME: %s", str(e))
                return event_value, None
    def __del__(self):
        logging.info('F_STRING_AS_TIME class destroyed')
