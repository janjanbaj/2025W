# Counts number of zeros in a 1^m 0^k string where m+k = n
def bitString(a):
    n = len(a)
    lo = 0
    hi = n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        # bsearch until you are a 1 and the next element is a 0 then the answer is just the difference
        if a[mid] == "1" and a[mid + 1] == "0":
            return n - mid - 1
        if a[mid] == "0":
            hi = mid - 1
        else:
            lo = mid + 1
    return None


a = "11110"
print(a)
print(bitString(a))
