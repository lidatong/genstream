from functools import partial
from itertools import count
from operator import add

from genstream import Stream


def main():
    add_one = partial(add, 1)
    xs = Stream(count(0))  # infinite stream counting from 0
    one_thru_five = xs[:5] | add_one > list
    print(one_thru_five)


if __name__ == '__main__':
    main()
