def checker():
    from generator import Generator
    from coveragetable import CoverageTable
    from sourcode import SourceCode

    example = ""
    program = SourceCode(example)
    generator = Generator()
    testcases = generator.generate_tests(program)


if __name__ == "__main__":
    checker()
