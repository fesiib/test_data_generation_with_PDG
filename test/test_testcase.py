def test_testcase_1():
    from sourcecode import SourceCode
    from testcase import TestCase

    sc = SourceCode(path = "./evaluation/gcd.py")
    sc.create_file()

    test = TestCase(input = [12, 10])

    test.execute_test_on(sc)

    assert test.get_output() == [2]

def test_testcase_2():
    from sourcecode import SourceCode
    from testcase import TestCase

    path = "./evaluation/gcd.py"
    
    str_sc = ""
    with open(path, "r") as f:
        str_sc = f.read()
    

    sc = SourceCode(str_sc)
    sc.create_file()

    test = TestCase(input = [10, 10])

    test.execute_test_on(sc)
    assert test.get_output() == [10]



if __name__ == "__main__":
    test_testcase_1()
