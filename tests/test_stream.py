from genstream import Stream
from typing import Iterator


class TestInit:
    def test_init(self):
        assert Stream(range(1, 4)).to(list) == [1, 2, 3]

    def test_of(self):
        assert Stream.of(1, 2, 3).to(list) == [1, 2, 3]

    def test_xs_is_iterator(self):
        assert isinstance(Stream([1, 2, 3])._xs, Iterator)
        assert isinstance(Stream.of(1, 2, 3)._xs, Iterator)


class TestOps:
    def test_collect(self):
        assert Stream.of(1).to(list) == [1]

    def test_bind(self):
        xs = Stream.of(1).bind(lambda x: Stream.of(x * 2)).to(list)
        assert xs == [2]

    def test_concat(self):
        xs = Stream.of(1)
        ys = Stream.of(2)
        assert xs.concat(ys).to(list) == [1, 2]

    def test_concatleft(self):
        xs = Stream.of(1)
        ys = Stream.of(2)
        assert xs.concatleft(ys).to(list) == [2, 1]

    def test_reduce(self):
        xs = Stream.of(1, 3, 2)
        assert xs.reduce(max) == 3

    def test_foldright(self):
        xs = Stream(range(0, 4))
        assert (xs.foldright(Stream.of(), lambda a, b: b + range(a)).to(list)
                == [0, 0, 1, 0, 1, 2])

    def test_filter(self):
        xs = Stream.of(1)
        assert xs.filter(lambda x: x != 1).to(list) == []

    def test_partition(self):
        is_even = lambda x: x % 2 == 0
        odds, evens = Stream.of(1, 2).partition(is_even)
        assert odds.to(list) == [1]
        assert evens.to(list) == [2]

    def test_zip(self):
        xs = Stream.of(1, 2, 3).zip(Stream.of("a", "b", "c")).to(list)
        assert xs == [(1, "a"), (2, "b"), (3, "c")]

    def test_grouper(self):
        xss = Stream.of(1, 2, 3, 4, 5).grouper(3)
        xss = xss.map(lambda xs: xs.to(list)).to(list)
        assert xss == [[1, 2, 3], [4, 5, None]]

    def test_head(self):
        assert Stream.of(1).map(lambda x: x).head() == 1

    def test_tail(self):
        assert Stream.of(1, 2, 3).map(lambda x: x).tail().to(list) == [2, 3]
