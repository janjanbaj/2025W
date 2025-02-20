from math import log2
import random


class Liar:
    def __init__(self, strategy=0):
        self.strategy = strategy

    def answer(self, other):
        # pessimal case, always return True
        if self.strategy == 0:
            return True
        if self.strategy == 1:
            return random.randint(0, 1) == 1
        return False

    def __str__(self):
        return "Liar"


class Honest:
    def __init__(self, strategy):
        return

    def answer(self, other):
        return type(other) is type(self)

    def __str__(self):
        return "Honest"


def ask(p1, p2):
    return p1.answer(p2) and p2.answer(p1)


def alg(a1):
    n = len(a1)
    if n % 2 != 0:
        pickout = a1[-1]
        count = 0

        for err in a1[:-1]:
            if err.answer(pickout):
                count += 1

        if count >= n // 2:
            return pickout
        a1.pop()
        n -= 1
    # must be even here: half the people such that you always have more truth tellers than liars
    result = [a1[i] for i in range(0, n, 2) if ask(a1[i], a1[i + 1])]
    return alg(result)


# def alg(a1):
#    print(f"{[str(i) for i in a1]}")
#    n = len(a1)
#    if n <= 2:
#        return a1[0]
#    if n == 3:
#        sitout = a1[0]
#        remaining = a1[1:]
#        if remaining[0].answer(sitout) or remaining[1].answer(sitout):
#            return sitout
#        return remaining[0]
#    # if even then pair up every consecutive pair
#    if n % 2 == 0:
#        result = [a1[i] for i in range(0, n, 2) if ask(a1[i], a1[i + 1])]
#        print(f"{result} | {n}")
#        return alg(result)
#    else:
#        sitout = a1[0]
#        result = [a1[i] for i in range(1, n, 2) if ask(a1[i], a1[i + 1])]
#        print(f"Size: {len(result)} | N={n}")
#        return alg([sitout] + result)


types = [Liar, Honest]
num_of_honest = random.randint(2, 100)
num_of_liars = random.randint(1, num_of_honest - 1)
print(f"Liars: {num_of_liars} | Honest: {num_of_honest}")
a1 = [Honest(0) for _ in range(num_of_honest)] + [Liar(1) for _ in range(num_of_liars)]
random.shuffle(a1)
answer = alg(a1)
print(f"We found the: {answer}")
if type(answer) is Liar:
    print([str(i) for i in a1])
