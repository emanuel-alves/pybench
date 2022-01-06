from pybench import Benchmark
from math import sqrt


def fib_equation(n: int) -> int:
    k1 = (1 + sqrt(5)) / 2
    k2 = (1 - sqrt(5)) / 2
    return round((k1 ** n - k2 ** n) / sqrt(5))


def fib_for(n: int) -> int:
    n1, n2 = 0, 1
    if n <= 1:
        return n
    else:
        for _ in range(n):
            nth = n1 + n2
            n1 = n2
            n2 = nth
        return n1


def fib_recursive(n: int) -> int:
    if n <= 1:
        return n
    else:
        return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_recursiveMemo_iteration(n: int, arr: list = []) -> int:
    if n <= 1:
        return n
    if arr[n] == 0:
        arr[n] = fib_recursiveMemo_iteration(n - 1, arr) + fib_recursiveMemo_iteration(
            n - 2, arr
        )
    return arr[n]


def fib_recursiveMemo(n: int) -> int:
    arr = [0] * (n + 1)
    return fib_recursiveMemo_iteration(n, arr)


f1 = fib_equation
f2 = fib_for
f3 = fib_recursive
f4 = fib_recursiveMemo

Benchmark(functions=[f1, f2, f3, f4], args=[35], numTests=10).print()
