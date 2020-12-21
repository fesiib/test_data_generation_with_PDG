def evaluate_iters(path: str, test_type):
    from sourcecode import SourceCode
    from generator import Generator
    import const

    code = SourceCode(path=path)

    for max_iter in const.MAX_ITERS:
        for wait_iter in const.WAIT_ITERS:
            for dependency_mode in const.DEPENDENCY_MODES:
                generator = Generator(
                    max_iter=max_iter,
                    wait_iter=wait_iter,
                    dependency_mode=dependency_mode,
                    test_type=test_type,
                )
                print(str(generator))
                (ct, generations_cnt) = generator.generate_tests(code)
                print(
                    "->",
                    "COV", ct.calculate_coverage(),
                    "GS", generations_cnt,
                    sep=" ",
                    end="\n\n"
                )


def evaluate_GA(path: str, test_type):
    from sourcecode import SourceCode
    from generator import Generator
    import const

    code = SourceCode(path=path)

    for pop_size in const.POP_SIZES:
        for rate_crossover in const.RATES_CROSSOVER:
            for rate_mutation in const.RATES_MUTATION:
                generator = Generator(
                    population_size=pop_size,
                    rate_crossover=rate_crossover,
                    rate_mutation=rate_mutation,
                    test_type=test_type,
                )
                print(str(generator))
                (ct, generations_cnt) = generator.generate_tests(code)
                print(
                    "->",
                    "COV", ct.calculate_coverage(),
                    "GS", generations_cnt,
                    sep=" ",
                    end="\n\n"
                )


def evaluate_all(path: str, test_type):
    from sourcecode import SourceCode
    from generator import Generator
    import const

    code = SourceCode(path=path)

    for seed_size in const.SEED_SIZES:
        for pop_size in const.POP_SIZES:
            for rate_crossover in const.RATES_CROSSOVER:
                for rate_mutation in const.RATES_MUTATION:
                    for max_iter in const.MAX_ITERS:
                        for wait_iter in const.WAIT_ITERS:
                            for dependency_mode in const.DEPENDENCY_MODES:
                                generator = Generator(
                                    seed_size,
                                    pop_size,
                                    rate_crossover,
                                    rate_mutation,
                                    max_iter,
                                    wait_iter,
                                    dependency_mode,
                                    test_type,
                                )
                                print(str(generator))
                                (
                                    ct,
                                    generations_cnt,
                                ) = generator.generate_tests(code)
                                print(
                                    "->",
                                    "COV", ct.calculate_coverage(),
                                    "GS", generations_cnt,
                                    sep=" ",
                                    end="\n\n"
                                )
                                tests = ct.get_tests()
                                for test in tests:
                                    print("ok")
                                    test.to_file("./evaluation/cheburek/")


def evaluate_traingle_classification():
    evaluate_all("./evaluation/triangle_classification.py", 1)


def evaluate_find_max():
    evaluate_all("./evaluation/find_max.py", 1)


if __name__ == "__main__":
    evaluate_traingle_classification()
