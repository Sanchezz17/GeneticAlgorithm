from Point import Point
from Timespan import Timespan


class Client:  # В генетическом алгоритме является геном
    def __init__(self, value: int, location: Point,
                 meeting_duration: float, free_time: Timespan) -> None:
        self.value = value
        self.location = location
        self.meeting_duration = meeting_duration
        self.free_time = free_time

    def __str__(self) -> str:
        return f"Клиент: (ценность: {self.value}, местоположение: {self.location}, " \
               f"длительность встречи: {self.meeting_duration}, свободное время: {self.free_time}"
