import os
import sys
import pytest
import warnings
import pdb
import json


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


@pytest.fixture
def json_generator():
    sys.path.append(os.getcwd())
    import generators.json_generators as json_generators
    json_gen = json_generators.JsonGenerator(
        out_file="./tests/files/test_json_generator.json")
    return json_gen


@pytest.fixture
def pipeline_json_generator():
    sys.path.append(os.getcwd())
    import generators.json_generators as json_generators

    json_generator = json_generators.PipelineJsonGenerator(
        out_file="./tests/files/test_json_generator.json")
    return json_generator


@pytest.fixture
def model_json_generator():
    sys.path.append(os.getcwd())
    import generators.json_generators as json_generators
    json_generator = json_generators.ModelJsonGenerator(
        out_file="./tests/files/test_json_generator.json")
    return json_generator

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


class TestGeneratorUtils:
    def test_is_valid_arg_dict(self):
        sys.path.append(os.getcwd())
        import generators.generator_utils as generator_utils

        args = None
        arg_str = generator_utils._is_valid_arg_dict(args)

        args = {}
        arg_str = generator_utils._is_valid_arg_dict(args)

        args = "not a dict"
        with pytest.raises(TypeError, match=r".*formatted as a dictionary.*"):
            generator_utils._is_valid_arg_dict(args)

        args = {
            "param_1": "val_1",
            "param_2": None
        }
        with pytest.raises(ValueError, match=r".*None.*"):
            generator_utils._is_valid_arg_dict(args)

        args = {
            "param_1": None,
            "param_2": "val_2",
            "param_3": None
        }
        with pytest.raises(ValueError, match=r".*None.*"):
            generator_utils._is_valid_arg_dict(args)

        args = {
            "param_1": 4,
            "param_2": None
        }
        with pytest.raises(ValueError, match=r".*None.*"):
            generator_utils._is_valid_arg_dict(args)

        args = {
            5: "val_1",
            "param_2": "val_2"
        }
        with pytest.raises(TypeError, match=r".*keys must be.*"):
            generator_utils._is_valid_arg_dict(args)

        args = {
            "param_1": None,
            "param_2": "val_2"
        }
        generator_utils._is_valid_arg_dict(args)

        args = {
            "param_1": "val_1",
            "param_2": "val_2"
        }
        generator_utils._is_valid_arg_dict(args)

        args = {
            "param_1": None,
            "param_2": None
        }
        generator_utils._is_valid_arg_dict(args)

        args = {
            "param_1": None,
            "param_2": 4
        }
        generator_utils._is_valid_arg_dict(args)

    def test_is_valid_fn_dict(self):
        sys.path.append(os.getcwd())
        import generators.generator_utils as generator_utils

        fn_dict = None
        with pytest.raises(TypeError, match=r".*dict.*"):
            generator_utils._is_valid_fn_dict(fn_dict)

        fn_dict = "notadict"
        with pytest.raises(TypeError, match=r".*dict.*"):
            generator_utils._is_valid_fn_dict(fn_dict)

        fn_dict = {
            "1": "val",
            "2": "val"
        }
        with pytest.raises(ValueError, match=r".*\"name\".*"):
            generator_utils._is_valid_fn_dict(fn_dict)

        fn_dict = {
            "name": 4,
            "args": None
        }
        with pytest.raises(TypeError, match=r".*name must be.*"):
            generator_utils._is_valid_fn_dict(fn_dict)

        fn_dict = {
            "name": "function",
            "args": "notadict"
        }
        with pytest.raises(TypeError):
            generator_utils._is_valid_fn_dict(fn_dict)

        fn_dict = {
            "name": "function",
            "notargs": {}
        }
        with pytest.raises(ValueError, match=r".*\"args\".*"):
            generator_utils._is_valid_fn_dict(fn_dict)

        fn_dict = {
            "notname": "function",
            "args": None
        }
        with pytest.raises(ValueError, match=r".*\"name\".*"):
            generator_utils._is_valid_fn_dict(fn_dict)

        fn_dict = {
            "name": "function",
            "args": {"param": "val"},
            "extra": "catchme"
        }
        with pytest.raises(ValueError, match=r".*only keys.*"):
            generator_utils._is_valid_fn_dict(fn_dict)

    def test_create_fn_dict(self):
        sys.path.append(os.getcwd())
        import generators.generator_utils as generator_utils

        fn_dict = generator_utils.create_fn_dict("function")
        assert fn_dict == {
            "name": "function",
            "args": None
        }

        args = {
            "param_1": "value_1",
            "param_2": "value_2"
        }
        fn_dict = generator_utils.create_fn_dict("function", args)
        assert fn_dict == {
            "name": "function",
            "args": {
                "param_1": "value_1",
                "param_2": "value_2"
            }
        }


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


