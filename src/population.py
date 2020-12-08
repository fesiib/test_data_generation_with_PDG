import random

class Population():
    def __init__(self, solutions, fitness):
        self.solutions = solutions
        self.fitness = fitness

    def initial_population(self, population_size, test_size):
        population = list()
        for i in range(population_size):
            test = list()
            for j in range(test_size):
                test.append(random.randint(-1000, 1000))
            population.append(test)
        return population

    def mutate_1(self, lower, upper, prob):
        mutated = list()
        for test in self.solutions:
            test_list = list(map(int, test.split()))
            for i in range(len(test_list)):
                if random.random() < prob:
                    test_list[i] = random.uniform(lower, upper)
            test_mutated = "".join(test_list)
            mutated.append(test_mutated)
        return mutated

    def mutate_2(self, lower, upper, prob, rate):
        mutated = list()
        for test in self.solutions:
            test_list = list(map(int, test.split()))
            for i in range(len(test_list)):
                if random.random() < prob:
                    test_list[i] = random.uniform(lower, upper)
            test_mutated = "".join(test_list)
            mutated.append(test_mutated)
        prob -= rate
        return mutated

    def crossover(self, parent_1, parent_2, rate):
        parent_1 = list(map(int, parent_1.split()))
        parent_2 = list(map(int, parent_2.split()))
        if random.random() < rate:
            crossover_point = random.choice(range(len(parent_1)))
            parent_1 = parent_1[:crossover_point] + parent_2[crossover_point:]
            parent_2 = parent_2[:crossover_point] + parent_1[crossover_point:]
        return parent_1, parent_2

    def tournament_selection(self):
        parents = []
        for _ in range(2):
            x, y = random.choices(self.solutions)
            if self.fitness[x] > self.fitness[y]:
                parent = x
            else:
                parent = y
            parents.append(parent)
        return tuple(parents)
