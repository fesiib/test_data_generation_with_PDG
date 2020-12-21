from typing import List, Tuple
from testcase import TestCase
from customconstraint import CustomConstraint
import const

import random
import copy


class Population:
    def __init__(self, source_code, solutions: List[TestCase] = []):
        self.solutions = solutions
        self.source_code = source_code

    def initial_population(self, population_size: int, test_type: int):
        self.solutions = []
        for _ in range(population_size):
            test = TestCase(test_type=test_type)
            test.execute_test_on(self.source_code)
            self.solutions.append(test)

    def mutate(self, solution: TestCase, mode: int) -> TestCase:
        offspring = copy.deepcopy(solution)
        offspring.input[
            random.randint(0, len(solution.input) - 1)
        ] = random.randint(-const.DEF_RNG, const.DEF_RNG)
        offspring.execute_test_on(self.source_code)
        return offspring

    def crossover(
        self, parent_1: TestCase, parent_2: TestCase
    ) -> Tuple[TestCase]:
        crossover_point = random.choice(range(len(parent_1.input)))
        offspring_1 = TestCase(
            input=parent_1.input[:crossover_point]
            + parent_2.input[crossover_point:]
        )
        offspring_2 = TestCase(
            input=parent_2.input[:crossover_point]
            + parent_1.input[crossover_point:]
        )
        offspring_1.execute_test_on(self.source_code)
        offspring_2.execute_test_on(self.source_code)
        return offspring_1, offspring_2

    def tournament_selection(
        self, constraint: CustomConstraint
    ) -> Tuple[TestCase]:
        parents = [None, None]
        for i in range(2):
            candidate_1, candidate_2 = random.choices(self.solutions, k=2)
            if candidate_1.get_fitness(constraint) < candidate_2.get_fitness(
                constraint
            ):
                parent = candidate_1
            else:
                parent = candidate_2
            parents[i] = parent

        ret = tuple(parents)
        return ret

    def get_size(self) -> int:
        return len(self.solutions)

    def get_best_by_fitness(self, constraint: CustomConstraint) -> TestCase:
        if len(self.solutions) == 0:
            raise AssertionError
        best = self.solutions[0]
        best_fitness = best.get_fitness(constraint)
        for test in self.solutions:
            current_fitness = test.get_fitness(constraint)
            if current_fitness < best_fitness:
                best_fitness = current_fitness
                best = test
        return best

    def insert(self, solution: TestCase):
        solution.execute_test_on(self.source_code)
        self.solutions.append(solution)
