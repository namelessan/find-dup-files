import os
import hashlib


def scan_files(path):
    '''
    input: a directory path
    output: all absolute file path in the directory
    '''
    file_list = []
    for root, dirs, files in os.walk(path):
        if files:
            for name in files:
                file_path = os.path.join(root, name)
                if not os.path.islink(file_path):
                    file_list.append(file_path)
    return file_list


def get_file_size(file):
    try:
        file_size = os.path.getsize(file)
        return file_size
    except Exception:
        return 0


def group_files_by_size_first(file_list):
    '''
    input: list of file paths
    output: a dictionary with file size as key and files paths
            with same size as value'''
    group_files = {}
    for file in file_list:
        file_size = get_file_size(file)
        if file_size == 0:
            continue
        elif file_size not in group_files:
            group_files[file_size] = [file]
        else:
            group_files[file_size].append(file)
    return group_files


def group_files_by_size(file_list):
    '''
    input: list of file paths
    output: nested list of files with same size
    '''
    group_multi_files = []
    group_files = group_files_by_size_first(file_list)
    for _, files in group_files.items():
        if len(files) >= 2:
            group_multi_files.append(files)
    return group_multi_files


def generate_md5(filename):
    '''
    input: absolute file path
    output: md5 of the a single file
    '''
    hash_md5 = hashlib.md5()
    try:
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except PermissionError:
        return 'permission deny'


def group_files_by_checksum_dict(file_list):
    '''
    input: alist of file have same size
    output: a dictionary with key is md5 and value is files have same md5
    '''
    group_files = {}
    for file in file_list:
        hash_md5 = generate_md5(file)
        if hash_md5 in 'permission deny':
            continue
        elif hash_md5 not in group_files:
            group_files[hash_md5] = [file ]
        else:
            group_files[hash_md5].append(file)
    return group_files


def group_files_by_checksum(file_list):
    '''
    input: a list of file have same size
    output: a list of file have same size and content(or md5)
    '''
    group_multi_file = []
    group_files = group_files_by_checksum_dict(file_list)
    for _, files in group_files.items():
        # keep files have same md5, remove others
        if len(files) >= 2:
            group_multi_file.append(files)
    return group_multi_file


def group_duplicate_files(file_groups):
    '''
    input: a nested list of file have same size
    output: a nested list of file have same size and checksum
    '''
    dup_files = []
    for group in file_groups:
        group_md5 = group_files_by_checksum(group)
        if group_md5:
            dup_files.extend(group_md5)
    return dup_files


def find_duplicate_files(dir):
    file_paths = scan_files(dir)
    group_size = group_files_by_size(file_paths)
    dup_files = group_duplicate_files(group_size)
    return dup_files
