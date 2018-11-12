import argparse
import json
import os

import sys

REPOSENSE_FOLDER_NAME = 'reposense-report'
AUTHORSHIP_FILE = "authorship.json"
OUTPUT_FOLDER = "output"


def create_author_if_not_exist(db, author):
    if author not in db and author not in ["-", ""]:
        db[author] = ["# " + author]


def add_file_header(db, author, filename):
    if author in db:
        ext = os.path.splitext(filename)[1].replace('.', '')
        db[author].append("###### " + filename)
        db[author].append("```" + ext)


def close_file_header(db, author):
    if author in db:
        db[author].append("```")


def add_line_to_author(db, author, line):
    if author in db:
        db[author].append(line['content'])


def filter_low_contrib(db, min_count=3):
    min_count += 3 # include the 2 header and 1 eof lines
    for author in db:
        start_index = 0
        index = 0
        lines = db[author]
        new_lines = []
        for line in lines:
            if line.startswith("######"):
                start_index = index
            elif line.endswith("```") and index - start_index >= min_count:
                new_lines += lines[start_index:index+1]

            index += 1
        db[author] = new_lines


def get_authorship_files(directory):
    result = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(AUTHORSHIP_FILE):
                result.append(os.path.join(root, file))

    return result


def parse_args():
    parser = argparse.ArgumentParser(
            description='Convert authorship.json generated by RepoSense.jar to markdown documents.')
    parser.add_argument('--formats', nargs='+',
            help='File formats to be included. Default: all files will be included.')
    parser.add_argument('--directory', nargs='?', default='.',
            help='Directory containing the reposense-report for conversion. Default: current working directory.')
    args = parser.parse_args(sys.argv[1:])
    return vars(args)

if __name__ == "__main__":
    args = parse_args()
    inclusive_exts = args['formats']
    input_directory = args['directory'] # where to look for reposense-report folder

    file_list = get_authorship_files(input_directory)

    for file in file_list:
        with open(file, 'r') as f:
            data_files = json.load(f)
        db = {}
        for data in data_files:
            last_author = ""
            data_filename = data['path']
            ext = os.path.splitext(data_filename)[1].replace('.', '')
            if inclusive_exts is not None and ext not in inclusive_exts and len(inclusive_exts) > 0:
                continue

            for line in data['lines']:
                try:
                    author = line['author']['gitId']
                except Exception as e:
                    author = "-"

                if author != last_author:
                    close_file_header(db, last_author)
                    create_author_if_not_exist(db, author)
                    add_file_header(db, author, data_filename)

                add_line_to_author(db, author, line)
                last_author = author

            close_file_header(db, last_author)

        output_path = OUTPUT_FOLDER + os.path.dirname(file.split(REPOSENSE_FOLDER_NAME, 1)[1])
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        filter_low_contrib(db, 3)
        for author in db:
            with open(os.path.join(output_path, author + ".md"), 'w') as f:
                f.write('\n'.join(db[author]))