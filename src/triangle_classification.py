# tri
import sys

i = int(sys.argv[1])
j = int(sys.argv[2])
k = int(sys.argv[3])

if i <= 0 or j <= 0 or k <= 0:
	print(4)
	exit()

tri = 0
if i == j:
	tri += 1
if i == k:
	tri += 2
if j == k:
	tri += 3

if tri == 0:
	if i + j < k or j + k < i or k + i < j:
		tri = 4
	else:
		tri = 1
	print(tri)
	exit()

if tri > 3:
	tri = 3
elif tri == 1 and i + j > k:
	tri = 2
elif tri == 2 and i + k > j:
	tri = 2
elif tri == 3 and j + k > i:
	tri = 2
else:
	tri = 4

print(tri)
exit()