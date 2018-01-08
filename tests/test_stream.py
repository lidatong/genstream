from genstream import Stream
from typing import Iterator


class TestInit:
    def test_iterable(self):
        assert Stream(range(1, 4)).to(list) == [1, 2, 3]

    def test_varargs(self):
        assert Stream(1, 2, 3).to(list) == [1, 2, 3]

    def test_xs_is_iterator(self):
        assert isinstance(Stream([1, 2, 3])._xs, Iterator)
        assert isinstance(Stream(1, 2, 3)._xs, Iterator)


class TestOps:
    def test_collect(self):
        assert Stream(1).to(list) == [1]

    def test_bind(self):
        xs = Stream(1).bind(lambda x: Stream(x * 2)).to(list)
        assert xs == [2]

    def test_chain(self):
        xs = Stream(1)
        ys = Stream(2)
        assert xs.chain(ys).to(list) == [1, 2]

    def test_reduce(self):
        xs = Stream(1, 3, 2)
        assert xs.reduce(max) == 3

    def test_filter(self):
        xs = Stream(1)
        assert xs.filter(lambda x: x != 1).to(list) == []

    def test_partition(self):
        is_even = lambda x: x % 2 == 0
        odds, evens = Stream(1, 2).partition(is_even)
        assert odds.to(list) == [1]
        assert evens.to(list) == [2]

    def test_zip(self):
        xs = Stream(1, 2, 3).zip(Stream("a", "b", "c")).to(list)
        assert xs == [(1, "a"), (2, "b"), (3, "c")]

    def test_grouper(self):
        xss = Stream(1, 2, 3, 4, 5).grouper(3)
        xss = xss.map(lambda xs: xs.to(list)).to(list)
        assert xss == [[1, 2, 3], [4, 5, None]]

    def test_head(self):
        assert Stream(1).map(lambda x: x).head() == 1

    def test_tail(self):
        assert Stream(1, 2, 3).map(lambda x: x).tail().to(list) == [2, 3]
