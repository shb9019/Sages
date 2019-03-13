"""Runner Class"""
#!/usr/bin/env python3
import subprocess
import random
import string

class Runner:
    """
        Class to handle Running executing a C++ code
        input_file_path -> file in temp which contains input test cases
        code -> C++ code as python string
    """

    def __init__(self, input_file_path, code):
        self.input_file_path = input_file_path
        self.code = code
        self.file_name = ''
        self.generate_file_name()
        self.write_to_file()

    def compile_and_run(self):
        """Function to Compile & Run the code"""

        compile_status_code = self.compile()
        if compile_status_code != 0:
            return False

        run_status_code = self.run()
        if run_status_code != 0:
            return False

        return True

    def generate_file_name(self):
        """Function to generate a random 15 characters string for filenames"""

        valid_characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        self.file_name = ''.join(random.choice(valid_characters) for _ in range(15))

    def write_to_file(self):
        """Function to write given code to .cpp file in tmp/"""

        file = open(string.Template("tmp/$file_name.cpp").substitute(file_name=self.file_name), "w")
        file.write(self.code)
        file.close()

    def compile(self):
        """Function to compile code"""

        command = 'g++ --std=c++14 tmp/$file_name.cpp -o tmp/$file_name.out'
        command_template = string.Template(command).substitute(file_name=self.file_name)
        compile_status_code = subprocess.call(command_template, shell=True)
        return compile_status_code

    def run(self):
        """Function to run code over a timeout of 10s"""

        command = 'timeout 10s ./tmp/$file_name.out < tmp/$input > tmp/$file_name.txt'
        command_template = string.Template(command)\
            .substitute(file_name=self.file_name, input=self.input_file_path)
        execute_status_code = subprocess.call(command_template, shell=True)
        return execute_status_code

    def clear_files(self):
        """Function to clear all generated for user"""

        command = 'rm tmp/$file_name.cpp tmp/$file_name.out tmp/$file_name.txt'
        command_template = string.Template(command).substitute(file_name=self.file_name)
        subprocess.call(command_template, shell=True)
