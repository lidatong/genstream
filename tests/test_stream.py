from genstream import Stream


class TestInit:
    def test_iterable(self):
        assert Stream(range(1, 4)).collect(list) == [1, 2, 3]

    def test_varargs(self):
        assert Stream(1, 2, 3).collect(list) == [1, 2, 3]


class TestOps:
    def test_collect(self):
        assert Stream(1).collect(list) == [1]

    def test_bind(self):
        xs = Stream(1).bind(lambda x: Stream(x * 2)).collect(list)
        assert xs == [2]

    def test_chain(self):
        xs = Stream(1)
        ys = Stream(2)
        assert xs.chain(ys).collect(list) == [1, 2]

    def test_reduce(self):
        xs = Stream(1, 3, 2)
        assert xs.reduce(max) == 3

    def test_filter(self):
        xs = Stream(1)
        assert xs.filter(lambda x: x != 1).collect(list) == []

    def test_partition(self):
        is_even = lambda x: x % 2 == 0
        odds, evens = Stream(1, 2).partition(is_even)
        assert odds.collect(list) == [1]
        assert evens.collect(list) == [2]

    def test_zip(self):
        xs = Stream(1, 2, 3).zip(Stream("a", "b", "c")).collect(list)
        assert xs == [(1, "a"), (2, "b"), (3, "c")]

    def test_grouper(self):
        xss = Stream(1, 2, 3, 4, 5).grouper(3)
        xss = xss.map(lambda xs: xs.collect(list)).collect(list)
        assert xss == [[1, 2, 3], [4, 5, None]]

    def test_head(self):
        assert Stream(1).map(lambda x: x).head() == 1

    def test_tail(self):
        assert Stream(1, 2, 3).map(lambda x: x).tail().collect(list) == [2, 3]
