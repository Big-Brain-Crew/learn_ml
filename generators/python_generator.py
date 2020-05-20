''' This script defines a base Python code generator.

Strings can be written to a file and formatted with indentations and docstrings.
'''
import json
import os
import sys


class PythonGenerator(object):
    '''Generates a Python script and writes code to it.
    '''

    def __init__(self, out):

        self.out_file_name = out
        self.out = open(self.out_file_name, "w+")  # Code written to this file

        self.indent_level = 0  # Keeps track of current indentation
        self.indent_str = "    "

    def __indent(self, inc=1):
        ''' Increments the indent level of the output string.
        '''

        self.indent_level += inc

    def __unindent(self, dec=1):
        ''' Decrements the indent level of the output string.
        '''

        self.indent_level -= dec

    def __spaces(self):
        '''Returns a string of the correct number of spaces for the current indent level.
        '''

        return self.indent_str * self.indent_level

    def __write(self, line):
        ''' Writes a line of code to the file.
        '''

        self.out.write(self.__spaces() + line)

    def __write_docstring(self, line):
        ''' Writes a line of docstring to the file.
            line: Docstring comment without docstring quotes.
        '''

        self.out.write(self.__spaces() + "'''" + line)
        self.out.write(self.__spaces() + "'''\n\n")

    def __start_method(self):
        '''Formats out string to generate a method.
        '''

        self.__indent()

    def __end_method(self):
        '''Formats out string once method is done.
        '''

        self.__write("\n\n")
        self.__unindent(2)

    def get_gen_file_name(self):
        '''Returns the name of the generated Python script.

        Currently the file name is not modifiable.
        '''

        return self.out
