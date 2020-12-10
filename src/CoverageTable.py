from Predicate import Predicate
from PDG import PDG


class CoverageTable:
    predicates = []
    tests = dict()

    def __init__(self, pdg):
        self.predicates = []
        for key in pdg.control_flow:
            self.predicates.append(Predicate(key[0], key[1], key[2], key[3], key[4]))

    def calculate_ease(self, predicate, pdg):
        if predicate.coverage_status:
            return 0
        tup = (predicate.number, predicate.program_line, predicate.predicate, predicate.branch, predicate.coverage_status)
        ease = 1000
        for p in self.predicates:
            t = (p.number, p.program_line, p.predicate, p.branch, p.coverage_status)
            if tup in pdg.control_flow[t][0] or tup in pdg.control_flow[t][1]:
                ease = min(ease, self.calculate_ease(p, pdg) + 1)
        return ease

    def calculate_improved_ease(self, predicate, pdg):
        if predicate.coverage_status:
            return 0
        # calculate previous total ease
        total_ease = 0
        for p in self.predicates:
            if p != predicate:
                total_ease += self.calculate_ease(p, pdg)
        # create new pdg and cov table with new predicate
        pdg.update(predicate)
        new_cov_table = CoverageTable(pdg)
        # calculate new total ease
        total_new_ease = 0
        for p in new_cov_table.predicates:
            total_new_ease += new_cov_table.calculate_ease(p, pdg)
        return total_ease - total_new_ease

    def get_target_branch(self, pdg):
        metrics = {}
        for predicate in self.predicates:
            if not predicate.coverage_status:
                ease = self.calculate_ease(predicate, pdg)
                minus_improved = -self.calculate_improved_ease(predicate, pdg)
                metrics[predicate] = (ease, minus_improved)
        if len(metrics) > 0:
            sorted_predicates = sorted(metrics, key=metrics.get)
            return sorted_predicates[0]
        else:
            return None

    def drop_predicate(self, predicate):
        self.predicates.remove(predicate)
        return

    # to implement - pizdec nevozmozhno zhe
    def update(self, population):
        pass

    # to implement
    def get_tests(self):
        pass

    def __str__(self):
        for predicate in self.predicates:
            print(predicate)
        return ""


def test_eases():
    pdg = PDG("# tri import sys i = int(sys.argv[1]) j = int(sys.argv[2]) k = int(sys.argv[3]) if i <= 0 or j <= 0 or k <= 0: print(4) exit() tri = 0 if i == j: tri += 1 if i == k: tri += 2 if j == k: tri += 3 if tri == 0: if i + j < k or j + k < i or k + i < j: tri = 4 else: tri = 1 print(tri) exit() if tri > 3: tri = 3 elif tri == 1 and i + j > k: tri = 2 elif tri == 2 and i + k > j: tri = 2 elif tri == 3 and j + k > i: tri = 2 else: tri = 4 print(tri) exit()")
    cov_table = CoverageTable(pdg)
    P = Predicate(8, 30, "if tri == 1 and i + j > k", True, False)
    print(cov_table.calculate_ease(P, pdg))
    print(cov_table.calculate_improved_ease(P, pdg))


test_eases()