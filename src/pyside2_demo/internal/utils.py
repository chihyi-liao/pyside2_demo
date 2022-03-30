import os
import sys

from pyside2_demo import __package__ as project


def get_resource(filename: str) -> str:
    return os.path.join(os.path.dirname(sys.modules[project].__file__), 'resource', filename)
