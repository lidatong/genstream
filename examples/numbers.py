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
