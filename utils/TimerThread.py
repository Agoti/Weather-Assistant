# TimerThread.py
# Description: a timer thread, which executes a function every interval seconds
# By Monster Kid

import threading
import time

class TimerThread(threading.Thread):
    """
    A thread that executes a function every interval seconds
    """

    def __init__(self, interval, function):
        super().__init__()
        # set the thread as daemon
        self.daemon = True
        # the function to execute
        self.function = function
        # the interval between execution
        self.interval = interval
        # the stop event(used to stop the thread)
        self._stop_event = threading.Event()

    def stop(self):
        """
        Stop the thread
        """
        self._stop_event.set()

    def run(self):
        """
        Run the thread
        """

        while not self._stop_event.is_set():
            time.sleep(self.interval)
            self.function()

