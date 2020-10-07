
斐波那契序列（Fibonacci sequence）是一系列数字，其中除第 1 个和第 2 个数字之外，其他数字都是前两个数字之和： 0, 1, 1, 2, 3, 5, 8, 13, 21, …

在此序列中，第 1 个斐波那契数是 0。第 4 个斐波那契数是 2。后续任一斐波那契数 n 的值可用以下公式求得：

fib(n) = fib(n − 1) + fib(n − 2)

上述计算斐波那契序列数的公式是一种伪代码形式，可将其简单地转换为一个 Python 递归函数：

def fib1(n: int) -> int:
    return fib1(n - 1) + fib1(n - 2)

所谓递归函数是一种调用自己的函数。这次机械的转换将作为你编写函数的首次尝试，返回的是斐波那契序列中的给定数。

下面试着带上参数值来调用这个函数。

if __name__ == "__main__":
    print(fib1(5))
copy
若我们运行 fib1.py，系统就会生成一条错误消息：

RecursionError: maximum recursion depth exceeded
copy
这里有一个问题，fib1() 将一直运行下去，而不会返回最终结果。每次调用 fib1() 都会再多调用两次 fib1()，如此反复永无止境。这种情况被称为无限递归（如下图所示），类似于无限循环（infinite loop）。




请注意，在运行 fib1() 之前，Python 运行环境不会有任何提示有错误存在。避免无限递归由程序员负责，而不由编译器或解释器负责。出现无限递归的原因是尚未指定基线条件（base case）。在递归函数中，基线条件即函数终止运行的时点。

就斐波那契函数而言，天然存在两个基线条件，其形式就是序列最开始的两个特殊数字 0 和 1。0 和 1 都不是由序列的前两个数求和得来的，而是序列最开始的两个特殊数字。那就试着将其设为基线条件吧，具体代码如下：

def fib2(n: int) -> int:
    if n < 2:  # base case
        return n
    return fib2(n - 2) + fib2(n - 1)  # recursive case
copy
注意：斐波那契函数的 fib2() 版本将返回 0 作为第 0 个数 （fib2(0)），而不是第一个数，这正符合我们的本意。这在编程时很有意义，因为大家已经习惯了序列从第 0 个元素开始。

fib2() 能被调用成功并将返回正确的结果。可以用几个较小的数试着调用一下：

if __name__ == "__main__":
    print(fib2(5))
    print(fib2(10))
copy
请勿尝试调用 fib2(50)，因为它永远不会终止运行！每次调用 fib2() 都会再调用两次 fib2()，方式就是递归调用 fib2(n - 1) 和 fib2(n - 2)（如图 1-3 所示）。换句话说，这种树状调用结构将呈指数级增长。例如，调用 fib2(4) 将产生如下一整套调用：

fib2(4) -> fib2(3), fib2(2)
fib2(3) -> fib2(2), fib2(1)
fib2(2) -> fib2(1), fib2(0)
fib2(2) -> fib2(1), fib2(0)
fib2(1) -> 1
fib2(1) -> 1
fib2(1) -> 1
fib2(0) -> 0
fib2(0) -> 0
copy
不妨来数一下（如果加入几次打印函数调用即可看明白），仅为了计算第 4 个元素就需要调用 9 次 fib2()！情况会越来越糟糕，计算第 5 个元素需要调用 15 次，计算第 10 个元素需要调用 117 次，计算第 20 个元素需要调用 21891 次。我们应该能改善这种情况。

1-3






结果缓存（memoization）是一种缓存技术，即在每次计算任务完成后就把结果保存起来，这样在下次需要时即可直接检索出结果，而不需要一而再再而三地重复计算。

下面创建一个新版的斐波那契函数，利用 Python 的字典对象作为结果缓存：
```
from typing import Dict
memo: Dict[int, int] = {0: 0, 1: 1}  # our base cases

def fib3(n: int) -> int:
    if n not in memo:
        memo[n] = fib3(n - 1) + fib3(n - 2)  # memoization
    return memo[n]
```

#现在就可以放心地调用 fib3(50) 了：

