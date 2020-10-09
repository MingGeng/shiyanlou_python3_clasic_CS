
斐波那契序列（Fibonacci sequence）是一系列数字，其中除第 1 个和第 2 个数字之外，其他数字都是前两个数字之和： 0, 1, 1, 2, 3, 5, 8, 13, 21, …

在此序列中，第 1 个斐波那契数是 0。第 4 个斐波那契数是 2。后续任一斐波那契数 n 的值可用以下公式求得：

fib(n) = fib(n − 1) + fib(n − 2)

上述计算斐波那契序列数的公式是一种伪代码形式，可将其简单地转换为一个 Python 递归函数：

def fib1(n: int) -> int:
    return fib1(n - 1) + fib1(n - 2)

所谓递归函数是一种调用自己的函数。这次机械的转换将作为你编写函数的首次尝试，返回的是斐波那契序列中的给定数。

下面试着带上参数值来调用这个函数。
```Python
if __name__ == "__main__":
    print(fib1(5))
```
若我们运行 fib1.py，系统就会生成一条错误消息：

RecursionError: maximum recursion depth exceeded
copy
这里有一个问题，fib1() 将一直运行下去，而不会返回最终结果。每次调用 fib1() 都会再多调用两次 fib1()，如此反复永无止境。这种情况被称为无限递归（如下图所示），类似于无限循环（infinite loop）。




请注意，在运行 fib1() 之前，Python 运行环境不会有任何提示有错误存在。避免无限递归由程序员负责，而不由编译器或解释器负责。出现无限递归的原因是尚未指定基线条件（base case）。在递归函数中，基线条件即函数终止运行的时点。

就斐波那契函数而言，天然存在两个基线条件，其形式就是序列最开始的两个特殊数字 0 和 1。0 和 1 都不是由序列的前两个数求和得来的，而是序列最开始的两个特殊数字。那就试着将其设为基线条件吧，具体代码如下：
```Python
def fib2(n: int) -> int:
    if n < 2:  # base case
        return n
    return fib2(n - 2) + fib2(n - 1)  # recursive case
```
注意：斐波那契函数的 fib2() 版本将返回 0 作为第 0 个数 （fib2(0)），而不是第一个数，这正符合我们的本意。这在编程时很有意义，因为大家已经习惯了序列从第 0 个元素开始。

fib2() 能被调用成功并将返回正确的结果。可以用几个较小的数试着调用一下：
```Python
if __name__ == "__main__":
    print(fib2(5))
    print(fib2(10))
```
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
```
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
```
运行 fib6.py 将会打印出斐波那契序列的前 51 个数。for 循环 for i in fib6(50): 每一次迭代时，fib6() 都会一路运行至某条 yield 语句。如果直到函数的末尾也没遇到 yield 语句，循环就会结束迭代。


无论是在虚拟环境还是在现实世界，节省空间往往都十分重要。空间占用越少，利用率就越高，也会更省钱。如果租用的公寓大小超过了家中人和物所需的空间，你就可以“缩”到小一点的地方去，租金也会更便宜。如果数据存储在服务器上是按字节付费的，那么或许就该压缩一下数据，以便降低存储成本。压缩就是读取数据并对其进行编码（修改格式）的操作，以便减少数据占用的空间。解压缩则是逆过程，即把数据恢复为原始格式。

既然压缩数据的存储效率更高，那么为什么不把所有数据全部压缩一遍呢？这里就存在一个在时间和空间之间进行权衡的问题。压缩一段数据并将其解压回其原始格式需要耗费一定的时间。因此，只有在数据大小优先于数据传输速度的情况下，数据压缩才有意义。考虑一下通过互联网传输的大文件，对它们进行压缩是有道理的，因为传输文件所花的时间要比收到文件后解压的时间长。此外，为了能在服务器上存储文件而对其进行压缩所花费的时间则只需算一次。

数据类型占用的二进制位数要比其内容实际需要的多，只要意识到这一点，就可以产生最简单的数据压缩方案。例如，从底层考虑一下，如果一个永远不会超过 65535 的无符号整数在内存中被存储为 64 位无符号整数，其存储效率就很低。对此的替代方案可以是存储为 16 位无符号整数，这会让该整数实际占用的空间减少 75%（64 位换成了 16 位）。如果有数百万个这样的整数的存储效率都如此低下，那么浪费的空间累计可能会达到数兆字节。

为简单起见（当然这是一个合情合理的目标），有时候开发人员在 Python 里可以不用以二进制位方式来考虑问题。Python 没有 64 位无符号整数类型，也没有 16 位无符号整数类型。这里只有一种 int 类型，可以存储任意精度的数值。用函数 sys.getsizeof() 可以查出 Python 对象占用的内存字节数。但由于 Python 对象系统的固有开销，在 Python 3.7 中无法创建少于 28 字节（224 位）的 int 类型。每个 int 类型对象每次可以扩大 1 个二进制位（本例就会如此操作），但最少也要占用 28 字节。

