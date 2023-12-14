import os

def find_path(file_name = ''):
    if file_name:
        main_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(main_dir, file_name)
        return file_path
    else:
        return os.path.dirname(os.path.realpath(__file__))