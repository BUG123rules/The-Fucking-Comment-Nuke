
import os
import sys
import re

def remove_comments_c_like(source):
    result = []
    in_block = False

    for line in source:
        i = 0
        length = len(line)
        new_line = ''
        in_string = False
        string_char = None

        while i < length:
            ch = line[i]
            nxt = line[i+1] if i+1 < length else ''

            
            if in_block:
                if ch == '*' and nxt == '/':
                    in_block = False
                    i += 2
                    continue
                else:
                    i += 1
                    continue

            
            if in_string:
                
                if ch == string_char:
                    
                    backslashes = 0
                    j = i - 1
                    while j >= 0 and line[j] == '\\':
                        backslashes += 1
                        j -= 1
                    if backslashes % 2 == 0:
                        in_string = False
                        string_char = None
                new_line += ch
                i += 1
                continue

            
            if ch in ('"', "'"):
                in_string = True
                string_char = ch
                new_line += ch
                i += 1
                continue

            
            if ch == '/' and nxt == '/':
                
                new_line += '\n'
                break

            
            if ch == '/' and nxt == '*':
                in_block = True
                i += 2
                continue

            
            new_line += ch
            i += 1

        result.append(new_line)

    return result

def remove_comments_python(source):
    result = []
    in_block = False
    block_delim = None

    for line in source:
        i = 0
        length = len(line)
        new_line = ''
        in_string = False
        string_char = None

        while i < length:
            ch = line[i]
            nxt3 = line[i:i+3]

            
            if in_block:
                if nxt3 == block_delim:
                    in_block = False
                    block_delim = None
                    i += 3
                    continue
                else:
                    i += 1
                    continue

            
            if in_string:
                if ch == string_char:
                    
                    backslashes = 0
                    j = i - 1
                    while j >= 0 and line[j] == '\\':
                        backslashes += 1
                        j -= 1
                    if backslashes % 2 == 0:
                        in_string = False
                        string_char = None
                new_line += ch
                i += 1
                continue

            
            if nxt3 in ("'''", '"""'):
                in_block = True
                block_delim = nxt3
                i += 3
                continue

            
            if ch in ('"', "'"):
                in_string = True
                string_char = ch
                new_line += ch
                i += 1
                continue

            
            if ch == '#':
                new_line += '\n'
                break

            
            new_line += ch
            i += 1

        result.append(new_line)

    return result

def remove_comments_asm(source):
    result = []
    for line in source:
        i = 0
        length = len(line)
        new_line = ''
        in_string = False
        string_char = None

        while i < length:
            ch = line[i]

            if in_string:
                if ch == string_char:
                    
                    backslashes = 0
                    j = i - 1
                    while j >= 0 and line[j] == '\\':
                        backslashes += 1
                        j -= 1
                    if backslashes % 2 == 0:
                        in_string = False
                        string_char = None
                new_line += ch
                i += 1
                continue

            
            if ch in ('"', "'"):
                in_string = True
                string_char = ch
                new_line += ch
                i += 1
                continue

            
            if ch in (';', '@'):
                new_line += '\n'
                break

            new_line += ch
            i += 1

        result.append(new_line)

    return result

def process_file(path, remover):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned = remover(lines)

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(cleaned)

def walk_directory(root, extensions, remover):
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames:
            lower_name = name.lower()
            if lower_name.endswith(extensions):
                full = os.path.join(dirpath, name)
                print(f"Cleaning {full} ...")
                process_file(full, remover)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python easyfuckingpeasy.py /path/to/project [language]")
        print("Languages: java (default), cpp, cs, python, javascript, assembly")
        sys.exit(1)

    root = sys.argv[1]
    if not os.path.isdir(root):
        print("Error: provided path is not a directory")
        sys.exit(1)

    
    language = sys.argv[2].lower() if len(sys.argv) == 3 else "java"

    
    if language == "java":
        extensions = (".java",)
        remover = remove_comments_c_like
        multi_mode = False
    elif language == "cpp":
        extensions = (".cpp", ".c++")
        remover = remove_comments_c_like
        multi_mode = False
    elif language == "cs":
        extensions = (".cs",)
        remover = remove_comments_c_like
        multi_mode = False
    elif language == "python":
        extensions = (".py", ".python")
        remover = remove_comments_python
        multi_mode = False
    elif language == "javascript":
        extensions = (".js", ".javascript")
        remover = remove_comments_c_like
        multi_mode = False
    elif language == "assembly":
        extensions = (".asm",)
        remover = remove_comments_asm
        multi_mode = False
    elif language == "all":
        
        extension_map = {
            ".java": remove_comments_c_like,
            ".cpp": remove_comments_c_like,
            ".c++": remove_comments_c_like,
            ".cs": remove_comments_c_like,
            ".py": remove_comments_python,
            ".python": remove_comments_python,
            ".js": remove_comments_c_like,
            ".javascript": remove_comments_c_like,
            ".asm": remove_comments_asm,
        }
        multi_mode = True
    else:
        print("Error: unknown language. Valid options are: java, cpp, cs, python, javascript, assembly, all")
        sys.exit(1)

    if multi_mode:
        for dirpath, dirnames, filenames in os.walk(root):
            for name in filenames:
                lower_name = name.lower()
                for ext, rm in extension_map.items():
                    if lower_name.endswith(ext):
                        full = os.path.join(dirpath, name)
                        print(f"Cleaning {full} ...")
                        process_file(full, rm)
        sys.exit(0)

    walk_directory(root, extensions, remover)