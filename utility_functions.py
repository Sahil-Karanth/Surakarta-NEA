def oneD_to_twoD_array(lst, width):
    return [lst[i:i+width] for i in range(0, len(lst), width)]