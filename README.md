# genstream

## Quickstart

`pip install genstream`

```python
from genstream.stream import Stream


def main():
    a_list_containing_four = (
        Stream(1, 2, 3)
            .map(lambda x: x * 2)
            .take(2)
            .tail()
            .collect(list)
    )
    print(a_list_containing_four)


if __name__ == '__main__':
    main()
```


## Soapbox
While generators are one of Python's best and most distinctive language features, I personally find it tiresome to read 
generator code that undergoes successive transformations. The `(x for x in xs)` pattern has a low signal-to-noise ratio, 
especially when it spans across many lines. Can the repetition be abstracted away?

The `itertools` module is another pain point: the module is fantastic and useful, but I don't like the two argument nature of
many of the provided functions. I'm always trying to remember which goes first, the parameterization or the iterable,
as the ordering is inconsistent across functions (especially when the parameterization is optional).

genstream provides a `Stream` structure that aims to address these two nits. It provides the familiar method chaining syntax
(enabled by methods like `map`, `filter`, etc.) that you encounter in many other languages. While I agree with
the python community consensus that `map(f, xs)` is less readable than `(f(x) for x in xs)`, how about `xs.map(f)`? I
prefer the infix method syntax when sequencing operations on a group of elements, as I find it more concise and readable.

## Example of reading lines from many large files without running out of memory

```python
# Located under examples/concat_files.py
import os
from genstream.stream import Stream


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
