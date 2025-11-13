#!/usr/bin/env python3
import os
import sys
import re

def remove_comments(source):
    result = []
    in_block = False
    i = 0

    while i < len(source):
        line = source[i]

        if not in_block:
            # Look for start of block comment
            start = line.find("/*")
            slc = line.find("//")

            if start == -1 and slc == -1:
                # No comments at all
                result.append(line)
            else:
                # Case: a single-line comment appears first
                if slc != -1 and (start == -1 or slc < start):
                    result.append(line[:slc] + "\n")
                else:
                    # Block comment starts
                    before = line[:start]
                    end = line.find("*/", start + 2)
                    if end != -1:
                        # Comment ends on the same line
                        after = line[end+2:]
                        # Recursively clean the remainder of this line
                        cleaned = remove_comments([before + after])
                        result.extend(cleaned)
                    else:
                        # Block comment continues to future lines
                        in_block = True
                        result.append(before + "\n")
        else:
            # Currently inside /* ... */ block
            end = line.find("*/")
            if end != -1:
                # Block ends here
                after = line[end+2:]
                in_block = False
                cleaned = remove_comments([after])
                result.extend(cleaned)
            # Otherwise skip the whole line

        i += 1

    return result

def process_file(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned = remove_comments(lines)

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(cleaned)

def walk_directory(root):
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".java"):
                full = os.path.join(dirpath, name)
                print(f"Cleaning {full} ...")
                process_file(full)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python remove_all_java_comments.py /path/to/project")
        sys.exit(1)

    root = sys.argv[1]
    if not os.path.isdir(root):
        print("Error: provided path is not a directory")
        sys.exit(1)

    walk_directory(root)