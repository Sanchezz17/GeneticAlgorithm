import numpy as np
import pandas as pd
import random
from pylab import plot, ylabel, xlabel, show, figure
from typing import List, Tuple
from Client import Client
from Manager import Manager
from Point import Point
from RouteInfo import RouteInfo
from Timespan import Timespan


Route = List[Client]  # В генетическом алгоритме является генотипом
Generation = List[Route]


def create_route(clients: List[Client]) -> Route:
    """Возвращает новый случайный маршрут."""
    return random.sample(clients, len(clients))


def initial_population(population_size: int, clients: List[Client]) -> Generation:
    """Цикл вызовов createRoute для создания начальной популяции.
    Возвращает начальную популяцию."""
    population = []
    for i in range(0, population_size):
        population.append(create_route(clients))
    return population


def rank_routes(manager: Manager, generation: Generation) -> List[Tuple[int, RouteInfo]]:
    """Вычисление параметров для каждого маршрута.
    Ранжирование маршрутов по значению функции приспособленности.
    Возвращает отсортированный по значению функции приспособленности
    список пар (индекс маршрута, информация о маршруте)."""
    route_info = []
    for i in range(0, len(generation)):
        route_info.append((i, RouteInfo(manager, generation[i])))
    return sorted(route_info, key=lambda item: item[1].fitness, reverse=True)


