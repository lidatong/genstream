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


xs = (
    Stream(1, 2, 3)
        .map(timestwo)
        .filter(is_even)
        .take(2)
        .tail()
    # .collect(list)
)

x, y, z = Stream(1, 2, 3)
print(x, y, z)

