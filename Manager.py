class Manager:
    def __init__(self, start, finish, work_time, speed):
        self.start = start
        self.finish = finish
        self.work_time = work_time
        self.speed = speed

    def __repr__(self):
        return f"Manager: (start: {self.start}, finish: {self.finish}, work time: {self.work_time})"
