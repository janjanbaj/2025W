import random

def flip(x,i):
    b = x[0:i+1][::-1]
    for j in range(0, i+1):
        x[j] = b[j]

def findLargestIndex(x):
    maxInd = 0
    for i in range(1, len(x)):
        if x[i] > x[maxInd]:
            maxInd = i
    return maxInd

def flipPancake(x):
    l = len(x)

    for i in range(len(x) - 1, 0, -1):

        maxInd = findLargestIndex(x[0:i+1])
        # so the thing is not at the end
        if maxInd != i :
            # flip it so that its infront
            if maxInd != 0:
                flip(x, maxInd)
            flip(x, i)




def main():
    x = [random.randint(0,50) for _ in range(10)]
    print(x)
    flipPancake(x)
    print(x)





main()
