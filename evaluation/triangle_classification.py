# tri





def classify(i, j, k):
    if i <= 0 or j <= 0 or k <= 0:
        return 4

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
        return tri

    
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
    return tri


def main():
    a = int(input())
    b = int(input())
    c = int(input())

    t = classify(a, b, c)

    print(t)


if __name__ == "__main__":
    main()
