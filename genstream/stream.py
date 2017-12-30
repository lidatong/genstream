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

    def head(self):
        return next(self.xs)

    def tail(self):
        next(self.xs)
        return Stream(self.xs)

    def map(self, f: Callable[[A], B]) -> 'Stream[B]':
        return Stream(map(f, self.xs))

    def filter(self, p: Callable[[A], bool]) -> 'Stream[A]':
        return Stream(filter(p, self.xs))

    def bind(self, f: Callable[[A], 'Stream[B]']) -> 'Stream[B]':
        return Stream(chain.from_iterable(map(f, self.xs)))

    def reduce(self, f: Callable[[A, 'Stream[B]'], 'B']) -> 'B':
        return reduce(f, self.xs)

    def concat(self, ys):
        return Stream(chain(self.xs, ys))

    def take(self, n: int) -> 'Stream[A]':
        return Stream(islice(self.xs, n))

    def drop(self, n: int) -> 'Stream[A]':
        return Stream(islice(self.xs, n, None))

    def takewhile(self, p: Callable[[A], bool]) -> 'Stream[A]':
        return Stream(takewhile(p, self.xs))

    def dropwhile(self, p: Callable[[A], bool]) -> 'Stream[A]':
        return Stream(dropwhile(p, self.xs))

    # Key functions reserved for situations in which a preceding .map to the op
    # would not evaluate to the same result

    def sort(self, key=None):
        return Stream(sorted(self.xs, key=key))

    # built-ins max/min don't handle key=None properly

    def max(self, key=None):
        key = (lambda x: x) if key is None else key
        return Stream(max(self.xs, key=key))

    def min(self, key=None):
        key = (lambda x: x) if key is None else key
        return Stream(min(self.xs, key=key))

    def distinct(self, key=None):
        key = (lambda x: x) if key is None else key

        def g():
            S = set()
            for x in self.xs:
                key_x = key(x)
                if key_x not in S:
                    yield x
                S.add(key_x)

        return Stream(g())

    # Terminal operations

    def collect(self, to: Callable[[Iterable[A]], Iterable[A]]) -> Iterable[A]:
        return to(self.xs)

    def sum(self):
        return sum(self.xs)

    def any(self):
        return any(self.xs)

    def all(self):
        return all(self.xs)

    def count(self):
        return sum(1 for _ in self.xs)


if __name__ == '__main__':
    print(Stream.of(1, 2, 3).concat(Stream.of(4, 5, 6)).collect(list))
    print(Stream.of(1, 2, 3).reduce(max))
    print(Stream.of(1, 2, 3).count())
    print(Stream.of(1, 2, 3).max())
    print(Stream.of(1, 5, 2, 2).distinct().collect(list))
