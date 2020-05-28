''' Utility functions for code generators.

These functions help with using object formats that were created specifically for 
the PythonGenerator and JsonGenerator class hierarchies. 

'''

import numpy as np


def _is_valid_arg_dict(arg_dict):
    ''' Check if arguments are formatted correctly in the argument dictionary.

    An arg dict defines all arguments to a function as param:value paries. They must follow the 
    rules of standard Python arguments. Args with default parameters must come after args without. 
    All keys in the dict must be of type string.

    Values may take the forms::
        string: To represent any object. Will be generated as code, not a string.
        int/float: To represent a number value.
        list of strings, ints, or floats: When an arg requires multiple values.
        dict: To represent a function being passed as a value.
        None: This can be used to signify there is no default parameter.
    This function raises exceptions if any of these rules are not followed.

    Args:
        arg_dict (dict): Method arguments in the form {"param" : "value"}. Refer to above for how
            to format an argument dictionary.

    Raises:
        TypeError: Arguments must be formatted as a dictionary.
        ValueError: All None values must come before all string values.
        TypeError: All keys must be strings and all values must be strings or None.

    '''

    if arg_dict:
        if not isinstance(arg_dict, dict):
            raise TypeError("Arguments must be formatted as a dictionary.")

        def allowed_val_type(val):
            return (isinstance(val, (dict, float, int, list, str)) or val is None)

        # Check that all keys are strings and all vals are string, int or None
        all_str_keys = [isinstance(k, str) for k in arg_dict.keys()]
        all_str_vals = [allowed_val_type(v) for v in arg_dict.values()]

        # Check for default parameters before args w/o default parameters
        bad_arg_order = False
        default_param = False
        for val in arg_dict.values():
            if val and not default_param:
                default_param = True
            elif not val and default_param:
                bad_arg_order = True

        if bad_arg_order:
            raise ValueError("All None values must come before all string values.")
        if not np.all(all_str_keys) or not np.all(all_str_vals):
            raise TypeError("All keys must be strings and all values must be strings, \
                    int, float, or None.")


def _is_valid_fn_dict(fn_dict):
    ''' Check if function is formatted correctly in a dictionary.

    The function dictionary must be correctly formatted so it can be parsed. It must have two
    keys: "name" and "args". The value of "name" must be a string, and args must be formatted
    as an arg_dict (see _is_valid_arg_dict for that format). Any input deviating from this will
    raise an exception.

    Args:
        fn_dict (dict): Represents a function name and its arguments.

    Raises:
        TypeError: Input must be of type dict.
        ValueError: Must have a "name" key in the dict.
        ValueError: Must have an "args" key in the dict.
        ValueError: The only keys must be "name' and "args".
        TypeError: Function name must be a string.

    '''

    if not isinstance(fn_dict, dict):
        raise TypeError("fn_dict must be of type dict.")

    if "name" not in fn_dict:
        raise ValueError("Must have a \"name\" key in the dict.")

    if "args" not in fn_dict:
        raise ValueError("Must have an \"args\" key in the dict.")

    for param in fn_dict.keys():
        if param != "name" and param != "args":
            raise ValueError("The only keys must be \"name\" and \"args\".")

    if not isinstance(fn_dict["name"], str):
        raise TypeError("Function name must be a string.")

    _is_valid_arg_dict(fn_dict["args"])


def create_fn_dict(name, args=None):
    ''' Creates a dictionary representation of a function.
        
        This function exists so the user doesn't have to worry about the internal representation
        of a function in the JSON file.

        Args:
            name (str): Name of the function.
            args (dict): Function arguments as {"parameter" : "value"} elements. Refer to
                _is_valid_arg_dict() docstring for formatting.

        Returns:
            dict: The formatted function.

        Example:
            >>> function_name = "flatten"
            >>> args = {
            >>>    "input_shape" : [28, 28, 1],
            >>>    "parameter" : "value"
            >>> }
            >>> print(create_fn_dict(function_name, args))
            ::
                {
                    "name" : "flatten",
                    "args" : {
                        "input_shape" : [28, 28, 1],
                        "parameter" : "value"
                    }
                }

    '''
    
    # Raise exceptions if args incorrectly formatted
    _is_valid_arg_dict(args)

    return {
        "name": name,
        "args": args if args else None
    }
