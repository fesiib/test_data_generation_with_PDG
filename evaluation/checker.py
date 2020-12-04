def test():
    from sourcecode import SourceCode

    sc = SourceCode("lol,ekfafdsfsd\nsfsdfsdf")
    sc.create_file()
    sc.delete_file()


def checker():
    from generator import Generator
    from coveragetable import CoverageTable
    from sourcode import SourceCode

    example = ""
    program = SourceCode(example)
    generator = Generator()
    testcases = generator.generate_tests(program)


if __name__ == "__main__":
    test()
