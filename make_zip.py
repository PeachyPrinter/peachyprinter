#!/usr/bin/env python
import os
import sys
import zipfile


def zip_dir(dir_to_zip, zip_file_handle):
    for root, dirs, files in os.walk(dir_to_zip):
        for current_file in files:
            zip_file_handle.write(os.path.join(root, file))

if __name__ == '__main__':
    if len(sys.argsv) != 3:
        Exception('Must provide directory and output file name')
    with zipfile.ZipFile(sys.argsv[2], 'w') as zip_file_handle:
        zip_dir(sys.argsv[1], zip_file_handle)
