from itertools import (takewhile, dropwhile, chain, islice)
from functools import reduce
from typing import Iterable, Callable, TypeVar, Generic

A = TypeVar("A")
B = TypeVar("B")


class Stream(Generic[A]):
    def __init__(self, xs: Iterable[A]):
        self.xs = xs

    def __iter__(self) -> Iterable[A]:
        yield from self.xs

    @staticmethod
    def of(*args: A):
        return Stream(args)

    def map(self, f: Callable[[A], B]) -> 'Stream[B]':
        return Stream(map(f, self.xs))

    def filter(self, p: Callable[[A], bool]) -> 'Stream[A]':
        return Stream(filter(p, self.xs))

    def bind(self, f: Callable[[A], 'Stream[B]']) -> 'Stream[B]':
        return Stream(chain.from_iterable(map(f, self.xs)))

    def reduce(self, f: Callable[[A], 'Stream[B]']) -> 'Stream[B]':
        return Stream(reduce(f, self.xs))

    def take(self, n: int) -> 'Stream[A]':
        return Stream(islice(self.xs, n))

    def drop(self, n: int) -> 'Stream[A]':
        return Stream(islice(self.xs, n, None))

    def takewhile(self, p: Callable[[A], bool]) -> 'Stream[A]':
        return Stream(takewhile(p, self.xs))

    def dropwhile(self, p: Callable[[A], bool]) -> 'Stream[A]':
        return Stream(dropwhile(p, self.xs))

    def collect(self, to: Callable[[Iterable[A]], Iterable[A]]) -> Iterable[A]:
        return to(list(self.xs))

    @property
    def sort(self, key=None):
        return Stream(sorted(self.xs, key=key))

    @property
    def count(self):
        return sum(1 for x in self.xs)

    @property
    def sum(self):
        return sum(self.xs)

    @property
    def max(self, key=None):
        return max(self.xs, key=key)

    @property
    def distinct(self, key=None):
        key = (lambda x: x) if key is None else key
        S = set()
        for x in self.xs:
            key_x = key(x)
            if key_x not in S:
                yield x
            S.add(key_x)
