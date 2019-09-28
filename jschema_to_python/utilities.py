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

def to_underscore_separated_name(name):
    result = ''
    first_char = True
    for ch in name:
        if ch.islower():
            next_char = ch
        else:
            next_char = ch.lower()
            if first_char:
                first_char = False
            else:
                next_char = '_' + next_char

        result += next_char
    return result

def unpickle_file(path):
    with open(path, mode='rt', encoding='utf-8') as file_obj:
        contents = file_obj.read()
        return jsonpickle.decode(contents)

def exit_with_error(message, *args):
    sys.stderr.write('error : ' + message.format(*args) + '\n')
    sys.exit(1)