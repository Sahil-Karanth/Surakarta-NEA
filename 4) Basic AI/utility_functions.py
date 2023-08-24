import random
from copy import deepcopy

def oneD_to_twoD_array(lst, width):
    return [lst[i:i+width] for i in range(0, len(lst), width)]

def shuffle_2D_array(arr):

    # ! IMPROVE THIS TO SHUFFLE BETWEEN ROWS AS WELL
    
    arr_copy = deepcopy(arr)

    random.shuffle(arr_copy)

    for row in arr_copy:
        random.shuffle(row)

    return arr_copy
