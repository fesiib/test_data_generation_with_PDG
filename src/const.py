"""
Constant Values
"""
import math

DEF_SEED_SIZE = 10
DEF_POP_SIZE = 100
DEF_RATE_CROSSOVER = 0.4
DEF_RATE_MUTATION = 0.4
DEF_MAX_ITER = 100
DEF_WAIT_ITER = 20
DEF_DEPENDENCY_MODE = 3
DEF_INF = math.inf
DEF_DOM = 10

"""
0 - [int, int]
1 - [int, int, int]
2 - #ints, [int, int, ... int]
"""
DEF_TEST_TYPE = 0


SEED_SIZES = [10, 30, 50]
POP_SIZES = [20, 50, 100]
RATES_CROSSOVER = [0.1, 0.2, 0.4]
RATES_MUTATION = [0.1, 0.2, 0.4]
MAX_ITERS = [20, 50, 100]
WAIT_ITERS = [5, 10, 20]
DEPENDENCY_MODES = [1, 2, 3]
