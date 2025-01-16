import time


class Task:
    def __init__(self, name: str):
        self.name = name
        self.total_seconds_worked = 0  # accumulator for all active working time
        self.start_time = None
        self.is_paused = True  # start in paused state

    def start(self):
        """Reset and start new timer."""
        if self.is_paused:
            self.start_time = time.time()
            self.is_paused = False

    def pause(self):
        if not self.is_paused:
            elapsed = time.time() - self.start_time
            self.total_seconds_worked += elapsed
            self.is_paused = True

    def getMMSS(self) -> str:
        """Returns current time in MM:SS format."""
        minutes = int(self.total_seconds_worked // 60)
        leftover_seconds = int(self.total_seconds_worked % 60)
        return f"{minutes}:{leftover_seconds}"

    def stop(self):
        """
        Stop and return total time, also finalize the Task’s total time if it’s still running.
        """
        if not self.is_paused:
            self.pause()  # accumulate the final seconds
        return self.getMMSS()
