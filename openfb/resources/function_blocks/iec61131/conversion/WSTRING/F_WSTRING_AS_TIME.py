import re
from datetime import timedelta

class F_WSTRING_AS_TIME:
    def schedule(self, event_name, event_value, IN):
        if event_name == 'REQ':
            s = str(IN)
            match = re.search(r'T#((?:\d+D)?(?:\d+H)?(?:\d+M)?(?:\d+S)?(?:\d+MS)?(?:\d+US)?(?:\d+NS)?)', s)
            if match:
                time_str = match.group(1)
                td = timedelta()
                if 'D' in time_str:
                    td += timedelta(days=int(re.search(r'(\d+)D', time_str).group(1)))
                if 'H' in time_str:
                    td += timedelta(hours=int(re.search(r'(\d+)H', time_str).group(1)))
                if 'M' in time_str:
                    td += timedelta(minutes=int(re.search(r'(\d+)M', time_str).group(1)))
                if 'S' in time_str:
                    td += timedelta(seconds=int(re.search(r'(\d+)S', time_str).group(1)))
                if 'MS' in time_str:
                    td += timedelta(milliseconds=int(re.search(r'(\d+)MS', time_str).group(1)))
                if 'US' in time_str:
                    td += timedelta(microseconds=int(re.search(r'(\d+)US', time_str).group(1)))
                if 'NS' in time_str:
                    td += timedelta(microseconds=int(re.search(r'(\d+)NS', time_str).group(1)) / 1000)
                return event_value, td
            return event_value, timedelta()

    def __del__(self):
        print('F_WSTRING_AS_TIME class destroyed')