注意　如果对二进制有点生疏，请记得每个二进制位就是一个 1 或 0 的值。以 2 为进制读出的一系列 1 和 0 就可以表示一个数。按照本节的讲解目标，不需要以 2 为进制进行任何数学运算，但需要理解某个数据类型的存储位数决定了它可以表示的不同数值的个数。例如，1 个二进制位可以表示 2 个值（0 或 1），2 个二进制位可以表示 4 个值（00、01、10、11），3 个二进制位则可以表示 8 个值，以此类推。

如果某个类型需要表示的不同值的数量少于存储二进制位可表示值的数量，或许存储效率就能得以提高。不妨考虑一下 DNA 中组成基因的核苷酸。每个核苷酸的值只能是这 4 种之一：A、C、G 或 T（更多相关信息将会在第 2 章中介绍）。如果基因用 str 类型存储（str 可被视作 Unicode 字符的集合），那么每个核苷酸将由 1 个字符表示，每个字符通常需要 8 个二进制位的存储空间。如果采用二进制，则有 4 种可能值的类型只需要用 2 个二进制位来存储，00、01、10 和 11 就是可由 2 个二进制位表示的 4 种不同值。如果 A 赋值为 00、C 赋值为 01、G 赋值为 10、T 赋值为 11，那么一个核苷酸字符串所需的存储空间可以减少 75%（每个核苷酸从 8 个二进制位减少到 2 个二进制位）。

因此可以不把核苷酸存储为 str 类型，而存储为位串（bit string）类型。正如其名，位串就是任意长度的一系列 1 和 0。不幸的是，Python 标准库中不包含可处理任意长度位串的现成结构体。代码清单 1-10 中的代码将把一个由 A、C、G 和 T 组成的 str 转换为位串，然后再转换回 str。位串存储在 int 类型中。因为 Python 中的 int 类型可以是任意长度，所以它可以当成任意长度的位串来使用。为了将位串类型转换回 str 类型，就需要实现 Python 的特殊方法 __str__()。

1-5 图 1-5 　将代表基因的 str 压缩为每个核苷酸占 2 位的位串

class CompressedGene:
    def __init__(self, gene: str) -> None:
        self._compress(gene)
copy
CompressedGene 类需要给定一个代表基因中核苷酸的 str 字符串，内部则将核苷酸序列存储为位串。__init__() 方法的主要职责是用适当的数据初始化位串结构体。_init__() 将调用 _compress()，将给定核苷酸 str 转换成位串的苦力活实际由 _compress() 完成。

注意，_compress() 是以下划线开头的。Python 没有真正的私有方法或变量的概念。所有变量和方法都可以通过反射访问到，Python 对它们没有严格的强制私有策略。前导下划线只是一种约定，表示类的外部不应依赖其方法的实现。这一类方法可能会发生变化，应该被视为私有方法。

提示：如果类的方法或实例变量名用两个下划线开头，Python 将会对其进行名称混淆（name mangle），通过加入盐值（salt）来改变其在实现时的名称，使其不易被其他类发现。本书用一条下划线表示“私有”变量或方法，但如果真要强调一些私有内容，或许得用两条下划线才合适。要获取有关 Python 命名的更多信息，参阅 PEP 8 中的“描述性命名风格”（Descriptive Naming Styles）部分。

下面介绍如何真正地执行压缩操作：

def _compress(self, gene: str) -> None:
    self.bit_string: int = 1  # start with sentinel
    for nucleotide in gene.upper():
        self.bit_string <<= 2  # shift left two bits
        if nucleotide == "A":  # change last two bits to 00
            self.bit_string |= 0b00
        elif nucleotide == "C":  # change last two bits to 01
            self.bit_string |= 0b01
        elif nucleotide == "G":  # change last two bits to 10
            self.bit_string |= 0b10
        elif nucleotide == "T":  # change last two bits to 11
            self.bit_string |= 0b11
        else:
            raise ValueError("Invalid Nucleotide:{}".format(nucleotide))
copy
_compress() 方法将会遍历核苷酸 str 中的每一个字符。遇到 A 就把 00 加入位串，遇到 C 则加入 01，依次类推。请记住，每个核苷酸需要两个二进制位，因此在加入新的核苷酸之前，要把位串向左移两位（self.bit_string<<= 2）。

添加每个核苷酸都是用“或”（|）操作进行的。当左移操作完成后，位串的右侧会加入两个 0。在位运算过程中，0 与其他任何值执行“或”操作（如 self.bit_string | = 0b10）的结果都是把 0 替换为该值。换句话说，就是在位串的右侧不断加入两个新的二进制位。加入的两个位的值将视核苷酸的类型而定。

