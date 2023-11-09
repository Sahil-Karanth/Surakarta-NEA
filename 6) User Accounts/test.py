from multiprocessing.dummy import Pool
import time
import random
from copy import deepcopy

master_lst = [1,2,3,4,5,6]

def func(x):
    lst = deepcopy(master_lst)
    lst[0], lst[-1] = lst[-1], lst[0]

    return lst


if __name__ == "__main__":
    
    pool = Pool(processes=16)
    results = []

    with pool as p:
        for _ in range(16):
            res = p.apply_async(func, (3,))
            results.append(res)

        p.close()
        p.join()

    for res in results:
        print(res.get())

