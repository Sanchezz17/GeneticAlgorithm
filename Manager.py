import math
from Client import Client
from Point import Point
from Timespan import Timespan


class Manager:
    def __init__(self, start: Point, finish: Point,
                 work_time: Timespan, speed: int) -> None:
        self.start = start
        self.start_dummy_client = Client(
            value=0,
            location=start,
            meeting_duration=0,
            free_time=Timespan(from_time=0, to_time=math.inf)
        )
        self.finish = finish
        self.end_dummy_client = Client(
            value=0,
            location=finish,
            meeting_duration=0,
            free_time=Timespan(from_time=0, to_time=math.inf)
        )
        self.work_time = work_time
        self.speed = speed

    def __str__(self) -> str:
        return f"Manager: (start: {self.start}, finish: {self.finish}, work time: {self.work_time})"
