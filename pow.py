def getPow(mpl, mtlr, e):
    "Power for given number with out */built-in methods"
    "Multiplication with out built-in 3*4 = 12 it gives.\
    where mpl=3 and mtlr=4"
    mulV = 0
    for i in range(0, mtlr):
        mulV += mpl
    if e:
        return getPow(mulV, mtlr, e-1)
    else:
        return mulV


if __name__ == '__main__':
    n = input("Enter the number: ")
    e = input("Enter the Exponential number: ")
    if n == 1:
        print 1
    elif e == 1:
        print n
    elif n <= 0 or e <= 0:
        print 'sry'
    else:
        print getPow(n, n, e-2), 'Observed'
        print pow(n, e), 'actual'
