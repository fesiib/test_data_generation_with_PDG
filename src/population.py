from typing import List, Tuple
from testcase import TestCase
from customconstraint import CustomConstraint
import const

import random
import copy


class Population:
    def __init__(self, solutions: List[TestCase] = None):
        self.solutions = solutions

    def initial_population(self, population_size: int, test_type: int):
        self.solutions = []
        for _ in range(population_size):
            test = TestCase(test_type=test_type)
            self.solutions.append(test)

    def mutate(self, solution: TestCase, mode: int) -> TestCase:
        offspring = copy.deepcopy(solution)
        offspring[random.randint(0, len(solution) - 1)] = random.randint(
            0, 10000
        )

        return offspring

    def crossover(
        self, parent_1: TestCase, parent_2: TestCase
    ) -> Tuple[TestCase]:
        crossover_point = random.choice(range(len(parent_1)))
        offspring_1 = parent_1[:crossover_point] + parent_2[crossover_point:]
        offspring_2 = parent_2[:crossover_point] + parent_1[crossover_point:]

        return offspring_1, offspring_2

    def tournament_selection(
        self, constraint: CustomConstraint
    ) -> Tuple[TestCase]:
        parents = [None, None]
        for i in range(2):
            candidate_1, candidate_2 = random.choices(self.solutions)
            if candidate_1.get_fitness(constraint) < candidate_2.to_fitness(
                constraint
            ):
                parent = candidate_1
            else:
                parent = candidate_2
            parents[i] = parent

        return tuple(parents)

    def get_size(self) -> int:
        return len(self.solutions)

    def get_best_by_fitness(self, constraint: CustomConstraint) -> TestCase:
        best_fitness = const.DEF_INF
        best = None
        for test in self.solutions:
            current_fitness = test.get_fitness(constraint)
            if current_fitness < best_fitness:
                best_fitness = current_fitness
                best = test

        return best

    def insert(self, solution: TestCase):
        self.solutions.append(solution)
