import os
import sys
import pytest
import warnings
import pdb


@pytest.fixture
def python_generator():
    sys.path.append(os.getcwd())
    import generators.python_generators as python_generators

    pygen = python_generators.PythonGenerator(out="./tests/files/test_python_generator.txt")
    return pygen


@pytest.fixture
def class_generator():
    sys.path.append(os.getcwd())
    import generators.python_generators as python_generators
    pygen = python_generators.ClassGenerator(class_config="./tests/files/test_class.json",
                                             map_config="./tests/files/test_map.json",
                                             out="./tests/files/test_class_generator.txt")
    return pygen


@pytest.fixture
def pygen_file_reader():
    return open("./tests/files/test_python_generator.txt", "r")


@pytest.fixture
def class_file_reader():
    return open("./tests/files/test_class_generator.txt", "r")


class TestPythonGenerator:
    def test_init(self):
        sys.path.append(os.getcwd())
        import generators.python_generators as python_generators

        file_name = "./tests/files/test_python_generator.txt"
        pygen = python_generators.PythonGenerator(out=file_name)

        assert pygen.out_file_name == file_name, "Out file name is incorrect"
        assert pygen.indent_level == 0, "Indent level not 0"
        assert pygen.indent_str == "    ", "Indent string is wrong"
        assert os.path.exists("./tests/files/test_python_generator.txt"), "Out file not opened"

    def test_indent(self, python_generator, pygen_file_reader):
        python_generator._indent()
        python_generator._write("This line is indented.\n")
        assert python_generator.indent_level == 1, "Indent level is incorrect"
        python_generator._close()
        assert pygen_file_reader.readline() == "    This line is indented.\n"

    def test_multiple_indent(self, python_generator, pygen_file_reader):
        python_generator._indent(3)
        python_generator._write("This line is thrice indented.\n")
        python_generator._close()
        assert pygen_file_reader.readline() == "            This line is thrice indented.\n"

    def test_unindent(self, python_generator, pygen_file_reader):
        python_generator._indent()
        python_generator._unindent()
        assert python_generator.indent_level == 0, "Indent level is wrong"

        python_generator._indent(3)
        python_generator._unindent(2)
        assert python_generator.indent_level == 1, "Indent level is wrong"

        python_generator._write("This line is indented once.\n")
        python_generator._close()
        assert pygen_file_reader.readline() == "    This line is indented once.\n"

    def test_spaces(self, python_generator):
        assert python_generator._spaces() == "", "Wrong number of spaces"
        python_generator._indent()
        assert python_generator._spaces() == "    ", "Wrong number of spaces"
        python_generator._indent(2)
        assert python_generator._spaces() == "            ", "Wrong number of spaces"
        python_generator._close()

    def test_write(self, python_generator, pygen_file_reader):
        python_generator._write("This is a line of code\n")
        python_generator._close()
        assert pygen_file_reader.readline() == "This is a line of code\n", "Line not written properly"

    def test_write_multiple_lines(self, python_generator, pygen_file_reader):
        python_generator._write(["Line 1\n",
                                 "Line 2\n",
                                 "Line 3\n"])
        python_generator._close()
        assert pygen_file_reader.readlines() == ["Line 1\n",
                                                 "Line 2\n",
                                                 "Line 3\n"], "Lines not written properly"

    def test_write_nothing(self, python_generator, pygen_file_reader):
        with pytest.warns(UserWarning):
            python_generator._write(None)

    def test_write_docstring(self, python_generator, pygen_file_reader):
        python_generator._write_docstring("This is a line of docstring.\n")
        python_generator._close()
        assert pygen_file_reader.readlines() == ["'''This is a line of docstring.\n",
                                                 "'''\n",
                                                 "\n"], "Docstring written incorrectly"

    def test_write_docstring_none(self, python_generator, pygen_file_reader):
        python_generator._write_docstring()
        python_generator._close()
        assert pygen_file_reader.readlines() == []

    def test_write_docstring_multiple_lines(self, python_generator, pygen_file_reader):
        python_generator._write_docstring(["This is the header line.\n",
                                           "This is the description. The description may be " +
                                           "multiple lines. It is very descriptive.\n"])
        python_generator._close()
        assert pygen_file_reader.readlines() == ["'''This is the header line.\n",
                                                 "\n",
                                                 "This is the description. The description may be " +
                                                 "multiple lines. It is very descriptive.\n",
                                                 "'''\n",
                                                 "\n"], "Docstring written incorrectly"

    def test_close(self, python_generator, pygen_file_reader):
        python_generator._close()
        with pytest.raises(ValueError):
            assert python_generator._write("Test")

    def test_get_gen_file_name(self, python_generator):
        assert python_generator.get_gen_file_name() == "./tests/files/test_python_generator.txt"


