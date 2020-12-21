import pytest

from coveragetable import CoverageTable
from predicate import Predicate
from testcase import TestCase
from sourcecode import SourceCode
from population import Population


def test_triangle_eases():
    cov_table = CoverageTable(SourceCode(
        "# tri import sys i = int(sys.argv[1]) j = int(sys.argv[2]) k = int(sys.argv[3]) if i <= 0 or j <= 0 or k <= 0: "
        "print(4) exit() tri = 0 if i == j: tri += 1 if i == k: tri += 2 if j == k: tri += 3 if tri == 0: if i + j < k or "
        "j + k < i or k + i < j: tri = 4 else: tri = 1 print(tri) exit() if tri > 3: tri = 3 elif tri == 1 and i + j > k: "
        "tri = 2 elif tri == 2 and i + k > j: tri = 2 elif tri == 3 and j + k > i: tri = 2 else: tri = 4 print(tri) exit("
        ")"
    ))
    P = Predicate(8, 30, "if tri == 1 and i + j > k", True, False)
    assert cov_table.calculate_ease(P) == 3
    assert cov_table.calculate_improved_ease(P) == 6


def test_find_max_eases():
    cov_table = CoverageTable(SourceCode(
        "# find_max import sys x = int(sys.argv[1]) y = int(sys.argv[2]) z = int(sys.argv[3]) if x > y: if x > z: print("
        "x) else: print(z) else: if y < z: print(z) else: print(y)"
    ))
    P = Predicate(2, 9, "if y > z", True, False)
    assert cov_table.calculate_ease(P) == 1
    assert cov_table.calculate_improved_ease(P) == 1


def test_general():
    cov_table = CoverageTable(SourceCode(
        "# tri import sys i = int(sys.argv[1]) j = int(sys.argv[2]) k = int(sys.argv[3]) if i <= 0 or j <= 0 or k <= 0: "
        "print(4) exit() tri = 0 if i == j: tri += 1 if i == k: tri += 2 if j == k: tri += 3 if tri == 0: if i + j < k or "
        "j + k < i or k + i < j: tri = 4 else: tri = 1 print(tri) exit() if tri > 3: tri = 3 elif tri == 1 and i + j > k: "
        "tri = 2 elif tri == 2 and i + k > j: tri = 2 elif tri == 3 and j + k > i: tri = 2 else: tri = 4 print(tri) exit("
        ")"
    ))
    P = Predicate(1, 8, "if i <= 0 or j <= 0 or k <= 0", True, True)
    assert cov_table.get_target_branch().program_line == 20
    c = cov_table.pdg.predicate_to_constraint(P, 1)
    values = [9, 8, 2, 0]
    assert c.to_fitness(values) == 4.0


def test_update():
    sc = SourceCode(
        "# tri import sys i = int(sys.argv[1]) j = int(sys.argv[2]) k = int(sys.argv[3]) if i <= 0 or j <= 0 or k <= 0: "
        "print(4) exit() tri = 0 if i == j: tri += 1 if i == k: tri += 2 if j == k: tri += 3 if tri == 0: if i + j < k or "
        "j + k < i or k + i < j: tri = 4 else: tri = 1 print(tri) exit() if tri > 3: tri = 3 elif tri == 1 and i + j > k: "
        "tri = 2 elif tri == 2 and i + k > j: tri = 2 elif tri == 3 and j + k > i: tri = 2 else: tri = 4 print(tri) exit("
        ")"
    )
    cov_table = CoverageTable(sc)
    print(cov_table.calculate_coverage())
    print(cov_table.tests)
    t1 = TestCase([9, 8, -1], [0])
    t2 = TestCase([1, 2, 3], [0])
    pop = Population(sc, [t1, t2])
    cov_table.update(pop)
    print(cov_table.calculate_coverage())
    print(cov_table.tests)
    t3 = TestCase([1, 1, 1], [0])
    pop = Population(sc, [t3])
    cov_table.update(pop)
    print(cov_table.calculate_coverage())
    print(cov_table.tests)


test_update()
