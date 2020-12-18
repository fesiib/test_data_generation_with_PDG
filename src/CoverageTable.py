from Predicate import Predicate
from PDG import PDG


class CoverageTable:
    predicates = []
    pdg = {}
    tests = {}

    def __init__(self, source_code):
        self.predicates = []
        self.pdg = PDG(source_code)
        for key in self.pdg.control_flow:
            self.predicates.append(Predicate(key[0], key[1], key[2], key[3], key[4]))

    def calculate_ease(self, predicate):
        if predicate.coverage_status:
            return 0
        tup = (predicate.number, predicate.program_line, predicate.predicate, predicate.branch, predicate.coverage_status)
        ease = 1000
        for p in self.predicates:
            t = (p.number, p.program_line, p.predicate, p.branch, p.coverage_status)
            if tup in self.pdg.control_flow[t][0] or tup in self.pdg.control_flow[t][1]:
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
            self.predicates.append(Predicate(key[0], key[1], key[2], key[3], key[4]))
        # calculate new total ease
        total_new_ease = 0
        for p in self.predicates:
            total_new_ease += self.calculate_ease(p)
        return total_ease - total_new_ease

    def get_target_branch(self):
        metrics = {}
        for predicate in self.predicates:
            if not predicate.coverage_status:
                ease = self.calculate_ease(predicate)
                minus_improved = -self.calculate_improved_ease(predicate)
                metrics[predicate] = (ease, minus_improved)
        if len(metrics) > 0:
            sorted_predicates = sorted(metrics, key=metrics.get)
            return sorted_predicates[0]
        else:
            return None

    def drop_predicate(self, predicate):
        self.predicates.remove(predicate)
        return

    def update(self, population):
        for test in population.solutions:
            for predicate in self.predicates:
                if self.pdg.predicate_to_constraint(predicate, 1).is_satisified(test.values):
                    self.pdg.update(predicate)
                    self.predicates = []
                    for key in self.pdg.control_flow:
                        self.predicates.append(Predicate(key[0], key[1], key[2], key[3], key[4]))
                    self.tests[predicate] = test

    def get_tests(self):
        return self.tests

    def __str__(self):
        for predicate in self.predicates:
            print(predicate)
        return ""


def test_triangle_eases():
    cov_table = CoverageTable("# tri import sys i = int(sys.argv[1]) j = int(sys.argv[2]) k = int(sys.argv[3]) if i <= 0 or j <= 0 or k <= 0: "
              "print(4) exit() tri = 0 if i == j: tri += 1 if i == k: tri += 2 if j == k: tri += 3 if tri == 0: if i + j < k or "
              "j + k < i or k + i < j: tri = 4 else: tri = 1 print(tri) exit() if tri > 3: tri = 3 elif tri == 1 and i + j > k: "
              "tri = 2 elif tri == 2 and i + k > j: tri = 2 elif tri == 3 and j + k > i: tri = 2 else: tri = 4 print(tri) exit("
              ")")
    P = Predicate(8, 30, "if tri == 1 and i + j > k", True, False)
    print(cov_table.calculate_ease(P))
    print(cov_table.calculate_improved_ease(P))


def test_find_max_eases():
    cov_table = CoverageTable("# find_max import sys x = int(sys.argv[1]) y = int(sys.argv[2]) z = int(sys.argv[3]) if x > y: if x > z: print("
              "x) else: print(z) else: if y < z: print(z) else: print(y)")
    P = Predicate(2, 9, "if y > z", True, False)
    print(cov_table.calculate_ease(P))
    print(cov_table.calculate_improved_ease(P))


test_triangle_eases()
test_find_max_eases()
