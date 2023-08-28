import random
from copy import deepcopy

def oneD_to_twoD_array(lst, width):
    return [lst[i:i+width] for i in range(0, len(lst), width)]

def twoD_to_oneD_array(lst):
    return [item for sublist in lst for item in sublist]

def shuffle_2D_array(arr):

    # ! IMPROVE THIS TO SHUFFLE BETWEEN ROWS AS WELL
    
    arr_copy = deepcopy(arr)

    arr = twoD_to_oneD_array(arr)
    random.shuffle(arr)
    arr = oneD_to_twoD_array(arr, len(arr_copy[0]))

    return arr


