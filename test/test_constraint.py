import pytest
from customConstraint import CustomConstraint

from constraint import Problem


def test_constraint():
    c = Problem()
    c.addVariable("i", range(-100, 10))
    c.addVariable("j", range(-10, 10))
    c.addVariable("k", range(-10, 10))
    c.addConstraint(lambda i, j, k: i <= 0 or j <= 0 or k <= 0, ("i", "j", "k"))
    C = CustomConstraint(c)
    values1 = [-1, -1, -1]
    values2 = [9, 8, 2]
    assert C.to_fitness(values1) == 9963.0
    assert C.to_fitness(values2) == 12349.0
