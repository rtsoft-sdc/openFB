import threading
import time

class E_CYCLE:
    def __init__(self):
        self.timer = None
        self.is_running = False
        self.dt = None
    
    def schedule(self, event_name, event_value, **kwargs):
        if event_name == 'START':
            dt = kwargs.get('DT')
            if dt is not None:
                # Convert time value to seconds
                if isinstance(dt, str):
                    # Handle TIME format (e.g., "PT1S" for 1 second)
                    dt_seconds = self._parse_time(dt)
                else:
                    dt_seconds = float(dt)
                
                self.dt = dt_seconds
                self.is_running = True
                
                # Start the periodic timer
                self._start_cycle()
                return event_value, None
        
        elif event_name == 'STOP':
            self.is_running = False
            if self.timer is not None:
                self.timer.cancel()
                self.timer = None
            return event_value, None
        
        return event_value, None
    
    def _start_cycle(self):
        """Start the periodic cycle that generates EO events"""
        if self.is_running and self.dt is not None:
            # Schedule the next cycle
            self.timer = threading.Timer(self.dt, self._trigger_cycle)
            self.timer.daemon = True
            self.timer.start()
    
    def _trigger_cycle(self):
        """Trigger the EO event and reschedule if still running"""
        if self.is_running:
            # Trigger EO event - this would be handled by the FB runtime
            self._start_cycle()
    
    @staticmethod
    def _parse_time(time_str):
        """Parse ISO 8601 duration format (e.g., PT1.5S = 1.5 seconds)"""
        import re
        
        # Pattern: PT[n]H[n]M[n]S or combinations
        pattern = r'PT(?:(\d+\.?\d*)H)?(?:(\d+\.?\d*)M)?(?:(\d+\.?\d*)S)?'
        match = re.match(pattern, time_str)

        if not match:
            return 1.0  # Default 1 second
        
        hours = float(match.group(1) or 0)
        minutes = float(match.group(2) or 0)
        seconds = float(match.group(3) or 0)
        
        return hours * 3600 + minutes * 60 + seconds
