import os
import re
import time
from pathlib import Path

def sync(mod_files, update):
    for file in mod_files:
        lines = []
        relative = file.relative_to(folder_path)
        context = relative.as_posix()
        with file.open(encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    
        with file.open('w', encoding='utf-8') as outfile:
            i = 0
            while i < len(lines):
                if lines[i].strip() == "> BEGIN STRING":
                    i += 1
                    string = lines[i]
                    trans = update.get(string)
                    i += 1
                    while(lines[i][0] == ">"):
                        i += 1
                    if trans and string!=trans:
                        print(lines[i].strip()+" replaced by "+trans.strip()
                        lines[i] = trans

                    i += 2
                else:
                    i += 1
                
            outfile.writelines(lines)

if __name__ == "__main__":
    current_dir = Path.cwd()
    main_dir = current_dir.parent / Path().resolve().name.replace("patch","mod_patch")
    translations = {}

    main_files = [main_dir / "characters.txt"]
    mod_files = [current_dir / "characters.txt"]
    for file in (main_dir / "patch").rglob("*.txt"):
        main_files.append(file)
    for file in (current_dir / "patch").rglob("*.txt"):
        mod_files.append(file)

    print("===Reading current translations===")
    for translations_file in main_files:
        lines = []
        with translations_file.open('r', encoding='utf-8') as trans_file:
            lines = trans_file.readlines()
        i = 0
        while i < len(lines):
            if lines[i].strip() == "> BEGIN STRING":
                i += 1
                string = lines[i]
                i += 1
                while(lines[i][0] == ">"):
                    i += 1
                if lines[i].strip():
                    if string in translations:
                        print(translations[string]+" replaced by "+lines[i].strip()
                    translations[string] = lines[i]

                i += 2
            else:
                i += 1

    print("===Updating mod translations===")
    sync(mod_files, translations)
