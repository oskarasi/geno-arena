def binary_search(xs, target: int) -> int:
    lo = 0
    hi = len(xs) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if xs[mid] == target:
            return mid
        if xs[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
