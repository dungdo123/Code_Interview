def binary_search(list, item):
    low = 0
    high = len(list) -1

    while low <= high:
        mid = int((low+high)/2)
        guess = list[mid]

        if guess == item:
            return mid
        if guess > item:
            high = mid -1
        if guess < item:
            low = mid + 1
    return None
my_list = [2,3,4,5,6,7,8]
print(binary_search(my_list, 3))
print(len(my_list))