class TestClassGenerator:
    def test_init(self):
        sys.path.append(os.getcwd())
        import generators.python_generators as python_generators

        with pytest.raises(FileNotFoundError):
            pygen = python_generators.ClassGenerator(class_config="notafile",
                                                     map_config="./tests/files/test_map.json",
                                                     out="./tests/files/test_class_generator.txt")
            pygen = python_generators.ClassGenerator(class_config="./tests/files/test_class.json",
                                                     map_config="notafile",
                                                     out="./tests/files/test_class_generator.txt")

            pygen = python_generators.ClassGenerator(class_config="./tests/files/test_class.json",
                                                     map_config="./tests/files/test_map.json",
                                                     out="./tests/files/test_class_generator.txt")

            assert pygen.class_ == {"test": "value"}
            assert pygen.map["map"]["sequential"] == {"name": "tf.keras.models.Sequential",
                                                      "type": "object"}

    def test_write_imports(self, class_generator, class_file_reader):
        with pytest.raises(TypeError):
            class_generator._write_imports("not a dict")

        imports = {
            "tensorflow": "tf",
            "numpy": "np"
        }
        class_generator._write_imports(imports)
        class_generator._close()
        assert class_file_reader.readlines() == ["# Imports\n",
                                                 "import tensorflow as tf\n",
                                                 "import numpy as np\n",
                                                 "\n",
                                                 "\n"]

    def test_start_class(self, class_generator, class_file_reader):
        class_generator._start_class("TestClass", "InheritedClass", "This is a test!\n")
        class_generator._close()

        assert class_file_reader.readlines() == [
            "class TestClass(InheritedClass):\n",
            "    '''This is a test!\n",
            "    '''\n",
            "\n"
        ]

    def test_is_valid_arg_dict(self, class_generator):
        args = None
        arg_str = class_generator._is_valid_arg_dict(args)

        args = {}
        arg_str = class_generator._is_valid_arg_dict(args)

        args = "not a dict"
        with pytest.raises(TypeError, match=r".*formatted as a dictionary.*"):
            class_generator._is_valid_arg_dict(args)

        args = {
            "param_1": "val_1",
            "param_2": None
        }
        with pytest.raises(ValueError, match=r".*None.*"):
            class_generator._is_valid_arg_dict(args)

        args = {
            "param_1": None,
            "param_2": "val_2",
            "param_3": None
        }
        with pytest.raises(ValueError, match=r".*None.*"):
            class_generator._is_valid_arg_dict(args)

        args = {
            "param_1": 4,
            "param_2": None
        }
        with pytest.raises(ValueError, match=r".*None.*"):
            class_generator._is_valid_arg_dict(args)

        args = {
            5: "val_1",
            "param_2": "val_2"
        }
        with pytest.raises(TypeError, match=r".*keys must be.*"):
            class_generator._is_valid_arg_dict(args)

        args = {
            "param_1": None,
            "param_2": "val_2"
        }
        class_generator._is_valid_arg_dict(args)

        args = {
            "param_1": "val_1",
            "param_2": "val_2"
        }
        class_generator._is_valid_arg_dict(args)

        args = {
            "param_1": None,
            "param_2": None
        }
        class_generator._is_valid_arg_dict(args)

        args = {
            "param_1": None,
            "param_2": 4
        }
        class_generator._is_valid_arg_dict(args)

    def test_arg_str(self, class_generator):
        args = None
        arg_str = class_generator._arg_str(args)
        assert arg_str == ""

        args = {}
        arg_str = class_generator._arg_str(args)
        assert arg_str == ""

        args = {
            "param_1": None,
            "param_2": "val_2"
        }
        arg_str = class_generator._arg_str(args)
        assert arg_str == "param_1, param_2=val_2"

        args = {
            "param_1": "val_1",
            "param_2": "val_2"
        }
        arg_str = class_generator._arg_str(args)
        assert arg_str == "param_1=val_1, param_2=val_2"

        args = {
            "param_1": None,
            "param_2": None
        }
        arg_str = class_generator._arg_str(args)
        assert arg_str == "param_1, param_2"

        args = {
            "param_1": None,
            "param_2": "4"
        }
        arg_str = class_generator._arg_str(args)
        assert arg_str == "param_1, param_2=4"

    def test_is_valid_fn_dict(self, class_generator):
        fn_dict = None
        with pytest.raises(TypeError, match=r".*dict.*"):
            class_generator._is_valid_fn_dict(fn_dict)

        fn_dict = "notadict"
        with pytest.raises(TypeError, match=r".*dict.*"):
            class_generator._is_valid_fn_dict(fn_dict)

        fn_dict = {
            "1": "val",
            "2": "val"
        }
        with pytest.raises(ValueError, match=r".*\"name\".*"):
            class_generator._is_valid_fn_dict(fn_dict)

        fn_dict = {
            "name": 4,
            "args": None
        }
        with pytest.raises(TypeError, match=r".*name must be.*"):
            class_generator._is_valid_fn_dict(fn_dict)

        fn_dict = {
            "name": "function",
            "args": "notadict"
        }
        with pytest.raises(TypeError):
            class_generator._is_valid_fn_dict(fn_dict)

        fn_dict = {
            "name": "function",
            "notargs": {}
        }
        with pytest.raises(ValueError, match=r".*\"args\".*"):
            class_generator._is_valid_fn_dict(fn_dict)

        fn_dict = {
            "notname": "function",
            "args": None
        }
        with pytest.raises(ValueError, match=r".*\"name\".*"):
            class_generator._is_valid_fn_dict(fn_dict)

        fn_dict = {
            "name": "function",
            "args": {"param": "val"},
            "extra": "catchme"
        }
        with pytest.raises(ValueError, match=r".*only keys.*"):
            class_generator._is_valid_fn_dict(fn_dict)

    def test_fn_str(self, class_generator):
        fn_dict = {
            "name": "function",
            "args": None
        }
        fn_str = class_generator._fn_str(fn_dict)
        assert fn_str == "function()"

        fn_dict = {
            "name": "function",
            "args": {
                "param_1": "val_1",
                "param_2": "val_2"
            }
        }
        fn_str = class_generator._fn_str(fn_dict)
        assert fn_str == "function(param_1=val_1, param_2=val_2)"

        fn_dict = {
            "name": "function",
            "args": {
                "param_1": None,
                "param_2": "val_2"
            }
        }
        fn_str = class_generator._fn_str(fn_dict)
        assert fn_str == "function(param_1, param_2=val_2)"

    def test_map(self, class_generator):
        input_ = None
        mapped = class_generator._map(input_)
        assert mapped is None

        input_ = 4
        mapped = class_generator._map(input_)
        assert mapped == 4

        input_ = "sequential"
        mapped = class_generator._map(input_)
        assert mapped == "tf.keras.models.Sequential"

        input_ = "dense"
        mapped = class_generator._map(input_)
        assert mapped == "\"dense_string\""

    def test_map_fn(self, class_generator):
        fn_dict = {
            "name": "sequential",
            "args": {
                "activation": "relu",
                "optim": "adam"
            }
        }
        mapped = class_generator._map_fn(fn_dict)
        assert mapped == {
            "name": "tf.keras.models.Sequential",
            "args": {
                "activation": "tf.nn.relu",
                "optimizer": "tf.keras.optimizers.Adam"
            }
        }

        fn_dict = {
            "name": "compile",
            "args": {
                "loss": "crossentropy",
                "optim": {
                    "name": "adam",
                    "args": {
                        "learning_rate": 0.001
                    }
                },
                "metrics": [
                    "accuracy"
                ]
            }
        }
        mapped = class_generator._map_fn(fn_dict)
        assert mapped == {
            "name": "compile",
            "args": {
                "loss": "tf.keras.losses.sparse_categorical_crossentropy",
                "optimizer": "tf.keras.optimizers.Adam(learning_rate=0.001)",
                "metrics": [
                    "accuracy"
                ]
            }
        }

        fn_dict = {
            "name": "compile",
            "args": {
                "loss": "crossentropy",
                "optim": {
                    "name": "adam",
                    "args": {
                        "learning_rate": {
                            "name": "learning_rate",
                            "args": {
                                "param_1": "relu",
                                "param_2": 0.001
                            }
                        }
                    }
                },
                "metrics": [
                    "accuracy"
                ]
            }
        }
        mapped = class_generator._map_fn(fn_dict)
        assert mapped == {
            "name": "compile",
            "args": {
                "loss": "tf.keras.losses.sparse_categorical_crossentropy",
                "optimizer": "tf.keras.optimizers.Adam(" +
                "learning_rate=learning_rate(param_1=tf.nn.relu, param_2=0.001))",
                "metrics": [
                    "accuracy"
                ]
            }
        }

    def test_fn(self, class_generator):
        fn_dict = {
            "name": "sequential",
            "args": {
                "activation": "relu",
                "optim": "adam"
            }
        }
        mapped = class_generator._fn(fn_dict)
        assert mapped == "tf.keras.models.Sequential(activation=tf.nn.relu, " + \
            "optimizer=tf.keras.optimizers.Adam)"

        fn_dict = {
            "name": "compile",
            "args": {
                "loss": "crossentropy",
                "optim": {
                    "name": "adam",
                    "args": {
                        "learning_rate": 0.001
                    }
                },
                "metrics": [
                    "accuracy",
                    "mae"
                ]
            }
        }
        mapped = class_generator._fn(fn_dict)
        assert mapped == "compile(loss=tf.keras.losses.sparse_categorical_crossentropy, " + \
            "optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), " + \
            "metrics=[\'accuracy\', \'mae\'])"

        fn_dict = {
            "name": "compile",
            "args": {
                "loss": "crossentropy",
                "optim": {
                    "name": "adam",
                    "args": {
                        "learning_rate": {
                            "name": "learning_rate",
                            "args": {
                                "param_1": "relu",
                                "param_2": 0.001
                            }
                        }
                    }
                },
                "metrics": [
                    "accuracy"
                ]
            }
        }
        mapped = class_generator._fn(fn_dict)
        assert mapped == "compile(loss=tf.keras.losses.sparse_categorical_crossentropy, " + \
            "optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate(" + \
            "param_1=tf.nn.relu, param_2=0.001)), " + \
            "metrics=[\'accuracy\'])"

        fn_dict = {
            "name": "compile",
            "args": {
                "layer": "dense",
            }
        }
        mapped = class_generator._fn(fn_dict)
        assert mapped == "compile(layer=\"dense_string\")"

    def test_start_method(self, class_file_reader):
        sys.path.append(os.getcwd())
        import generators.python_generators as python_generators

        class_generator = python_generators.ClassGenerator(class_config="./tests/files/test_class.json",
                                                           map_config="./tests/files/test_map.json",
                                                           out="./tests/files/test_class_generator.txt")
        class_file_reader = open("./tests/files/test_class_generator.txt", "r")

        class_generator._start_method("method")
        class_generator._close()
        assert class_file_reader.readline() == "def method():\n"

        class_generator = python_generators.ClassGenerator(class_config="./tests/files/test_class.json",
                                                           map_config="./tests/files/test_map.json",
                                                           out="./tests/files/test_class_generator.txt")
        class_file_reader = open("./tests/files/test_class_generator.txt", "r")

        args = {}
        docstring = "This is docstring.\n"
        class_generator._start_method("method", args, docstring)
        class_generator._close()
        assert class_file_reader.readlines() == [
            "def method():\n",
            "    '''This is docstring.\n",
            "    '''\n",
            "\n"
        ]

        class_generator = python_generators.ClassGenerator(class_config="./tests/files/test_class.json",
                                                           map_config="./tests/files/test_map.json",
                                                           out="./tests/files/test_class_generator.txt")
        class_file_reader = open("./tests/files/test_class_generator.txt", "r")
        args = {
            "param_1": "val_1",
            "param_2": None
        }
        with pytest.raises(ValueError):
            class_generator._start_method("method", args)

        class_generator = python_generators.ClassGenerator(class_config="./tests/files/test_class.json",
                                                           map_config="./tests/files/test_map.json",
                                                           out="./tests/files/test_class_generator.txt")
        class_file_reader = open("./tests/files/test_class_generator.txt", "r")
        args = {
            "param_1": "val_1",
            "param_2": "val_2"
        }
        docstring = "This is docstring.\n"
        class_generator._start_method("method", args, docstring)
        class_generator._close()
        assert class_file_reader.readlines() == [
            "def method(param_1=val_1, param_2=val_2):\n",
            "    '''This is docstring.\n",
            "    '''\n",
            "\n"
        ]

    def test_start_class_method(self):
        sys.path.append(os.getcwd())
        import generators.python_generators as python_generators

        class_generator = python_generators.ClassGenerator(class_config="./tests/files/test_class.json",
                                                           map_config="./tests/files/test_map.json",
                                                           out="./tests/files/test_class_generator.txt")
        class_file_reader = open("./tests/files/test_class_generator.txt", "r")

        args = {
            "param_1": "val_1",
            "param_2": "val_2"
        }
        docstring = "This is docstring.\n"
        class_generator._start_class_method("method", args, docstring)
        class_generator._close()
        assert class_file_reader.readlines() == [
            "def method(self, param_1=val_1, param_2=val_2):\n",
            "    '''This is docstring.\n",
            "    '''\n",
            "\n"
        ]

        class_generator = python_generators.ClassGenerator(class_config="./tests/files/test_class.json",
                                                           map_config="./tests/files/test_map.json",
                                                           out="./tests/files/test_class_generator.txt")
        class_file_reader = open("./tests/files/test_class_generator.txt", "r")

        docstring = "This is docstring.\n"
        class_generator._start_class_method("method", docstring=docstring)
        class_generator._close()
        assert class_file_reader.readlines() == [
            "def method(self):\n",
            "    '''This is docstring.\n",
            "    '''\n",
            "\n"
        ]
