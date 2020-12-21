# find_max

def main():
    x = int(input())
    y = int(input())
    z = int(input())

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


if __name__ == "__main__":
    main()
