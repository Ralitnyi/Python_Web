from multiprocessing import Pool
from time import time


# def factorize(*numbers):
    
#     result = []
    
#     for num in numbers:
#         res = []
#         for i in range(1, max(numbers) + 1):
#             if not num % i:
#                 res.append(i)

#         result.append(res)
#     return result    

# start = time()
# a, b, c, d  = factorize(128, 255, 99999, 10651060)
# print(time() - start) # 1.86

# assert a == [1, 2, 4, 8, 16, 32, 64, 128]
# assert b == [1, 3, 5, 15, 17, 51, 85, 255]
# assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
# assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]


def worker(num):
    res = []
    for i in range(1, num + 1):
        if not num % i:
            res.append(i)
    return res


def factorize(numbers):
    
    with Pool(processes=1) as pool:
        result = list(pool.map(worker, numbers))
    return result
  
if __name__ == '__main__':
    start = time()
    a, b, c, d  = factorize((128, 255, 99999, 10651060))
    print(time() - start)
    """
    Befor pool time = 1.86, after pool time = 0.63
    """

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]