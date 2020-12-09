from typing import List

from sourcecode import SourceCode

import random
import os
import uuid

class TestCase:
    def __init__(self, input: List[int] = None, output: List[int] = None, test_type: int = None):
        self.input = input
        self.output = output
        self.test_type = test_type

    def get_input(self) -> List[int]:
        if self.input is None:
            return list()
        return self.input
    
    def get_output(self) -> List[int]:
        if self.output is None:
            if self.input is None:
                return list()
            raise AssertionError
        return self.output

    def get_test_type(self) -> int:
        if self.test_type is None:
            return -1
        return self.test_type

    def generate_test(self, test_type: int):
        if test_type == 0:
            self.__generate(2)
        elif test_type == 1:
            self.__generate(3)
        elif test_type == 2:
            self.__generate(10)
        else:
            raise AssertionError

    def __generate(self, n: int):
        self.input = list()
        for _ in range(n):
            self.input.append(random.randint(0, 10000))

    def execute_test_on(self, source_code: SourceCode):
        path = source_code.create_file()
        input = self.input.copy()
        if self.test_type == 2:
            input.insert(0, len(input))
        #Execute with `path` and `input` (C++ or python)
        source_code.delete_file()

    def to_file(self, path, name = None):
        if os.path.exists(path) is False:
            raise AssertionError
        if name is None:
            name = "test" + uuid.uuid4().hex
        input_file = os.path.join(path, name + ".in")
        #output_file = os.path.join(path, name + ".out")

        with open(input_file, 'w') as f:
            for i in self.input:
                print(i, file=f)
        return input_file




