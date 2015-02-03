def main():
    "Cube for given number with out */built-in method"
    n = input("Enter the number: ")
    c = 0
    for i in range(0, n):
        for j in range(0, n):
            c += n
    print c

if __name__ == '__main__':
    main()
