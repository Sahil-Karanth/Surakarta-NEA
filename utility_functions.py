import random

def oneD_to_twoD_array(lst, width):

    """returns a 2D array with the specified width from a 1D array. Each element in the 2D array is a list with a length equal to the specified width parameter."""

    return [lst[i:i+width] for i in range(0, len(lst), width)]

def twoD_to_oneD_array(lst):

    """returns a 1D array from a 2D array. Each row in the 2D array is appended to the end of the 1D array."""

    return [item for sublist in lst for item in sublist]

def shuffle_2D_array(arr):

    """returns a 2D array with the same elements as the specified 2D array but with the elements shuffled.
    Elements are shuffled between rows and columns."""
    
    width = len(arr[0])

    arr = twoD_to_oneD_array(arr)
    random.shuffle(arr)
    arr = oneD_to_twoD_array(arr, width)

    return arr


