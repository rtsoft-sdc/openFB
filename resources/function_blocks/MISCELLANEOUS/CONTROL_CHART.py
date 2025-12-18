import numpy as np
import time

class CONTROL_CHART:

    def schedule(self, event_name, event_value, range, value):

        if event_name == 'INIT':
            self.state = 0
            if range is None:
                print("You should define a range for the Control Chart")
            else:
                self.min_range, self.max_range = str(range).split("-")

            return [event_value, None, None]

        elif event_name == 'RUN':

            if range is None:
                print("You should define a range for the Control Chart")
            else:
                self.min_range, self.max_range = str(range).split("-")

            if float(value) > float(self.max_range):
                return [None, event_value, "1"]
            elif float(value) < float(self.min_range):
                return [None, event_value, "-1"]
            else:
                return [None, event_value, "0"]