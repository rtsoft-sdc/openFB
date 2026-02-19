import threading
import time

class E_RDELAY:
        def __init__(self):
            self._timer = None
            self._callback = None
            self._event_value = None

        def schedule(self, event_name, event_value, DT, callback=None):

            if event_name == 'START':
                self._event_value = event_value
                self._callback = callback
                if self._timer:
                    self._timer.cancel()
                self._timer = threading.Timer(DT, self._on_timeout)
                self._timer.start()
            elif event_name == 'STOP':
                if self._timer:
                    self._timer.cancel()
                    self._timer = None
            return None

        def _on_timeout(self):
            if self._callback:
                self._callback(self._event_value)
            self._timer = None

''' import asyncio
    class E_RDELAY:
        def __init__(self):
            self._task = None
            self._event_value = None
            self._callback = None
    
        async def schedule(self, event_name, event_value, DT, callback=None):
            self._event_value = event_value
            self._callback = callback
            if event_name == 'START':
                if self._task and not self._task.done():
                    self._task.cancel()
                self._task = asyncio.create_task(self._delay(DT))
            elif event_name == 'STOP':
                if self._task and not self._task.done():
                    self._task.cancel()
    
        async def _delay(self, DT):
            try:
                await asyncio.sleep(DT)
                if self._callback:
                    self._callback(self._event_value)
            except asyncio.CancelledError:
                pass
'''