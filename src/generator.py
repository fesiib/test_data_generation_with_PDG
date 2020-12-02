"""
Main Class that abstracts Test Data Generation API.
It represents first layer of contact with the user code
and should handle:
    - Tuning Global Variables
    - Generation of Test Data using GA and PDG
"""

from population import Population
from ipdg import IPDG
from coveragetable import CoverageTable
from sourcecode import SourceCode
from testcase import TestCase
from predicate import Predicate
from constraint import Constraint

import const
from typing import List
import random


class Generator:
    def validate_global_variables(self):
        if self.seed_size < 2 or self.seed_size > 10:
            raise AssertionError
        if self.population_size < 1 or self.population_size > 500:
            raise AssertionError
        if self.rate_crossover < 0.0 or self.rate_crossover > 0.9:
            raise AssertionError
        if self.rate_mutation < 0.0 or self.rate_mutation > 0.9:
            raise AssertionError
        if self.max_iter < 1 or self.max_iter > 1000:
            raise AssertionError
        if self.wait_iter < 0 or self.wait_iter > 1000:
            raise AssertionError
        if self.dependency_mode < 0 or self.dependency_mode > 3:
            raise AssertionError

    def __init__(
        self,
        seed_size: int = const.DEF_SEED_SIZE,
        population_size: int = const.DEF_POP_SIZE,
        rate_crossover: float = const.DEF_RATE_CROSSOVER,
        rate_mutation: float = const.DEF_RATE_MUTATION,
        max_iter: int = const.DEF_MAX_ITER,
        wait_iter: int = const.DEF_WAIT_ITER,
        dependency_mode: int = const.DEF_DEPENDENCY_MODE,
    ):
        self.seed_size = seed_size
        self.population_size = population_size
        self.rate_crossover = rate_crossover
        self.rate_mutation = rate_mutation
        self.max_iter = max_iter
        self.wait_iter = wait_iter
        self.dependency_mode = dependency_mode
        self.validate_global_variables()

    def generate_tests(self, source_code: SourceCode):
        ipdg = IPDG(source_code)
        ct = CoverageTable(source_code)

        ct.random_seed(self.seed_size)

        dependency_mode = 0

        while True:
            target: Predicate = ct.get_target_branch()

            if target is None:
                break

            constraint: Constraint = ipdg.predicate_to_constraint(
                target, dependency_mode
            )
            cur_population = Population()
            cur_population.initialize(self.population_size)
            ct.update(cur_population)

            iter_cnt = 0
            wait_iter = self.wait_iter

            while (
                iter_cnt <= self.max_iter
                and target.get_coverage_status() is False
            ):
                iter_cnt += 1

                next_population = Population()

                # Best Solution Survives
                best_solution: TestCase = cur_population.get_best_by_fintess(
                    constraint
                )
                next_population.insert(best_solution)

                while next_population.get_size() < self.population_size:
                    (parent1, parent2) = cur_population.tournament_selection()
                    offspring1: TestCase = parent1.copy()
                    offspring2: TestCase = parent2.copy()
                    if random.random() <= self.rate_crossover:
                        (offspring1, offspring2) = cur_population.crossover(
                            parent1, parent2
                        )
                    if random.random() <= self.rate_mutation:
                        offspring1 = cur_population.mutate(
                            offspring1, random.randint(0, 2)
                        )
                        offspring2 = cur_population.mutate(
                            offspring2, random.randint(0, 2)
                        )
                    next_population.insert(offspring1)
                    if next.population.get_size() < self.population_size:
                        next_population.insert(offspring2)

                next_best_fitness = next_population.get_best_by_fintess(
                    constraint
                ).get_fitness(constraint)

                if next_best_fitness >= best_solution.get_fitness(constraint):
                    wait_iter -= 1
                    if wait_iter <= 0:
                        break
                else:
                    wait_iter = self.wait_iter

                cur_population = next_population
                ct.update(next_population)

            if target.get_coverage_status() is False:
                if dependency_mode == self.dependency_mode:
                    ct.drop_predicate(target)
                    dependency_mode = 0
                else:
                    dependency_mode += 1
        return ct.get_tests()