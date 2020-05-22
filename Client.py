class Client:  # In genetic algorithm, this is our representation of Gene.
    def __init__(self, value, location,  meeting_duration, free_time):
        self.value = value
        self.location = location
        self.meeting_duration = meeting_duration
        self.free_time = free_time

    def __repr__(self):
        return f"Client: (value: {self.value}, location: {self.location}, " \
               f"meeting duration: {self.meeting_duration}, free time: {self.free_time}"
