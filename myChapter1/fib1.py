import sys
from typing import Dict
gcount_fab1 = 0
gcount_fab3 = 0

memo: Dict[int, int] = {0: 0, 1: 1}

def fib1(n: int) -> int:
    global gcount_fab1
    gcount_fab1 += 1
    if n < 2:
        return n
    print("fib1 total: ", gcount_fab1)
    return fib1(n - 1) + fib1(n - 2)

def fib3(n: int) -> int:
    global gcount_fab3
    gcount_fab3 += 1

    if n not in memo:
        memo[n] = fib3(n - 1) + fib3(n - 2)

    print("fib3 total: ",gcount_fab3)
    return memo[n]


if __name__ == "__main__":
    # print(fib1(int(sys.argv[1])))
    print(fib1(int(sys.argv[1])))


    print("=======================")
    print(fib3(int(sys.argv[1])))