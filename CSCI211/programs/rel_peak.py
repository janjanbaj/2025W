
import random


def relpeak(arr, i, j):
    if j - i < 0:
        return arr[i]
    mid = (i + j)//2
    if arr[mid] < arr[mid-1]:
        return relpeak(arr, 0, mid)
    elif arr[mid] < arr[mid+1]:
        return relpeak(arr,mid+1, j)
    else:
        return arr[mid]




if __name__ == "__main__":
    arr = [i for i in range(1, 11)]
    random.shuffle(arr)
    print(arr)
    print(relpeak(arr, 0 , 10))