class TestJsonGenerator:
    def test_init(self):
        sys.path.append(os.getcwd())
        import generators.json_generators as json_generators

        json_gen = json_generators.JsonGenerator(out_file="./tests/files/test_json_generator.json")

        assert json_gen.out_file == "./tests/files/test_json_generator.json"
        assert json_gen.out.name == "./tests/files/test_json_generator.json"
        assert json_gen.root == {}
        assert json_gen.index == json_gen.root

    def test_close(self, json_generator):
        json_generator._close()
        assert json_generator.out.closed == True

    def test_indent(self, json_generator):
        json_generator.root["key"] = {"param": "val"}
        json_generator._indent("key")
        assert json_generator.index == {"param": "val"}

        with pytest.warns(UserWarning):
            json_generator._indent("param")

        json_generator._indent("new_key")
        assert json_generator.index == {}
        assert json_generator.root == {
            "key": {
                "param": "val",
                "new_key": {}
            }
        }

    def test_unindent(self, json_generator):
        json_generator._indent("key_1")
        json_generator._indent("key_2")
        json_generator._unindent()
        assert json_generator.root == {
            "key_1": {
                "key_2": {}
            }
        }
        assert json_generator.index == json_generator.root

    def test_add_entry(self, json_generator):
        json_generator.add_entry("key", "value")
        assert json_generator.index == {
            "key": "value"
        }

        json_generator.add_entry("key_2", "value")
        assert json_generator.index == {
            "key": "value",
            "key_2": "value"
        }

        json_generator.add_entry("key", "new_value")
        assert json_generator.index == {
            "key": "new_value",
            "key_2": "value"
        }

        json_generator._indent("key_3")
        json_generator.add_entry("key_4", "value")
        assert json_generator.index == {
            "key_4": "value"
        }
        assert json_generator.root == {
            "key": "new_value",
            "key_2": "value",
            "key_3": {
                "key_4": "value"
            }
        }

        json_generator._unindent()
        json_generator.add_entry("key_5", ["value_1"])
        json_generator.add_entry("key_5", "value_2")
        assert json_generator.index == {
            "key": "new_value",
            "key_2": "value",
            "key_3": {
                "key_4": "value"
            },
            "key_5": ["value_1", "value_2"]
        }

    def test_add_fn(self, json_generator):
        json_generator.add_fn("key", "function")
        assert json_generator.index == {
            "key": {
                "name": "function",
                "args": None
            }
        }

        args = {
            "param_1": "val_1",
            "param_2": "val_2"
        }
        json_generator.add_fn("key", "function", args)
        assert json_generator.index == {
            "key": {
                "name": "function",
                "args": {
                    "param_1": "val_1",
                    "param_2": "val_2"
                }
            }
        }

    def test_write(self, json_generator):
        json_generator.add_entry("key", {
            "param": "val"
        })
        json_generator.write()

        json_file_reader = json.load(open("./tests/files/test_json_generator.json"))

        assert json_file_reader == {
            "key": {
                "param": "val"
            }
        }


class TestPipelineJsonGenerator:
    def test_init(self):
        sys.path.append(os.getcwd())
        import generators.json_generators as json_generators

        json_generator = json_generators.PipelineJsonGenerator(
            out_file="./tests/files/test_json_generator.json")

        assert json_generator.root == {
            "pipeline": {
                "dataset": {},
                "operations": []
            }
        }

    def test_add_dataset(self, pipeline_json_generator):
        pipeline_json_generator.add_dataset("test_dataset")
        assert pipeline_json_generator.index["dataset"]["label"] == "test_dataset"

    def test_add_operation(self, pipeline_json_generator):
        pipeline_json_generator.add_operation("op_1")
        assert pipeline_json_generator.index["operations"] == [
            {
                "name": "op_1",
                "args": None
            }
        ]

        args = {
            "param": "val"
        }
        pipeline_json_generator.add_operation("op_2", args)
        assert pipeline_json_generator.index["operations"] == [
            {
                "name": "op_1",
                "args": None
            },
            {
                "name": "op_2",
                "args": {
                    "param": "val"
                }
            }
        ]


class TestModelJsonGenerator:
    def test_init(self):
        sys.path.append(os.getcwd())
        import generators.json_generators as json_generators
        model_json_generator = json_generators.ModelJsonGenerator(
            out_file="./tests/files/test_json_generator.json")

        assert model_json_generator.root == {
            "model": {
                "model": {},
                "layers": [],
                "compile": {}
            }
        }

    def test_add_model(self, model_json_generator):
        model_json_generator.add_model("test_model")
        assert model_json_generator.index["model"]["name"] == "test_model"

    def test_add_layer(self, model_json_generator):
        model_json_generator.add_layer("flatten")
        assert model_json_generator.index["layers"] == [
            {
                "name": "flatten",
                "args": None
            }
        ]

        args = {
            "param": "value"
        }
        model_json_generator.add_layer("dense", args)
        assert model_json_generator.index["layers"] == [
            {
                "name": "flatten",
                "args": None
            },
            {
                "name": "dense",
                "args": {
                    "param": "value"
                }
            }
        ]

    def test_add_compile(self, model_json_generator):
        args = {
            "loss": "crossentropy",
            "optimizer": {
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
        model_json_generator.add_compile(args)
        assert model_json_generator.index["compile"] == {
            "name": "compile",
            "args": {
                "loss": "crossentropy",
                "optimizer": {
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
