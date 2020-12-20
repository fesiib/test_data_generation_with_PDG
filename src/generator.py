"""
Main Class that abstracts Test Data Generation API.
It represents first layer of contact with the user code
and should handle:
    - Tuning Global Variables
    - Generation of Test Data using GA and PDG
"""

from population import Population
from pdg import PDG
from coverageTable import CoverageTable
from sourcecode import SourceCode
from testcase import TestCase
from predicate import Predicate
from customConstraint import CustomConstraint

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
        test_type: int = const.DEF_TEST_TYPE,
    ):
        self.seed_size = seed_size
        self.population_size = population_size
        self.rate_crossover = rate_crossover
        self.rate_mutation = rate_mutation
        self.max_iter = max_iter
        self.wait_iter = wait_iter
        self.dependency_mode = dependency_mode
        self.test_type = test_type
        self.validate_global_variables()

    def generate_tests(self, source_code: SourceCode):
        pdg = PDG(source_code)
        ct = CoverageTable(source_code)

        # Random Seeding CT
        random_seed = Population()
        random_seed.initial_population(self.seed_size, self.test_type)
        ct.update(random_seed)

        dependency_mode = 0

        # for Statistics
        generations_cnt = 0

        while True:
            target: Predicate = ct.get_target_branch()

            if target is None:
                break

            constraint: CustomConstraint = pdg.predicate_to_constraint(
                target, dependency_mode
            )
            cur_population = Population()
            cur_population.initial_population(
                self.population_size, self.test_type
            )
            ct.update(cur_population)

            generations_cnt += 1

            iter_cnt = 0
            wait_iter = self.wait_iter

            while (
                iter_cnt <= self.max_iter
                and target.get_coverage_status() is False
            ):
                iter_cnt += 1

                next_population = Population()

                # Best Solution Survives
                best_solution: TestCase = cur_population.get_best_by_fitness(
                    constraint
                )
                next_population.insert(best_solution)
                generations_cnt += 1
                while next_population.get_size() < self.population_size:
                    parent1, parent2 = cur_population.tournament_selection(constraint)
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
                    if next_population.get_size() < self.population_size:
                        next_population.insert(offspring2)

                next_best_fitness = next_population.get_best_by_fitness(
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

        # print(generations_cnt)
        return ct, generations_cnt
