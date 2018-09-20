import base64
import os
import sys


def rename_files(src_path, dst_path, map_func, filter_func):
    for base, dirs, files in os.walk(src_path):
        for filename in files:
            rel_path_name = os.path.relpath(os.path.join(base, filename), src_path)
            if filter_func(rel_path_name):
                dst_path_name = os.path.join(dst_path, map_func(rel_path_name))
                os.makedirs(os.path.dirname(dst_path_name), exist_ok=True)
                os.replace(os.path.join(src_path, rel_path_name), dst_path_name)


def rename_base64(name_path):
    dir_name, file_name_ext = os.path.split(name_path)
    file_name, file_ext = os.path.splitext(file_name_ext)
    file_name_base64 = base64.b64encode(file_name.encode('utf-8', errors='ignore')).decode('utf-8')
    return os.path.join(dir_name, ''.join([file_name_base64, file_ext]))


def filter_wav(name_path):
    return name_path.endswith('.mp3')


def main(src_path, dst_path):
    rename_files(src_path, dst_path, rename_base64, filter_wav)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
