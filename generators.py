def genCountingNumbers():
    n = 0
    while True:
        yield n
        n = n + 1

f = genCountingNumbers()

for i in range(0, 15):
    print f.next()