下面来实现解压方法和调用它的特殊方法 __str__()：
```python
def decompress(self) -> str:
    gene: str = ""
    for i in range(0, self.bit_string.bit_length() - 1, 2):  # -1 to exclude sentinel
        bits: int = self.bit_string >> i & 0b11  # get just 2 relevant bits
        if bits == 0b00:  # A
            gene += "A"
        elif bits == 0b01:  # C
            gene += "C"
        elif bits == 0b10:  # G
            gene += "G"
        elif bits == 0b11:  # T
            gene += "T"
        else:
             raise ValueError("Invalid bits:{}".format(bits))
    return gene[::-1]  # [::-1] reverses string by slicing backward
def __str__(self) -> str:  # string representation for pretty printing
    return self.decompress()
```
decompress() 方法每次将从位串中读取两个位，再用这两个位确定要加入基因的 str 尾部的字符。与压缩时的读取顺序不同，解压时位的读取是自后向前进行的（从右到左而不是从左到右），因此最终的 str 要做一次反转（用切片表示法进行反转 [::-1]）。最后请留意一下，int 类型的 bit_length() 方法给 decompress() 的开发带来了很大便利。
```
if __name__ == "__main__":
    from sys import getsizeof
    original: str = "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATA" * 100
    print("original is {} bytes".format(getsizeof(original)))
    compressed: CompressedGene = CompressedGene(original)  # compress
    print("compressed is {} bytes".format(getsizeof(compressed.bit_string)))
    print(compressed)  # decompress
    print("original and decompressed are the same: {}".format(original ==
     compressed.decompress()))
```
利用 sys.getsizeof() 方法，输出结果时就能显示出来，通过该压缩方案确实节省了基因数据大约 75% 的内存开销：
```
original is 8649 bytes
compressed is 2320 bytes
TAGGGATTAACC…
original and decompressed are the same: True
```
注意：在 CompressedGene 类中，为了判断压缩方法和解压方法中的一系列条件，大量采用了 if 语句。
因为 Python 没有 switch 语句，所以这种情况有点儿普遍。在 Python 中有时还会出现一种情况，
就是高度依靠字典对象来代替大量的 if 语句，以便对一系列的条件做出处理。不妨想象一下，可以
用字典对象来找出每个核苷酸对应的二进制位形式。有时字典方案的可读性会更好，但可能会带来一
定的性能开销。尽管查找字典在技术上的复杂度为 O(1)，但运行哈希函数存在开销，这有时会意
味着字典的性能还不如一串 if。是否采用字典，取决于具体的 if 语句做判断时需要进行什么
计算。如果在关键代码段中要在多个 if 和查找字典中做出取舍，或许该分别对这两种方法
运行一次性能测试。


### 牢不可破的加密方案

一次性密码本（one-time pad）是一种加密数据的方法，它将无意义的随机的假数据（dummy data）混入数据中，这样在无法同时拿到加密结果和假数据的情况下就不能重建原始数据。这实质上是给加密程序配上了密钥对。其中一个密钥是加密结果，另一个密钥则是随机的假数据。单个密钥是没有用的，只有两个密钥的组合才能解密出原始数据。只要运行无误，一次性密码本就是一种无法破解的加密方案。

以下示例将用一次性密码本方案加密一个 srt。Python 3 的 str 类型有一种用法可被视为 UTF-8 字节序列（UTF-8 是一种 Unicode 字符编码）。通过 encode() 方法可将 str 转换为 UTF-8 字节序列（以 bytes 类型表示）。同理，用 bytes 类型的 decode() 方法可将 UTF-8 字节序列转换回 str。一次性密码本的加密操作中用到的假数据必须符合 3 条标准，这样最终的结果才不会被破解。假数据必须与原始数据长度相同、真正随机、完全保密。第 1 条标准和第 3 条标准是常识。如果假数据因为太短而出现重复，就有可能被觉察到规律。如果其一个密钥不完全保密（可能在其他地方被重复使用或部分泄露），那么攻击者就能获得一条线索。第 2 条标准给自己出了一道难题：能否生成真正随机的数据？大多数计算机的答案都是否定的。本例将会用到 secrets 模块的伪随机数据来生成函数 token_ bytes()（自 Python 3.6 开始包含在于标准库中）。这里的数据并非是真正随机的，因为 secrets 包在幕后采用的仍然是伪随机数生成器，但它已足够接近目标了。下面就来生成一个用作假数据的随机密钥：

```Python
from secrets import token_bytes
from typing import Tuple

def random_key(length: int) -> int:
    # generate length random bytes
    tb: bytes = token_bytes(length)
    # convert those bytes into a bit string and return it
    return int.from_bytes(tb, "big")
```
以上函数将创建一个长度为 length 字节的 int，其中填充的数据是随机生成的。int. from_bytes() 方法用于将 bytes 转换为 int。如何将多字节数据转换为单个整数呢？答案就在 1.2 节。在 1.2 节中已经介绍过 int 类型可为任意大小，而且还展示了 int 能被当作通用的位串来使用。本节以同样的方式使用 int。例如，from_bytes() 方法的参数是 7 字节（7 字节 ×8 位/字节= 56 位），该方法会将这个参数转换为 56 位的整数。为什么这种方式很有用呢？因为与对序列中的多字节进行操作相比，对单个 int（读作“长位串”）进行位操作将更加简单高效。下面将会用到 XOR 位运算。

[一次性密码体](https://doc.shiyanlou.com/courses/2654/484222/05eeb1160026c79d73bde325ddc9ef0c-0)
![图1-6 一次性密码本身会产生两个秘钥,它们可以分开存放,后续可以再组合起来以重建原始数据](https://doc.shiyanlou.com/courses/2654/484222/05eeb1160026c79d73bde325ddc9ef0c-0)
