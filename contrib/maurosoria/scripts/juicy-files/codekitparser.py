#!/usr/bin/env python3
import sys
import json
import os

def parse_codekit(file_path):

    result_by_type = {}
    file_data = open(file_path).read()
    json_data = json.loads(file_data)
    for file_name in json_data['files'].keys():
        file_type = json_data['files'][file_name]['fileType']
        if result_by_type.get(file_type) is None:
            result_by_type[file_type] = []
        result_by_type[file_type].append(file_name)
    return result_by_type

def main():
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        print('Usage of {0}: config.codekit'.format(sys.argv[0]))
        exit(1)
    result_by_type = parse_codekit(sys.argv[1])
    for file_type in sorted(result_by_type.keys()):
        ext = os.path.splitext(result_by_type[file_type][0])[1][1:]
        print ("FILE_TYPE ID {0} {1}".format(file_type, ext))

        for file_path in result_by_type[file_type]:
            print(file_path)

if __name__ == '__main__':
    main()


