class Activity:
    def __init__(self, name):
        self.name = name
        self.logs = []

    def add_log(self, duration, engagement):
        self.logs.append({"duration": duration, "engagement": engagement})

    def __str__(self):
        return self.name

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)
