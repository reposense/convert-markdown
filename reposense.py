import json
import os

import sys


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

INPUT_FILE = "authorship.json"
OUTPUT_PATH = "output"

if __name__ == "__main__":
    """
    Input parameters serve as inclusive extensions.
    e.g. `python3 reposense.py java fxml`
    """
    inclusive_exts = sys.argv[1:] if len(sys.argv) > 1 else []

    if os.path.isfile(INPUT_FILE):
        with open(INPUT_FILE, 'r') as file:
            data_files = json.load(file)

    db = {}
    for data in data_files:
        last_author = ""
        filename = data['path']
        ext = os.path.splitext(filename)[1].replace('.', '')
        if ext not in inclusive_exts and len(inclusive_exts) > 0:
            continue

        for line in data['lines']:
            try:
                author = line['author']['gitId']
            except Exception as e:
                author = "-"

            if author != last_author:
                close_file_header(db, last_author)
                create_author_if_not_exist(db, author)
                add_file_header(db, author, filename)

            add_line_to_author(db, author, line)
            last_author = author

        close_file_header(db, last_author)

    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    filter_low_contrib(db, 3)
    for author in db:
        with open(os.path.join(OUTPUT_PATH, author + ".md"), 'w') as file:
            file.write('\n'.join(db[author]))
