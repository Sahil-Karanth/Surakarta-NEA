import random

def oneD_to_twoD_array(lst, width):
    return [lst[i:i+width] for i in range(0, len(lst), width)]

def shuffle_2D_array(arr):
    
    arr_copy = arr.copy()

    random.shuffle(arr_copy)

    for row in arr_copy:
        random.shuffle(row)

    return arr_copy