```

if __name__ == "__main__":
    print(fib3(5))
    print(fib3(50))

```
现在一次调用 fib3(20) 只会产生 39 次 fib3() 调用，而不会像调用 fib2(20) 那样产生 21891 次 fib2() 调用。memo 中预填了之前的基线条件 0 和 1，并加了一条 if 语句大幅降低了 fib3() 的计算复杂度。



还可以对 fib3() 做进一步的简化。Python 自带了一个内置的装饰器（decorator），可以自动为任何函数缓存结果。在 fib4() 中，装饰器 @functools.lru_cache() 所用的代码与 fib2() 中所用的代码完全相同。每次用新的参数执行 fib4() 时，该装饰器就会把返回值缓存起来。以后再用相同的参数调用 fib4() 时，都会从缓存中读取该参数对应的 fib4() 之前的返回值并返回。
```
from functools import lru_cache

@lru_cache(maxsize=None)
def fib4(n: int) -> int:  # same definition as fib2()
    if n < 2:  # base case
        return n
    return fib4(n - 2) + fib4(n - 1)  # recursive case

if __name__ == "__main__":
    print(fib4(5))
    print(fib4(50))
```
注意，虽然以上斐波那契函数体部分与 fib2() 中的函数体部分相同，但能立刻计算出 fib4(50) 的结果。@lru_cache 的 maxsize 属性表示对所装饰的函数最多应该缓存多少次最近的调用结果，如果将其设置为 None 就表示没有限制。



还有一种性能更好的做法，即可以用老式的迭代法来解决斐波那契问题，如代码所示。
```
def fib5(n: int) -> int:
    if n == 0: return n  # special case
    last: int = 0  # initially set to fib(0)
    next: int = 1  # initially set to fib(1)
    for _ in range(1, n):
        last, next = next, last + next
    return next

if __name__ == "__main__":
    print(fib5(5))
    print(fib5(50))
```
警告：fib5() 中的 for 循环体用到了元组（tuple）解包操作，或许这有点儿过于卖弄了。有些人可能会觉得这是为了简洁而牺牲了可读性，还有些人可能会发现简洁本身就更具可读性，这里的要领就是 last 被设置为 next 的上一个值，next 被设置为 last 的上一个值加上 next 的上一个值。这样在 last 已更新而 next 未更新时，就不用创建临时变量以存储 next 的上一个值了。以这种形式使用元组解包来实现某种变量交换的做法在 Python 中十分常见。

以上方案中，for 循环体最多会运行 n-1 次。换句话说，这是效率最高的版本。为了计算第 20 个斐波那契数，这里的 for 循环体只运行了 19 次，而 fib2() 则需要 21891 次递归调用。对现实世界中的应用程序而言，这种强烈的反差将会造成巨大的差异！

递归解决方案是反向求解，而迭代解决方案则是正向求解。有时递归是最直观的问题解决方案。例如，fib1() 和 fib2() 的函数体几乎就是原始斐波那契公式的机械式转换。然而直观的递归解决方案也可能伴随着巨大的性能损耗。请记住，能用递归方式求解的问题也都能用迭代方式来求解。

## 用生成器生成斐波那契数

到目前为止，已完成的这些函数都只能输出斐波那契序列中的单个值。如果要将到某个值之前的整个序列输出，又该怎么做呢？用 yield 语句很容易就能把 fib5() 转换为 Python 生成器。在对生成器进行迭代时，每轮迭代都会用 yield 语句从斐波那契序列中吐出一个值：

from typing import Generator

def fib6(n: int) -> Generator[int, None, None]:
    yield 0  # special case
    if n > 0: yield 1  # special case
    last: int = 0  # initially set to fib(0)
    next: int = 1  # initially set to fib(1)
    for _ in range(1, n):
        last, next = next, last + next
        yield next  # main generation step

if __name__ == "__main__":
    for i in fib6(50):
        print(i)
copy
运行 fib6.py 将会打印出斐波那契序列的前 51 个数。for 循环 for i in fib6(50): 每一次迭代时，fib6() 都会一路运行至某条 yield 语句。如果直到函数的末尾也没遇到 yield 语句，循环就会结束迭代。