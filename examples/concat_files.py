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
