#!/usr/bin/env python
import os
import sys
import zipfile


def zip_dir(dir_to_zip, zip_file_handle):
    for root, dirs, files in os.walk(dir_to_zip):
        for current_file in files:
            zip_file_handle.write(os.path.join(root, current_file))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        Exception('Must provide directory and output file name')
    out_file = sys.argv[2]
    in_folder = sys.argv[1]
    print("Zipping from {} into {}".format(in_folder, out_file))
    with zipfile.ZipFile(out_file, 'w', zipfile.ZIP_DEFLATED) as zip_file_handle:
        zip_dir(in_folder, zip_file_handle)
