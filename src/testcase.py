from typing import List

from sourcecode import SourceCode
from CustomConstraint import CustomConstraint

import random
import os
import uuid
import subprocess

class TestCase:
    def __init__(self, input: List[int] = None, output: List[int] = None, test_type: int = None):
        self.input = input
        self.output = output
        self.test_type = test_type
        if test_type is not None:
            self.generate_test(self.test_type)


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
        self.test_type = test_type
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
        input_data = self.input.copy()
        if self.test_type == 2:
            input_data.insert(0, len(input_data))
        
        #Execute with `path` and `input` (C++ or python)
        
        str_input_data = ""

        for i in input_data:
            str_input_data += str(i) + "\n"

        process = subprocess.Popen(['python3', path], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        
        stdout, stderr = process.communicate(input = bytearray(str_input_data, 'utf-8'))
        
        if len(stderr) != 0:
            print("Error is:" + stderr.decode("utf-8"))
            raise AssertionError

        str_output_data = stdout.decode("utf-8")
        str_output_data = str_output_data.split("\n")
        self.output = []
        for x in str_output_data:
            if x.isnumeric() is True:
                self.output.append(int(x))

        source_code.delete_file()

    def to_file(self, path, name = None):
        if os.path.exists(path) is False:
            os.mkdir(path)
            #raise AssertionError
        if name is None:
            name = "test" + uuid.uuid4().hex
        input_file = os.path.join(path, name + ".in")
        #output_file = os.path.join(path, name + ".out")

        data = self.input

        if self.test_type == 2:
            data.insert(0, len(data))
        

        with open(input_file, 'w') as f:
            for i in data:
                print(i, file=f)
        return input_file

    def get_fitness(self, constraint: CustomConstraint) -> float:
        return constraint.to_fitness(self.input)





