import os
from stream import Stream


def read_lines_in_file(filename):
    with open(filename) as fp:
        yield from fp


def concat_files(dirname):
    return (
        Stream(os.listdir(dirname))
            .sort
            .map(lambda fname: f"{dirname}/{fname}")
            .bind(read_lines_in_file)
    )


def main():
    for line in concat_files("very_large_files"):
        print(line, end="")


if __name__ == '__main__':
    main()
