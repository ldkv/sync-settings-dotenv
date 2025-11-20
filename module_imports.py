import importlib.util
import sys
from inspect import isclass
from pathlib import Path
from typing import Type

from pydantic_settings import BaseSettings

SUPPORTED_MODELS = (BaseSettings,)


def import_isolated_module(dotted_module_name: str) -> Type[BaseSettings]:
    """
    Loads the class from the specified module path without
    executing the module's side effects
    """
    # Create a module spec from the file path
    sys.path.insert(0, ".")
    spec = importlib.util.find_spec(dotted_module_name)
    if not spec or not spec.origin:
        raise ImportError(f"Could not find module spec for {dotted_module_name}")

    # Create a new module object
    module = importlib.util.module_from_spec(spec)
    module_path = Path(spec.origin)

    # Read the source code of the module
    with open(module_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    exec_code = filter_necesary_code(source_code)

    exec(exec_code, module.__dict__)

    # Retrieve the classes from the isolated module
    for cls in module.__dict__.values():
        if isclass(cls) and issubclass(cls, SUPPORTED_MODELS) and cls.__module__.startswith(dotted_module_name):
            return cls

    raise ImportError(f"No BaseSettings subclass found in module {module_path}.")


def filter_necesary_code(source_code: str):
    """Only import code related to BaseSettings"""
    lines = source_code.splitlines()
    for i, line in enumerate(lines):    
        
        

if __name__ == "__main__":
    import_isolated_module("tests.test_command")
