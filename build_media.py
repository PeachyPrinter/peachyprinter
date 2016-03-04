#!/usr/bin/env python
import os
import zipfile


def zip_dir(dir_to_zip, zip_file_name):
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zip_file_handle:
        files = os.listdir(dir_to_zip)
        files.sort()
        for current_file in files:
            print ("Processing: {}".format(current_file))
            zip_file_handle.write(os.path.join(dir_to_zip, current_file), current_file)

if __name__ == '__main__':
    current_file_path = os.path.dirname(os.path.realpath(__file__))
    media_path = os.path.join(current_file_path, 'media')
    output_path = os.path.join(current_file_path, 'src', 'resources', 'images')
    print ("Media Source: {}".format(media_path))
    print ("Media Destination: {}".format(output_path))
    for folder in os.listdir(media_path):
        source_path = os.path.join(media_path, folder)
        destination_file = os.path.join(output_path, folder + '.zip')
        print ("Zipping {} into {}".format(source_path, destination_file))
        zip_dir(source_path, destination_file)
        print ("Complete writing {}".format(destination_file))
