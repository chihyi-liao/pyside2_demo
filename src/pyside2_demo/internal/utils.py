import os
from pkg_resources import resource_filename

from pyside2_demo import __package__ as project


def get_resource(filename: str) -> str:
    return resource_filename(project, os.path.join('resources', filename))
