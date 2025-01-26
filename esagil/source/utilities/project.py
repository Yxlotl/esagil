from sys import argv
from os import path

# Project
PROJECT_NAME = 'esagil'

# Resources
_current_script = path.realpath(argv[0])
RESOURCE_DIRECTORY = path.abspath(path.normpath(f'{_current_script[0:_current_script.rfind(PROJECT_NAME) + len(PROJECT_NAME) + 1]}/resources'))

def get_resource(file_name):
    desired_resource = f'{RESOURCE_DIRECTORY}/{file_name}'

    # Ensure that the desired resource is in the resource directory
    if path.exists(desired_resource) and path.commonpath([RESOURCE_DIRECTORY, desired_resource]) == RESOURCE_DIRECTORY:
        return path.abspath(path.normpath(desired_resource))
    else:
        raise FileNotFoundError(f'Resource not found: {desired_resource}')
