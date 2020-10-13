import sys
from collections import defaultdict
from datetime import datetime
from functools import lru_cache
from typing import Dict, Generator

gcount_fib1 = 0
gcount_fib3 = 0
gcount_fib4 = 0
gcount_fib5 = 0
gcount_fib6 = 0

total = defaultdict(int)

memo: Dict[int, int] = {0: 0, 1: 1}


def fib1(n: int) -> int:
    global gcount_fib1
    gcount_fib1 += 1

    if n < 2:
        print("fib1 total: ", gcount_fib1)
        return n

    return fib1(n - 1) + fib1(n - 2)


def fib3(n: int) -> int:
    global gcount_fib3
    gcount_fib3 += 1

    if n not in memo:
        memo[n] = fib3(n - 1) + fib3(n - 2)

    print("fib3 total: ", gcount_fib3)
    return memo[n]


@lru_cache(maxsize=None)
def fib4(n: int) -> int:
    global gcount_fib4
    gcount_fib4 += 1

    if n < 2:
        return n

    print("fib4 total: ", gcount_fib4)
    return fib4(n - 1) + fib4(n - 2)


def fib5(n: int) -> int:
    global gcount_fib5
    if n == 0:
        return n
    last: int = 0
    next: int = 1

    for _ in range(1, n):
        gcount_fib5 += 1
        last, next = next, last + next

    print("fib5 total: ", gcount_fib5)
    return next


def fib6(n: int) -> Generator[int, None, None]:
    global gcount_fib6

    yield 0
    if n > 0: yield 1
    last: int = 0
    next: int = 1

    for _ in range(1, n):
        last, next = next, last + next
        gcount_fib6 += 1
        print("fib6(%d): %d" % (gcount_fib6 + 1, next))
        return next
        # yield next


def fib7(k):
    assert k > 0, 'K must larger than 0'
    if k in [1, 2]:
        return 1
    global total
    total[k] += 1
    return fib7(k - 1) + fib7(k - 2)


if __name__ == "__main__":
    start_time = datetime.now()
    print("fib1(20):  ", fib1(int(20)))
    print("耗时: {}".format((datetime.now() - start_time).total_seconds()))
    print("=======================")
    start_time = datetime.now()

    print("fib3: ", fib3(int(sys.argv[1])))
    print("耗时: {}".format((datetime.now() - start_time).total_seconds()))
    start_time = datetime.now()

    print("fib4 ", fib4(int(sys.argv[1])))
    print("耗时: {}".format((datetime.now() - start_time).total_seconds()))
    start_time = datetime.now()

    print("fib5 ", fib5(int(sys.argv[1])))
    print("耗时: {}".format((datetime.now() - start_time).total_seconds()))
    start_time = datetime.now()

    # print("fib6 ",fib6(int(sys.argv[1])))
    # print("耗时: {}".format((datetime.now()-start_time).total_seconds()))

    # for i in fib6(int(sys.argv[1])):
    #     print("fib6:", i)
    # pass
    print("fib7(20): {}".format(fib7(20)))
    print(total)

