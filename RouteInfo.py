import math
from Client import Client
from Manager import Manager
from Timespan import Timespan, display_time
from typing import List


class RouteInfo:
    def __init__(self, manager: Manager, route: List[Client]) -> None:
        if len(route) == 0:
            raise ValueError("Маршрут не должен быть пустым")

        self.manager = manager
        self.route = [manager.start_dummy_client, *route, manager.end_dummy_client]
        self.distance = 0
        self.cancellation_count = 0
        self.waiting_time = 0
        self.fitness = 0.0
        self.value = 0
        self.meetings = []
        self.end_time = 0

        self.calculate_parameters()

    def calculate_parameters(self) -> None:
        """Функция расчета всех параметров маршрута"""
        if self.distance != 0:
            # если параметры уже рассчитаны, то выходим
            return

        current_time = self.manager.work_time.from_time
        path_distance = 0
        cancellation_count = 0
        waiting_time = 0
        value = 0
        meetings = []

        for i in range(0, len(self.route) - 1):
            from_client = self.route[i]
            to_client = self.route[i + 1]

            current_distance = from_client.location.distance(to_client.location)
            path_distance += current_distance
            arrival_time = current_time + int(current_distance / self.manager.speed)

            if arrival_time < to_client.free_time.from_time:
                waiting_time += to_client.free_time.from_time - arrival_time
                arrival_time = to_client.free_time.from_time

            if arrival_time > to_client.free_time.to_time - to_client.meeting_duration:
                cancellation_count += 1
            else:
                meetings.append((to_client.location, Timespan(current_time, current_time + to_client.meeting_duration)))
                current_time = arrival_time + to_client.meeting_duration
                value += to_client.value

        self.distance = path_distance
        self.cancellation_count = cancellation_count
        self.waiting_time = waiting_time
        self.value = value
        self.meetings = meetings[:-1]
        self.end_time = current_time
        self.fitness = self.value / float(self.distance + 10 * self.cancellation_count + 2 * self.waiting_time)

    def __str__(self) -> str:
        meetings = "\n\t".join([f"{meeting_location} {meeting_time}"
                                for (meeting_location, meeting_time) in self.meetings])
        return (
            "Маршрут\n"
            f"Старт: {self.manager.start} в {display_time(self.manager.work_time.from_time * 60)}\n\n"
            "Встречи\n\t"
            f"{meetings}\n\n"
            f"Конечная точка: {self.manager.finish} в {display_time(self.end_time * 60)}\n"
            f"Длина маршрута (в метрах): {self.distance}\n"
            f"Количество встреч: {len(self.meetings)} из {len(self.route)}\n"
            f"Суммарное время ожидания (в минутах): {self.waiting_time}\n"
            f"Суммарная ценность клиентов: {self.value}\n"        
            f"Значение функции приспособленности: {self.fitness}\n"
        )
