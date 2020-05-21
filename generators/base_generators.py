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

    def _indent(self, inc=1):
        ''' Increments the indent level of the output string.
        '''

        self.indent_level += inc

    def _unindent(self, dec=1):
        ''' Decrements the indent level of the output string.
        '''

        self.indent_level -= dec

    def _spaces(self):
        '''Returns a string of the correct number of spaces for the current indent level.
        '''

        return self.indent_str * self.indent_level

    def _write(self, line):
        ''' Writes a line of code to the file.
        '''

        self.out.write(self._spaces() + line)

    def _write_docstring(self, line):
        ''' Writes a line of docstring to the file.
            line: Docstring comment without docstring quotes.
        '''

        self.out.write(self._spaces() + "'''" + line)
        self.out.write(self._spaces() + "'''\n\n")

    def _start_method(self):
        '''Formats out string to generate a method.
        '''

        self._indent()

    def _end_method(self):
        '''Formats out string once method is done.
        '''

        self._write("\n\n")
        self._unindent(2)
    
    def _close(self):
        self.out.close()

    def get_gen_file_name(self):
        '''Returns the name of the generated Python script.

        Currently the file name is not modifiable.
        '''

        return self.out



class JsonGenerator(object):
    def __init__(self, out_file):
        
        self.out_file = out_file
        self.out = open(self.out_file, "w+")

        self.root = {}
        self.index = self.root
    
    def _close(self):
        self.out.close()
        
    def indent(self, name):
        self.index = self.root[name]

    def unindent(self):
        self.index = self.root

    def add_entry(self, name, entry):
        if name in self.index and isinstance(self.index[name], list):
            self.index[name].append(entry)
        else:
            self.index[name] = entry
    
    def write(self):
        json.dump(self.root, self.out, indent=4)
        self._close()
        print("Saved to {}".format(self.out_file))