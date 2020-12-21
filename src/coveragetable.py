from predicate import Predicate
from pdg import PDG

"""
TODO: change drop predicate

"""


class CoverageTable:
    predicates = []
    pdg = {}
    tests = {}

    def __init__(self, source_code):
        self.predicates = []
        self.pdg = PDG(source_code)
        for key in self.pdg.control_flow:
            self.predicates.append(
                Predicate(key[0], key[1], key[2], key[3], key[4])
            )

    def calculate_ease(self, predicate):
        if predicate.coverage_status:
            return 0
        tup = (
            predicate.number,
            predicate.program_line,
            predicate.predicate,
            predicate.branch,
            predicate.coverage_status,
        )
        ease = 1000
        for p in self.predicates:
            t = (
                p.number,
                p.program_line,
                p.predicate,
                p.branch,
                p.coverage_status,
            )
            if (
                tup in self.pdg.control_flow[t][0]
                or tup in self.pdg.control_flow[t][1]
            ):
                ease = min(ease, self.calculate_ease(p) + 1)
        return ease

    def calculate_improved_ease(self, predicate):
        if predicate.coverage_status:
            return 0
        # calculate previous total ease
        total_ease = 0
        for p in self.predicates:
            if p != predicate:
                total_ease += self.calculate_ease(p)
        # create new pdg and cov table with new predicate
        self.pdg.update(predicate)
        self.predicates = []
        for key in self.pdg.control_flow:
            self.predicates.append(
                Predicate(key[0], key[1], key[2], key[3], key[4])
            )
        # calculate new total ease
        total_new_ease = 0
        for p in self.predicates:
            total_new_ease += self.calculate_ease(p)
        return total_ease - total_new_ease

    def get_target_branch(self):
        metrics = {}
        for predicate in self.predicates:
            if not predicate.coverage_status and not predicate.dropped:
                ease = self.calculate_ease(predicate)
                minus_improved = -self.calculate_improved_ease(predicate)
                t = (
                    predicate.number,
                    predicate.program_line,
                    predicate.predicate,
                    predicate.branch,
                    predicate.coverage_status,
                )
                metrics[t] = (ease, minus_improved)
        if len(metrics) > 0:
            sorted_predicates = sorted(metrics, key=metrics.get)
            for predicate in self.predicates:
                if predicate.number == sorted_predicates[0][0]:
                    return predicate
            raise AssertionError
        else:
            return None

    def drop_predicate(self, predicate):
        self.predicates.remove(predicate)
        predicate.dropped = True
        self.predicates.append(predicate)

    def update(self, population):
        for test in population.solutions:
            for predicate in self.predicates:
                if self.pdg.predicate_to_constraint(predicate, 2).is_satisfied(
                    test.get_values()
                ):
                    self.pdg.update(predicate)
                    self.predicates = []
                    for key in self.pdg.control_flow:
                        self.predicates.append(
                            Predicate(key[0], key[1], key[2], key[3], key[4])
                        )
                    self.tests[predicate] = test

    def get_tests(self):
        return self.tests

    def calculate_coverage(self):
        covered = 0
        for predicate in self.predicates:
            if predicate.get_coverage_status():
                covered += 1
        return (float(covered) / float(len(self.predicates))) * 100.0

    def __str__(self):
        ret_str = ""
        for predicate in self.predicates:
            ret_str += str(predicate)
        return ret_str
