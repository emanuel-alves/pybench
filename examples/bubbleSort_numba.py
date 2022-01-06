from typing import Sized
from pybench import Benchmark

import numba as nb
from random import randrange
import numpy as np


def bubbleSort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


@nb.jit()
def bubbleSort_numba1(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


@nb.jit(nopython=True)
def bubbleSort_numba2(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


@nb.jit(nopython=True, fastmath=True)
def bubbleSort_numba3(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


@nb.jit(nopython=True, fastmath=True, cache=True)
def bubbleSort_numba4(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


maxItens = 10000
interval = 10000
numTests = 10
arr = np.random.randint(low=-interval, high=interval, size=maxItens)

bench = Benchmark(
    functions=[bubbleSort, bubbleSort_numba1, bubbleSort_numba2, bubbleSort_numba3],
    args=[arr],
    numTests=numTests,
)
print(bench)
