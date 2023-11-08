from multiprocessing.dummy import Pool
import time


def func():
    time.sleep(1)
    print("waited 1 second")

    return 10

if __name__ == "__main__":
    pool = Pool(processes=16)
    results = []

    with pool as p:
        for _ in range(16):
            res = p.apply_async(func)
            results.append(res)

        p.close()
        p.join()

    for res in results:
        print(res.get())

