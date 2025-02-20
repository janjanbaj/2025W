def majority_element(A, left, right):
    # Base case: If there's only one element, it's the majority of itself
    if left == right:
        return A[left]

    mid = (left + right) // 2
    left_majority = majority_element(A, left, mid)
    right_majority = majority_element(A, mid + 1, right)

    # If both halves agree on the majority element, return it
    if left_majority == right_majority:
        return left_majority

    # Otherwise, count occurrences of both candidates
    left_count = sum(1 for i in range(left, right + 1) if A[i] == left_majority)
    right_count = sum(1 for i in range(left, right + 1) if A[i] == right_majority)

    # Check if either candidate appears more than n/2 times
    majority_threshold = (right - left) // 2
    if left_count > majority_threshold:
        return left_majority
    if right_count > majority_threshold:
        return right_majority

    return None  # No majority element


def find_majority(A):
    return majority_element(A, 0, len(A) - 1)


a = [3, 1, 2, 3]
print(find_majority(a))
a = [2, 2, 5, 2, 1, 2, 2, 3, 3]
print(find_majority(a))
