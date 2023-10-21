'''Useful module-related functions.'''


import importlib
import types

from python_compatibility import is_string


SEP = '.'


def get_module_path(module_input):
    '''Get path of given module or string representation of module (ie. 'os.path', 'os.path.join').

    Args:
        module_input (module or str): Python module or string representation of module (ie.
            'os.path').

    Returns:
        str: File path of specified module

    Raises:
        TypeError: If the module_input is not a string or types.ModuleType.
        ModuleNotFoundError: If the specified module is not found.
        RuntimeError: If parent module exists, but doesn't contain last item.
    '''
    if isinstance(module_input, types.ModuleType):
        return module_input.__file__

    if not is_string(module_input):
        raise TypeError(f'Unsupported module type: {type(module_input)}')

    try:
        module = importlib.import_module(module_input)
    except ModuleNotFoundError as err:
        # Maybe the last item is a function/class/variable, and the previous part is a module.
        # For example: 'os.path.dirname'. See if os.path is the module and dirname is part of it.
        if SEP in module_input:
            # Split last item after SEP.
            items = module_input.split(SEP)
            module_input_prev = SEP.join(items[:-1])
            last_item = items[-1]

            try:
                module = importlib.import_module(module_input_prev)
            except ModuleNotFoundError as err:
                raise err(f'Could not find module in {module_input} nor {module_input_prev}')
            else:
                if hasattr(module, last_item):
                    return module.__file__

                # Module does exist, but doesn't contain last item.
                raise RuntimeError(
                    f"Module {module_input_prev} exists, but doesn't contain {last_item}")
        raise err
    else:
        return module.__file__


def print_module_path(module_input):
    print(get_module_path(module_input))
