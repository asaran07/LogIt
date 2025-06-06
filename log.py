class Log:
    def __init__(self, name, duration, engagement):
        self.name = name
        self.duration = duration
        self.engagement = engagement
        self.tag = None

    def __str__(self):
        return f"{self.name} - Duration: {self.duration} minutes, Engagement: {self.engagement}"

    def add_to_tag(self, tag):
        self.tag = tag
        tag.logs.append(self)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)
