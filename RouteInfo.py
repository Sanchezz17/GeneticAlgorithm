import math
from Timespan import Timespan
from Client import Client


class RouteInfo:
    def __init__(self, manager, route):
        if len(route) == 0:
            raise ValueError("Маршрут не должен быть пустым")

        self.manager = manager
        # Добавляем фиктивных клиентов для стартовой и конечной точки
        start_dummy_client = Client(
            value=0,
            location=self.manager.start,
            meeting_duration=0,
            free_time=Timespan(from_time=0, to_time=math.inf)
        )
        end_dummy_client = Client(
            value=0,
            location=self.manager.finish,
            meeting_duration=0,
            free_time=Timespan(from_time=0, to_time=math.inf)
        )
        self.route = [start_dummy_client, *route, end_dummy_client]
        self.distance = 0
        self.lateness_count = 0
        self.waiting_time = 0
        self.fitness = 0.0
        self.value = 0

        self.calculate_parameters()

    def calculate_parameters(self):
        if self.distance != 0:  # если параметры уже рассчитаны, то выходим
            return

        current_time = self.manager.work_time.from_time
        path_distance = 0
        lateness_count = 0
        waiting_time = 0
        value = 0

        # от стартовой точки до первого клиента
        # first_client = self.route[0]
        # current_distance = self.manager.start.distance(first_client.location)
        # path_distance += current_distance
        # current_time += int(current_distance / self.manager.speed)
        #
        # if current_time < first_client.free_time.from_time:
        #     waiting_time += first_client.free_time.from_time - current_time
        #     current_time = first_client.free_time.from_time
        #
        # if current_time > first_client.free_time.to_time - first_client.meeting_duration:
        #     lateness_count += 1
        # else:
        #     current_time += first_client.meeting_duration
        #     value += first_client.value

        for i in range(0, len(self.route) - 1):
            from_client = self.route[i]
            to_client = self.route[i + 1]

            current_distance = from_client.location.distance(to_client.location)
            path_distance += current_distance
            current_time += int(current_distance / self.manager.speed)

            if current_time < to_client.free_time.from_time:
                waiting_time += to_client.free_time.from_time - current_time
                current_time = to_client.free_time.from_time

            if current_time > to_client.free_time.to_time - to_client.meeting_duration:
                lateness_count += 1
            else:
                current_time += to_client.meeting_duration
                value += to_client.value

        # от последнего клиента до конечной точки
        last_client = self.route[-1]
        current_distance = last_client.location.distance(self.manager.finish)
        path_distance += current_distance
        current_time += int(current_distance / self.manager.speed)

        self.distance = path_distance
        self.lateness_count = lateness_count
        self.waiting_time = waiting_time
        self.value = value
        self.fitness = self.value / float(self.distance + 3 * self.lateness_count + 2 * self.waiting_time)
    #
    # def route_fitness(self):
    #     if self.fitness == 0:
    #         self.fitness = self.value / float(self.distance + 3 * self.lateness_count + 2 * self.waiting_time)
    #     return self.fitness
