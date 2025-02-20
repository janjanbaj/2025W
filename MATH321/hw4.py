import math
import typst_tables


def q2():
    n = 32
    s = [i for i in range(1, n) if math.gcd(n, i) == 1]  # rel prime

    cayley_table = [[j] + [(i * j) % n for i in s] for j in s]
    cayley_table.insert(0, ["op"] + [i for i in s])

    print("---")
    for i in s:
        a = [i]
        while True:
            if (a[-1] * i) % n in a:
                break
            else:
                a.append((a[-1] * i) % n)
        print(a)
    print("---")

    print(typst_tables.typstTables(cayley_table))


def q3():
    n = 8
    s = [i for i in range(1, 31)]
    order = {}
    for i in s:
        a = [i]
        while True:
            if (a[-1] + i) % n in a:
                break
            else:
                a.append((a[-1] + i) % n)
        a.sort()
        order_current = len(a)
        if order_current not in order:
            order[order_current] = []
        order[order_current].append(i)
        # print(f"+ $ al {i} ar = [{','.join(map(str, a))}], abs(al {i} ar) = {len(a)} $")

    for row in order:
        print(row, order[row])


q2()
