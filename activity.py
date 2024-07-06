class Activity:
    def __init__(self, name):
        self.name = name
        self.logs = []

    def add_log(self, log):
        if log not in self.logs:
            self.logs.append(log)
            log.activity = self

    def __str__(self):
        return self.name

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)
