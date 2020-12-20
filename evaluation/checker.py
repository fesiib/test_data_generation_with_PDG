def test():
    from sourcecode import SourceCode
    from testcase import TestCase

    sc = SourceCode(path="./evaluation/gcd.py")
    sc.create_file()

    test = TestCase(test_type=0)

    test.execute_test_on(sc)

    print(test.get_output)


def checker():
    from generator import Generator
    from coveragetable import CoverageTable
    from sourcecode import SourceCode

    example = ""
    program = SourceCode(example)
    generator = Generator()
    testcases = generator.generate_tests(program)


if __name__ == "__main__":
    test()
