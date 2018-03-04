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


def _identity(x):
    return x


class Stream(Generic[A]):
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Iterable):
            self._xs = iter(args[0])
        else:
            self._xs = iter(args)

    def __iter__(self) -> Iterable[A]:
        yield from self._xs

    def __add__(self, ys) -> 'Stream[A]':
        return self.concat(ys)

    def __or__(self, f: Callable[[A], B]) -> 'Stream[B]':
        return self.map(f)

    def __gt__(self, f: Callable[[Iterable[A]], Iterable[A]]) -> Iterable[A]:
        return self.to(f)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.slice(i.start, i.stop, i.step)
        raise TypeError("'stream' object only supports slice operations")

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

    def concat(self, ys):
        return Stream(chain(self._xs, ys))

    def slice(self, start: int, stop: int, step: int) -> 'Stream[A]':
        return Stream(islice(self._xs, start, stop, step))

    def take(self, n: int) -> 'Stream[A]':
        return Stream(islice(self._xs, n))

    def drop(self, n: int) -> 'Stream[A]':
        return Stream(islice(self._xs, n, None))

    def takewhile(self, p: Callable[[A], bool]) -> 'Stream[A]':
        return Stream(takewhile(p, self._xs))

    def dropwhile(self, p: Callable[[A], bool]) -> 'Stream[A]':
        return Stream(dropwhile(p, self._xs))

    # Key functions are provided in situations in which adding a preceding .map
    # would not result in the same transformation

    def sort(self, key=_identity):
        return Stream(sorted(self._xs, key=key))

    def max(self, key=_identity):
        return Stream(max(self._xs, key=key))

    def min(self, key=_identity):
        return Stream(min(self._xs, key=key))

    def unique(self, key=_identity):
        def g():
            S = set()
            for x in self._xs:
                kx = key(x)
                if kx not in S:
                    S.add(kx)
                    yield x

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
