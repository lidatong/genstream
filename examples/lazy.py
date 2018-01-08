from genstream import Stream
from functools import wraps


def print_event(f):
    @wraps(f)
    def g(*args, **kwargs):
        print(f"Executing {f}")
        return f(*args, **kwargs)

    return g


@print_event
def timestwo(x):
    return x * 2


@print_event
def is_even(x):
    return x % 2 == 0


def main():
    xs = (
        Stream(1, 2, 3)
            .map(timestwo)
            .filter(is_even)
            .take(2)
            .tail()
    )
    xs.to(list)


if __name__ == '__main__':
    main()