def selection(population_ranked: List[Tuple[int, RouteInfo]], elite_size: int) -> List[int]:
    """Селекция: выбор маршрутов, которые будут использованы для создания следующего поколения.
    Возвращает список индексов выбранных маршрутов."""
    selection_results = []
    df = pd.DataFrame(np.array([(item[0], item[1].fitness) for item in population_ranked]),
                      columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_percent'] = 100 * df.cum_sum / df.Fitness.sum()

    for i in range(0, elite_size):
        selection_results.append(population_ranked[i][0])
    for _ in range(0, len(population_ranked) - elite_size):
        pick = 100 * random.random()
        for i in range(0, len(population_ranked)):
            if pick <= df.iat[i, 3]:
                selection_results.append(population_ranked[i][0])
                break
    return selection_results


def get_mating_pool(population: Generation, selection_results: List[int]) -> Generation:
    """Возвращает множество маршрутов-родителей, которые были выбраны."""
    return [population[index] for index in selection_results]


def breed(parent1: Route, parent2: Route) -> Route:
    """Функция скрещивания двух маршрутов-родителей.
    Возвращает результат скрещивания двух маршрутов-родителей."""
    child_p1 = []

    gene_a = int(random.random() * len(parent1))
    gene_b = int(random.random() * len(parent1))

    start_gene = min(gene_a, gene_b)
    end_gene = max(gene_a, gene_b)

    for i in range(start_gene, end_gene):
        child_p1.append(parent1[i])

    child_p2 = [item for item in parent2 if item not in child_p1]

    child = child_p1 + child_p2
    return child


def breed_population(mating_pool: Generation, elite_size: int) -> Generation:
    """Функция скрещивания популяции.
    Возвращает новую популяцию, полученную в результате скрещивания."""
    children = []
    # Элитарность - элита автоматически проходит в следующее поколение
    for i in range(0, elite_size):
        children.append(mating_pool[i])

    pool = random.sample(mating_pool, len(mating_pool))

    for i in range(0, len(mating_pool) - elite_size):
        child = breed(pool[i], pool[len(mating_pool) - i - 1])
        children.append(child)
    return children


def mutate(individual: Route, mutation_rate: float) -> Route:
    """Мутация генотипа.
    Возвращает мутированный генотип."""
    for swapped in range(len(individual)):
        if random.random() < mutation_rate:
            swap_with = int(random.random() * len(individual))

            individual1 = individual[swapped]
            individual2 = individual[swap_with]

            individual[swapped] = individual1
            individual[swap_with] = individual2

    return individual


def mutate_population(population: Generation, mutation_rate: float) -> Generation:
    """Мутация популяции.
    Возвращает мутированную популяцию."""
    mutated_population = []
    for i in range(0, len(population)):
        mutate_individual = mutate(population[i], mutation_rate)
        mutated_population.append(mutate_individual)

    return mutated_population


def get_next_generation(manager: Manager,
                        current_generation: Generation,
                        elite_size: int,
                        mutation_rate: float) -> Generation:
    """Основной цикл:
    Функция, производящая новое поколение.
    Во-первых, ранжируем маршруты текущего поколения используя "rank_routes".
    Затем выбираем множество потенциальных родителей в функции "selection".
    Создаем множество потенциальных родителей в функции "get_mating_pool".
    Наконец, создаем новое поколение, используя функцию "breed_population".
    и затем применяем мутацию в функции "mutate_population".
    Возвращает новую популяцию."""
    population_ranked = rank_routes(manager, current_generation)
    selection_results = selection(population_ranked, elite_size)
    mating_pool = get_mating_pool(current_generation, selection_results)
    children = breed_population(mating_pool, elite_size)
    next_generation = mutate_population(children, mutation_rate)
    return next_generation


#
def genetic_algorithm_plot(manager: Manager,
                           population: List[Client],
                           pop_size: int,
                           elite_size: int,
                           mutation_rate: float,
                           generation_count: int):
    """Генетический алгоритм.
    Основной цикл выполняется определенное количество раз.
    Отслеживается прогресс и по окончании работы алгоритма выводится несколько графиков для наглядности.
    На консоль печатается результат работы алгоритма - расписание встреч менеджера.
    """
    current_generation = initial_population(pop_size, population)
    progress = [rank_routes(manager, current_generation)[0][1]]

    for i in range(0, generation_count):
        current_generation = get_next_generation(manager, current_generation, elite_size, mutation_rate)
        progress.append(rank_routes(manager, current_generation)[0][1])

    best_route = progress[-1]
    print(best_route)

    plot([r.fitness for r in progress])
    ylabel('Fitness')
    xlabel('Generation')
    show()

    figure()
    plot([r.distance for r in progress])
    ylabel('Distance')
    xlabel('Generation')
    show()

    figure()
    plot([r.lateness_count for r in progress])
    ylabel('Lateness count')
    xlabel('Generation')
    show()

    figure()
    plot([r.waiting_time for r in progress])
    ylabel('Waiting time')
    xlabel('Generation')
    show()

    figure()
    plot([r.value for r in progress])
    ylabel('Value')
    xlabel('Generation')
    show()


# 540 = 9:00, 1260 = 21:00
# расстояние в метрах
# скорость в м / мин
# время в минутах
radius = 5000  # радиус расположения клиентов в метрах

random_manager = Manager(
    start=Point(x=int(random.random() * radius), y=int(random.random() * radius)),
    finish=Point(x=int(random.random() * radius), y=int(random.random() * radius)),
    work_time=Timespan(from_time=540, to_time=1260),
    speed=10 * 60  # 36 км/час = 600 м/мин
)
random_client_list = []
min_meeting_duration = 20
max_meeting_duration = 60

for _ in range(0, 25):
    random_meeting_duration = random.randint(min_meeting_duration, max_meeting_duration)
    random_free_time_from = random.randint(random_manager.work_time.from_time,
                                           random_manager.work_time.to_time - random_meeting_duration)
    random_free_time_to = random.randint(random_free_time_from + random_meeting_duration,
                                         random_manager.work_time.to_time)
    random_client_list.append(
        Client(
            value=random.randint(1, 100),
            location=Point(x=int(random.random() * radius), y=int(random.random() * radius)),
            meeting_duration=random_meeting_duration,
            free_time=Timespan(from_time=random_free_time_from, to_time=random_free_time_to)
        ))

genetic_algorithm_plot(manager=random_manager,
                       population=random_client_list,
                       pop_size=100,
                       elite_size=20,
                       mutation_rate=0.01,
                       generation_count=500)
