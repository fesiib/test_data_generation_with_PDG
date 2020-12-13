# find_max
import sys

x = int(sys.argv[1])
y = int(sys.argv[2])
z = int(sys.argv[3])

if x > y:
	if y > z:
		print(x)
	else:
		if x > z:
			print(x)
		else:
			print(z)
else:
	if x > z:
		print(y)
	else:
		if y > z:
			print(y)
		else:
			print(z)
