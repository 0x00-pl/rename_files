import base64
import json
import os
import sys


def rename_files(src_path, dst_path, map_func, filter_func):
    mapping = []
    for base, dirs, files in os.walk(src_path):
        for filename in files:
            rel_path_name = os.path.relpath(os.path.join(base, filename), src_path)
            if filter_func(rel_path_name):
                dst_path_name = os.path.join(dst_path, map_func(rel_path_name))
                os.makedirs(os.path.dirname(dst_path_name), exist_ok=True)
                src_path_name = os.path.join(src_path, rel_path_name)
                print('mv', src_path_name, dst_path_name)
                mapping.append([src_path_name, dst_path_name])
                os.replace(src_path_name, dst_path_name)
    return mapping


def rename_base64(name_path):
    dir_name, file_name_ext = os.path.split(name_path)
    file_name, file_ext = os.path.splitext(file_name_ext)
    file_name_base64 = base64.b64encode(file_name.encode('utf-8', errors='ignore')).decode('utf-8')
    return os.path.join(dir_name, ''.join([file_name_base64, file_ext]))


def rename_seq():
    seq = [0]

    def rename_seq(name_path):
        dir_name, file_name_ext = os.path.split(name_path)
        file_name, file_ext = os.path.splitext(file_name_ext)
        file_name_seq = str(seq[0])
        seq[0] = seq[0] + 1
        return os.path.join(dir_name, ''.join([file_name_seq, file_ext]))

    return rename_seq


def filter_wav(name_path):
    return name_path.endswith('.mp3')


def main(src_path, dst_path, mapping_file='mapping.json'):
    mapping = rename_files(src_path, dst_path, rename_seq(), filter_wav)
    json.dump(mapping, open(mapping_file, 'w'), ensure_ascii=True)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
