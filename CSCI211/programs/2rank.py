import random


def bsearch(arr, target):
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    # return the index where it should be
    return low


def bsearch2(x, y, rank, carry=0):
    # assume rank item is in the x array
    xx = len(x) // 2
    yy = rank - xx - 1 + carry
    print(f"Search: {x} | {y} | {xx},{yy}")

    if len(x) == 0:
        return False

    if yy == -1:
        # if yy is going to contribute 1 item then it must be smaller than x[xx]
        if x[xx] < y[yy]:
            return x[xx]
        return False

    if yy < 0:
        return x[xx]

    # our rank is too small, recurse right
    if y[yy] > x[xx]:
        return bsearch2(x[xx + 1 :], y, rank, carry + xx)

    # our rank is too big, recurse left
    if y[yy + 1] < x[xx]:
        return bsearch2(x[0:xx], y, rank, 0)

    # our rank is the answer:
    return x[xx]


def rank2(a1, a2, rank):
    x = a1[0 : rank + 1]
    y = a2[0 : rank + 1]

    ans = bsearch2(x, y, rank)
    if ans is False:
        ans = bsearch2(y, x, rank)
    return ans

    # when we have r rank item we have r-1 items left of it
    # r - 1 = xx + yy implies yy = r - 1 - xx


# def peak2d(a1, a2, rank):
#    # if the rank is greater than or equal to the sum of two lists combined then
#    # thats a problem
#    if rank >= len(a1) + len(a2):
#        return None
#
#    print(f"Searching for Rank: {rank}")
#
#    b1 = a1[0 : rank]
#    b2 = a2[0 : rank]
#
#    o = 0
#    t = 0
#
#    while True:
#        print(f"In: {b1[o:]} | {b2[t:]} o:{o} t:{t}")
#
#        if o + t == rank:
#            print(f"o :{o} | t: {t}")
#            if len(b1) > o and len(b2) > t:
#                return min(b1[o], b2[t])
#            if len(b1) <= o:
#                return b2[t]
#            return b1[o]
#
#        if t >= len(b2):
#            o += 1
#            continue
#        if o >= len(b1):
#            t += 1
#            continue
#
#        if b1[o] < b2[t]:
#            ind = bsearch(b1, b2[t])
#            if ind < t - rank:
#                o = ind
#            else:
#                o += 1
#
#        elif b1[o] > b2[t]:
#            ind = bsearch(b2, b1[o])
#            if ind < o - rank:
#                t = ind
#            else:
#                t += 1
#        else:
#            o += 1


def main():
    size = 5
    print(f"For Size: {size}")
    all = random.sample(range(size * 3), size * 2)
    a1 = sorted(all[0:size])
    a2 = sorted(all[size:])
    rank = random.randint(0, size * 2 - 1)
    # rank = 0
    print(a1)
    print(a2)
    print(f"Sorted: {sorted(a1 + a2)}")
    ans = rank2(a1, a2, rank)
    print(ans)
    print(f"Answer: {sorted(a1 + a2)[rank]}")


if __name__ == "__main__":
    main()
