import const

from constraint import *


class CustomConstraint:
    constraint = Problem()

    def __init__(self, constraint: Problem) -> object:
        self.constraint = constraint

    def is_satisfied(self, values):
        return self.to_fitness(values) == 0.0

    def to_fitness(self, values):
        print(values)
        test = {}
        cnt = 0
        for var in self.constraint._variables.keys():
            test[var] = values[cnt]
            cnt += 1
        solutions_iterator = self.constraint.getSolutionIter()
        fitness = const.DEF_INF
        for solution in solutions_iterator:
            cur_fitness = 0.0
            for key in solution.keys():
                cur_fitness += (test[key] - solution[key]) * (
                    test[key] - solution[key]
                )
            fitness = min(fitness, cur_fitness)
        return fitness
