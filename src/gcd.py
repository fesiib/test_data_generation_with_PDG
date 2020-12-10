# gcd
import sys

x = int(sys.argv[1])
y = int(sys.argv[2])

while y > 0:
	x, y = y, x % y

print(x)
