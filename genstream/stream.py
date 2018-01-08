from itertools import (takewhile,
                       dropwhile,
                       chain,
                       islice,
                       tee,
                       filterfalse,
                       zip_longest)
from functools import reduce
from typing import Iterable, Callable, TypeVar, Generic

A = TypeVar("A")
B = TypeVar("B")


class Stream(Generic[A]):
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Iterable):
            self._xs = iter(args[0])
        else:
            self._xs = iter(args)

    def __iter__(self) -> Iterable[A]:
        yield from self._xs

    def head(self):
        return next(self._xs)

    def tail(self):
        return self.drop(1)

    def map(self, f: Callable[[A], B]) -> 'Stream[B]':
        return Stream(map(f, self._xs))

    def filter(self, p: Callable[[A], bool]) -> 'Stream[A]':
        return Stream(filter(p, self._xs))

    def bind(self, f: Callable[[A], 'Stream[B]']) -> 'Stream[B]':
        return Stream(chain.from_iterable(map(f, self._xs)))

    def reduce(self, f: Callable[[A, 'Stream[B]'], 'B']) -> 'B':
        return reduce(f, self._xs)

    def chain(self, ys):
        return Stream(chain(self._xs, ys))

    def take(self, n: int) -> 'Stream[A]':
        return Stream(islice(self._xs, n))

    def drop(self, n: int) -> 'Stream[A]':
        return Stream(islice(self._xs, n, None))

    def takewhile(self, p: Callable[[A], bool]) -> 'Stream[A]':
        return Stream(takewhile(p, self._xs))

    def dropwhile(self, p: Callable[[A], bool]) -> 'Stream[A]':
        return Stream(dropwhile(p, self._xs))

    # Key functions reserved for situations in which a preceding .map to the op
    # would not evaluate to the same result

    def sort(self, key=None):
        return Stream(sorted(self._xs, key=key))

    # built-ins max/min don't handle key=None properly

    def max(self, key=None):
        key = (lambda x: x) if key is None else key
        return Stream(max(self._xs, key=key))

    def min(self, key=None):
        key = (lambda x: x) if key is None else key
        return Stream(min(self._xs, key=key))

    def distinct(self, key=None):
        key = (lambda x: x) if key is None else key

        def g():
            S = set()
            for x in self._xs:
                key_x = key(x)
                if key_x not in S:
                    yield x
                S.add(key_x)

        return Stream(g())

    # Terminal operations

    def to(self, f: Callable[[Iterable[A]], Iterable[A]]) -> Iterable[A]:
        return f(self._xs)

    def sum(self):
        return sum(self._xs)

    def any(self):
        return any(self._xs)

    def all(self):
        return all(self._xs)

    def quantify(self):
        return sum(1 for _ in self._xs)

    def zip(self, ys):
        return Stream(zip(self._xs, ys))

    def zip_longest(self, ys, fillvalue=None):
        return Stream(zip_longest(self._xs, ys, fillvalue=fillvalue))

    def tee(self, n=2):
        return Stream(Stream(g) for g in tee(self._xs, n))

    def partition(self, p):
        t1, t2 = self.tee()
        return Stream(filterfalse(p, t1)), Stream(filter(p, t2))

    def grouper(self, n, fillvalue=None):
        args = [iter(self)] * n
        return Stream(Stream(g) for g in
                      zip_longest(*args, fillvalue=fillvalue))
