import random



def findMaxIndex(row):
    maxInd = 0
    for i in range(1, len(row)):
        if row[i] > row[maxInd]:
            maxInd = i
    return maxInd

def twoDPeak(mat):

    center = len(mat) // 2

    maxIndx = findMaxIndex(mat[center])

    if center != 0 and mat[center][maxIndx] < mat[center-1][maxIndx]:
        return twoDPeak(mat[0:maxIndx])
    elif center == len(mat) - 1 and mat[center][maxIndx] < mat[center+1][maxIndx]:
        return twoDPeak(mat[maxIndx:])
    return (center, maxIndx)



def pprintMat(mat):
    print("[")
    for row in mat:
        print(row)
    print("]")

if __name__ == "__main__":
    n = 10
    mat = [[random.randint(0,5) for _ in range(n)] for _ in range(n)]
    pprintMat(mat)
    print(twoDPeak(mat))
