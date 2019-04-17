#!/usr/bin/env python3
import argparse
import os
import json
from core import find_duplicate_files
from bonus import find_duplicate_files_by_cmp
import time


def parse_arguments():
    parser = argparse.ArgumentParser(prog='find_duplicate_file',
                                     description='find duplicate file')
    parser.add_argument('--path', action='store', default=os.getcwd(),
                        help='path of directory to find duplicate files')
    parser.add_argument('--method', action='store', default='core',
                        help='choose between core & bonus')
    return parser.parse_args()


def main():
    args = parse_arguments()
    dir = args.path
    method = args.method

    dup_files = find_duplicate_files_by_cmp(dir)

    dup_files_json = json.dumps(dup_files)
    return dup_files_json


if __name__ == '__main__':
    start = time.time()
    print(main())
    end = time.time()
    print(end - start)
