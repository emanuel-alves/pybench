import sys
from os import devnull

from typing import List
from types import FunctionType
from statistics import mean, pstdev

from copy import deepcopy
from time import perf_counter_ns
from typing import List
from types import FunctionType


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class BenchmarkData:
    __times: List[int]

    def __init__(self, function: FunctionType):
        """Data class for handling benchmarks.

        Args:
            function (FunctionType): Function used in tests.
        """
        self.function = function
        self.__times = []

    def __lt__(self, other):
        return self.mean < other.mean

    @property
    def mean(self) -> float:
        """Returns the mean of the times (Population).

        Returns:
            float: Mean of times in nanoseconds.
        """
        if len(self.times) > 1:
            return mean(self.times)
        return self.times[0] if len(self.times) else 0

    @property
    def deviation(self) -> float:
        """Returns the standard deviation (Population).

        Returns:
            float: Standard deviation of times in nanoseconds.
        """
        if len(self.times) > 1:
            return pstdev(self.times)
        return 1 if len(self.times) else 0

    @property
    def times(self):
        """Return time list.

        Returns:
            List[int]: Time list.
        """
        return self.__times

    def setTimes(self, newTime: int):
        """Add new time.

        Args:
            newTime (int): Time in nanoseconds.
        """
        self.__times.append(newTime)

    def sum(self) -> int:
        """Sum of recorded times.

        Returns:
            Time sam in nanoseconds.
        """
        return sum(self.__times)

    def reset(self):
        """Clean of recorded times."""
        self.times.clear()


class Benchmark:
    __benchs: List[BenchmarkData] = []
    __args: list = []
    __countBenchmark: int = 0
    nothing = [object()]

    def __init__(self, functions: List[FunctionType], args: list = [], numTests=0):
        """Class to perform function benchmark.

        Args:
            functions (List[FunctionType]): List of functions for the benchmark.
            args (list, optional): List of arguments for the benchmark. Defaults to [].
            numTests (int, optional): Number of tests performed. Defaults to 0.
        """
        self.__countBenchmark = 0
        self.__args = deepcopy(args)
        for function in functions:
            self.__benchs.append(BenchmarkData(function))
        self.testing(numTests)

    def testingElement(self, function: FunctionType, args: list = []) -> int:
        """Performs the test of a specific element.

        Args:
            function (FunctionType): Function used for benchmark.
            args (list): List of arguments for the benchmark. Defaults to [].

        Returns:
            int: Time in nanoseconds used by the function.
        """
        try:
            with HiddenPrints():
                argsCopy = deepcopy(args)
                speedTest = perf_counter_ns()
                function(*argsCopy)
                return perf_counter_ns() - speedTest
        except:
            print("ERROR: function <%s>" % function.__name__)
            return 0

    def testing(self, numTests=1):
        """Performs the benchmark with the functions and arguments entered in the class.

        Args:
            numTests (int, optional):  Number of tests performed. Defaults to 1.
        """
        for _ in range(numTests):
            self.__countBenchmark += 1
            for data in self.__benchs:
                data.setTimes(self.testingElement(data.function, self.__args))
        self.__sort()

    def reset(self) -> None:
        """Clear the tests performed by keeping the arguments and functions entered."""
        for itens in self.__benchs:
            itens.reset()

    def removeArg(self, args: list = nothing) -> None:
        """Remove one or more arguments. Defaults remove all arguments.

        Args:
            args (list, optional): Arguments to be removed. Defaults to nothing.
        """
        if args == self.nothing:
            self.__args.clear()
        self.__args = [arg for arg in self.__args if arg not in args]

    def setArgs(self, args: list) -> None:
        """Inserts new arguments. Remove all previously entered arguments.

        Args:
            args (list): List of arguments to be entered.
        """
        self.__args = deepcopy(args)

    def addArgs(self, args: list) -> None:
        """Adds new arguments. Does not remove previously entered arguments.

        Args:
            args (list): List of arguments to add.
        """
        self.__benchs.extend(deepcopy(args))

    def getResults(self) -> List[List[object]]:
        """Returns benchmark results.

        Returns:
            List[[FunctionType, int]]: Benchmark list, returns function and time spent in nanoseconds.
        """
        self.__sort()
        return [[item.function, item.mean] for item in self.__benchs]

    def __sort(self) -> None:
        """Sort the benchmarks."""
        self.__benchs = sorted(self.__benchs)

    def getArgs(self):
        """Returns list of arguments entered.

        Returns:
            list: Argument list.
        """
        return self.__args

    @property
    def best(self):
        """The best result (shortest time). If no test has occurred, the return will be self.nothing.

        Returns:
            functionType: function with the shortest time.
        """
        if self.__countBenchmark and len(self.__benchs):
            return self.__benchs[0].function
        else:
            return self.nothing

    @property
    def worst(self):
        """The worst result (longer time). If no test has occurred, the return will be self.nothing.

        Returns:
            functionType: function with the longer time.
        """
        if self.__countBenchmark and len(self.__benchs):
            return self.__benchs[-1].function
        else:
            return self.nothing

    def print(self) -> None:
        """Show some test data"""
        print(self.__str__())

    def __str__(self) -> str:
        """Return some test data

        Returns:
            str: String for print.
        """
        if self.__countBenchmark:
            allMean = all = 0
            aux = ""
            string__benchs = ""

            string__benchs += "---------------------Benchmark---------------------\n"
            string__benchs += "Numero de testes: %d\n" % (self.__countBenchmark)
            string__benchs += "Numero de funções: %d\n" % (len(self.__benchs))

            for data in self.__benchs:
                allMean += data.mean
                all += data.sum()
                aux += "\t%s: (%f ± %f) s\n" % (
                    data.function.__name__,
                    data.mean / 1e9,
                    data.deviation / 1e9,
                )

            string__benchs += "Total Mean: %f s\n" % (allMean / 1e9)
            string__benchs += "Total     : %f s\n" % (all / 1e9)

            string__benchs += "Best result: <%s> with mean %fs\n" % (
                self.__benchs[0].function.__name__,
                self.__benchs[0].mean / 1e9,
            )
            string__benchs += "Worst result: <{}> with mean {:f}s\n".format(
                self.__benchs[-1].function.__name__,
                self.__benchs[-1].mean / 1e9,
            )

            string__benchs += "\nTestes:"
            string__benchs += aux
        else:
            string__benchs = "No benchmark performed..."
        return string__benchs
