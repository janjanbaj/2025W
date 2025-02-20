import random


def mergeSort(arr, count):
    def merge(arr1, arr2):
        if len(arr1) == 0:
            return arr2
        elif len(arr2) == 0:
            return arr1
        elif arr1[0] <= arr2[0]:
            return [arr1[0]] + merge(arr1[1:], arr2)
        else:
            count[0] += len(arr1)
            return [arr2[0]] + merge(arr1, arr2[1:])

    if len(arr) < 2:
        return arr
    else:
        h = len(arr) // 2
        return merge(mergeSort(arr[:h], count), mergeSort(arr[h:], count))


def inversionCount(arr):
    count = 0
    for i in range(len(arr) - 1):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                count += 1
    print(f"Brute Force: {count}")
    return


a1 = [random.randint(0, 10) for _ in range(random.randint(5, 20))]
b1 = a1.copy()
# a1 = [1,3,5,10,2,6,8,9]
count = [0]
a2 = mergeSort(a1, count)
print(a2)
inversionCount(b1)
print(count)
