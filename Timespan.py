class Timespan:
    def __init__(self, from_time, to_time):
        self.from_time = from_time
        self.to_time = to_time

    def __repr__(self):
        return f"From {self.from_time} to {self.to_time}"
