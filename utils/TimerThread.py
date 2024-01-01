
import threading
import time

class TimerThread(threading.Thread):
    def __init__(self, interval, function):
        super().__init__()
        # set the thread as daemon
        self.daemon = True
        self.function = function
        self.interval = interval
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            time.sleep(self.interval)
            self.function()

