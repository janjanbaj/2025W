import random

N = 10


# given 0-n-1 numbers where one of the numbers is missing in an unsorted list, we find it using
def missing(a, pPivot=0):
    if len(a) == 0:
        return pPivot  # Base case: the missing number is found

    pivot = a[0]  # Choose pivot (this choice is arbitrary)

    left = [i for i in a if i < pivot]
    right = [i for i in a if i > pivot]

    left_size = len(left)  # Number of elements in left partition
    expected_left_size = pivot - pPivot  # Expected count of elements in left

    if left_size == expected_left_size:
        # If left partition has the expected count, search in right
        return missing(right, pivot + 1)
    else:
        # Otherwise, search in left
        return missing(left, pPivot)


a = [i for i in range(10)]
# a.pop(random.randint(0, N - 1))
print(a)
random.shuffle(a)

print(missing(a))
