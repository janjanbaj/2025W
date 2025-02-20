import random


def minMax(a):
    n = len(a)
    if n == 1:
        return a[0], a[0]
    m = n // 2
    min1, max1 = minMax(a[0:m])
    min2, max2 = minMax(a[m:])
    return min(min1, min2), max(max1, max2)

def maxDifference(a):
    min1, max1 = minMax(a)
    return max1 - min1


a = [random.randint(0, 40) for _ in range(10)]
print(a)
print(minMax(a))
print(f"Max Difference: {maxDifference(a)}")
