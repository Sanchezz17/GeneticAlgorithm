import pandas as pd
from pylab import *
import numpy as np
import random
from Point import Point
from Timespan import Timespan
from Client import Client
from Manager import Manager
from RouteInfo import RouteInfo


# Creates an one individual
def create_route(client_list):
    route = random.sample(client_list, len(client_list))
    return route


# Loop over createRoute def to create many routes for our population.
def initial_population(pop_size, client_list):
    population = []
    for i in range(0, pop_size):
        population.append(create_route(client_list))
    return population


# Determinate the fitness. Simulate the "survival of the fittest";
# Use the Fitness to rank each individual in the population;
# The output will be an ordered list with the route IDs and each associated fitness score.
def rank_routes(manager, population):
    route_info = {}
    for i in range(0, len(population)):
        route_info[i] = RouteInfo(manager, population[i])
    return sorted(route_info.items(), key=lambda r: r[1].fitness, reverse=True)


# SELECT THE MATING POOL:
# Select the parents that will be used to create the next generation
def selection(pop_ranked, elite_size):
    selection_results = []
    df = pd.DataFrame(np.array([(r[0], r[1].fitness) for r in pop_ranked]), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_percent'] = 100 * df.cum_sum / df.Fitness.sum()

    for i in range(0, elite_size):
        selection_results.append(pop_ranked[i][0])
    for _ in range(0, len(pop_ranked) - elite_size):
        pick = 100 * random.random()
        for i in range(0, len(pop_ranked)):
            if pick <= df.iat[i, 3]:
                selection_results.append(pop_ranked[i][0])
                break
    return selection_results


def get_mating_pool(population, selection_results):
    mating_pool = []
    for i in range(0, len(selection_results)):
        index = selection_results[i]
        mating_pool.append(population[index])
    return mating_pool


# BREED FUNCTION:
# With our mating pool created, we can create the next generation in a process called "crossover"
def breed(parent1, parent2):
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


def breed_population(mating_pool, elite_size):
    children = []
    length = len(mating_pool) - elite_size
    pool = random.sample(mating_pool, len(mating_pool))

    for i in range(0, elite_size):
        children.append(mating_pool[i])

    for i in range(0, length):
        child = breed(pool[i], pool[len(mating_pool) - i - 1])
        children.append(child)
    return children


# MUTATE:
def mutate(individual, mutation_rate):
    for swapped in range(len(individual)):
        if random.random() < mutation_rate:
            swap_with = int(random.random() * len(individual))

            individual1 = individual[swapped]
            individual2 = individual[swap_with]

            individual[swapped] = individual1
            individual[swap_with] = individual2

    return individual


def mutate_population(population, mutation_rate):
    mutated_population = []
    for i in range(0, len(population)):
        mutate_individual = mutate(population[i], mutation_rate)
        mutated_population.append(mutate_individual)

    return mutated_population


# REPEAT:
# Function that produces a new generation.
# First, we rank the routes in the current generation using "rankRoutes".
# We then determine our potential parents by running the "selection" function,
# which allows us to create the mating pool using the "matingPool" function.
# Finally, we then create our new generation using the "breedPopulation" function
# and then applying mutation using the "mutatePopulation" function.
def get_next_generation(manager, current_gen, elite_size, mutation_rate):
    population_ranked = rank_routes(manager, current_gen)
    selection_results = selection(population_ranked, elite_size)
    mating_pool = get_mating_pool(current_gen, selection_results)
    children = breed_population(mating_pool, elite_size)
    next_generation = mutate_population(children, mutation_rate)
    return next_generation


# def genetic_algorithm(manager, population, pop_size, elite_size, mutation_rate, generations):
#     population = initial_population(pop_size, population)
#     print("Initial distance: " + str(1 / rank_routes(manager, population)[0][1]))
#
#     for i in range(0, generations):
#         population = get_next_generation(manager, population, elite_size, mutation_rate)
#
#     print("Final distance: " + str(1 / rank_routes(manager, population)[0][1]))
#     best_route_index = rank_routes(manager, population)[0][0]
#     best_route = population[best_route_index]
#     return best_route


def genetic_algorithm_plot(manager, population, pop_size, elite_size, mutation_rate, generations):
    population = initial_population(pop_size, population)
    progress = []
    progress.append(rank_routes(manager, population)[0][1])

    for i in range(0, generations):
        population = get_next_generation(manager, population, elite_size, mutation_rate)
        progress.append(rank_routes(manager, population)[0][1])

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
random_manager = Manager(
    start=Point(x=int(random.random() * 200), y=int(random.random() * 200)),
    finish=Point(x=int(random.random() * 200), y=int(random.random() * 200)),
    work_time=Timespan(from_time=540, to_time=1260),
    speed=10 * 60  # 36 км/час = 600 м/мин
)
random_client_list = []
min_meeting_duration = 20
max_meeting_duration = 60

for _ in range(0, 25):
    random_meeting_duration = random.randint(min_meeting_duration, max_meeting_duration)
    random_free_time_from = random.randint(random_manager.work_time.from_time, random_manager.work_time.to_time - random_meeting_duration)
    random_free_time_to = random.randint(random_free_time_from + random_meeting_duration, random_manager.work_time.to_time)
    random_client_list.append(
        Client(
            value=random.randint(1, 100),
            location=Point(x=int(random.random() * 200), y=int(random.random() * 200)),
            meeting_duration=random_meeting_duration,
            free_time=Timespan(from_time=random_free_time_from, to_time=random_free_time_to)
        ))

genetic_algorithm_plot(manager=random_manager, population=random_client_list, pop_size=100, elite_size=20, mutation_rate=0.01, generations=5000)
