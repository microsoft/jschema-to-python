import os
import shutil
import sys

import jsonpickle

def capitalize_first_letter(identifier):
    return identifier[0].capitalize() + identifier[1:]

def create_directory(directory, force):
    if os.path.exists(directory):
        if force:
            shutil.rmtree(directory, ignore_errors=True)
        else:
            exit_with_error('output directory {} already exists', directory)

    os.makedirs(directory)

def unpickle_file(path):
    with open(path, mode='rt', encoding='utf-8') as file_obj:
        contents = file_obj.read()
        return jsonpickle.decode(contents)

def exit_with_error(message, *args):
    sys.stderr.write('error : ' + message.format(*args) + '\n')
    sys.exit(1)