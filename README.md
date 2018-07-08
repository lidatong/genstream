# genstream

## Quickstart

`pip install genstream`

```python
from genstream import Stream


def main():
    a_list_containing_four = (
        Stream.of(1, 2, 3)
            .map(lambda x: x * 2)
            .take(2)
            .tail()
            .to(list) # prints [4]
    )
    print(a_list_containing_four)


if __name__ == '__main__':
    main()
```


## Soapbox
While generators are one of Python's best and most distinctive language features, I personally find it tiresome to read 
generator code that undergoes successive transformations. The `(x for x in xs)` pattern has a low signal-to-noise ratio, 
especially when it spans across many lines. Can the repetition be abstracted away?

The `itertools` module is another pain point: the module is very useful, but I don't like the two argument nature of
many of the provided functions. I'm always trying to remember which goes first, the parameterization or the iterable,
as the ordering is inconsistent across functions (e.g. compare `take` with `map`)`.

**genstream** provides a `Stream` structure that aims to address these two nits. It provides the infix method chaining syntax
(`.map`, `.filter`, etc.) found in many other programming languages. While I agree with
the python community consensus that `map(f, xs)` is less readable than `(f(x) for x in xs)`, how about `xs.map(f)`? I
prefer method syntax when sequencing many operations on an iterable.

## Example of reading lines from many large files without running out of memory

```python
# Located under examples/concat_files.py
import os
from genstream import Stream


def read_lines_in_file(filename):
    with open(filename) as fp:
        yield from fp


# Using `Stream`
def concat_files(dirname):
    return (
        Stream(os.listdir(dirname))
            .sort()
            .map(lambda fname: f"{dirname}/{fname}")
            .bind(read_lines_in_file)
    )


# Using generators
def concat_files_gen(dirname):
    fnames = os.listdir(dirname)
    sorted_fnames = sorted(fnames)
    fnames_with_dir = (f"{dirname}/{fname}" for fname in sorted_fnames)
    for fname in fnames_with_dir:
        yield from read_lines_in_file(fname)


# A more concise way, but perhaps less readable
# In particular, `sorted(os.listdir(dirname))` is very dense
def concat_files_concise(dirname):
    for fname in sorted(os.listdir(dirname)):
        yield from read_lines_in_file(f"{dirname}/{fname}")


def main():
    for line in concat_files("very_large_files"):
        print(line, end="")


if __name__ == '__main__':
    main()
```

## Example using Stream's symbolic operators

```python
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
```

## Note on implementation
Given a particular set of primitive operations (e.g. `__init__` and `reduce`),
it is possible to derive almost all stream ops in terms of one another.

However, the methods on `Stream` instead make calls to a corresponding
`itertools` function whenever possible. This is primarily for performance
reasons: itertools is a highly-optimized module implemented in C.

