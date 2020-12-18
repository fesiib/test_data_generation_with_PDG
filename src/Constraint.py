from constraint import *


class Constraint:
	constraint = Problem()

	def __init__(self, constraint):
		self.constraint = constraint

	def is_satisfied(self, values):
		test = {}
		cnt = 0
		for var in self.constraint.variables:
			test[var] = values[cnt]
			cnt += 1
		return test in self.constraint.getSolutions()

	def constraint_to_fitness(self, values):
		if self.is_satisfied(values):
			return 1
		return 0


def test_constraint():
	c = Problem()
	c.addVariable("i", range(-100, 10))
	c.addVariable("j", range(-10, 10))
	c.addVariable("k", range(-10, 10))
	c.addConstraint(lambda i, j, k: i <= 0 or j <= 0 or k <= 0, ("i", "j", "k"))
	C = Constraint(c)
	values = [9, 8, -1]
	print(C.is_satisfied(values))
