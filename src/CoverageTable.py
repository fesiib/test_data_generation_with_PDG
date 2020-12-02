from Predicate import Predicate
# from PDG import PDG

class CoverageTable:
    predicates = []

    def __init__(self, predicates):
        self.predicates = predicates

    def calculate_ease(self, predicate, pdg):
        return predicate.number

    def calculate_improved_ease(self, predicate, pdg):
        if predicate.branch == False:
            return predicate.number + 1
        return predicate.number

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
            return "ALL BRANCHES ARE COVERED"

    def __str__(self):
        for predicate in self.predicates:
            print(predicate)
        return ""


def test1():
    predicate1 = Predicate(1, 3, "if tri == 1", True, True)
    predicate2 = Predicate(2, 6, "if tri >= 2", True, False)
    predicate3 = Predicate(2, 6, "if tri >= 2", False, False)
    predicate4 = Predicate(3, 8, "if tri <= 3", True, False)
    predicates = [predicate1, predicate2, predicate3, predicate4]
    table = CoverageTable(predicates)
    print(table)
    print(table.get_target_branch())
