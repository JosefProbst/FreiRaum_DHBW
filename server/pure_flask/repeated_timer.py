from threading import Timer

# https://stackoverflow.com/a/38317060


class RepeatedTimer:
    def __init__(self, interval, repeated_function):
        self._timer = None
        self.interval = interval
        self.repeated_function = repeated_function
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.repeated_function()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

