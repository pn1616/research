def find_max(arr):
    if not arr:
        raise ValueError("Input list is empty.")
    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val
