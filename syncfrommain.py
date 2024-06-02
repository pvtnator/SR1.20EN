import os
import re
import time
from pathlib import Path

def sync(file, update, txstrdir=0):
    lines = []
    try:
        with file.open(encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("File not found")
        return

    with file.open('w', encoding='utf-8') as outfile:
        i = 0
        while i < len(lines):
            if lines[i].strip() == "> BEGIN STRING":
                i += 1
                string = lines[i]
                i += 1
                while(lines[i][0] != ">"):
                    string += lines[i]
                    i += 1
                while(lines[i][0] == ">"):
                    i += 1
                trans = update.get(string)
                if not trans and txstrdir!=0:
                    string = string.replace('\\', '\\\\')
                    withquote = '"'+string.strip()+'"'+"\n"
                    #print(withquote)
                    trans = update.get(withquote)
                    if trans:
                        trans = trans.replace('"','').replace('\\\\', '\\')
                old = lines[i]
                for k in range(5):
                    if lines[i+k+1][0]!=">":
                        old+=lines[i+k+1]
                    else:
                        break
                if trans and old!=trans:
                    #print(string+" replaced by "+trans)
                    lines[i] = trans
                    i+=1
                    while(lines[i][0] != ">"):
                        lines[i]=""
                        i += 1

                i += 1
            else:
                i += 1
            
        outfile.writelines(lines)

if __name__ == "__main__":
    current_dir = Path.cwd()
    main_dir = current_dir.parent / Path().resolve().name.replace("mod_patch","patch")

    main_files = [main_dir / "characters.txt"]
    for file in (main_dir / "patch").rglob("*.txt"):
        main_files.append(file)

    #print("===Reading current translations===")
    for file in main_files:
        translations = {}
        print(file.as_posix())
        lines = []
        with file.open('r', encoding='utf-8') as trans_file:
            lines = trans_file.readlines()
        i = 0
        while i < len(lines):
            if lines[i].strip() == "> BEGIN STRING":
                i += 1
                string = lines[i]
                i += 1
                while(lines[i][0] != ">"):
                    string += lines[i]
                    i += 1
                while(lines[i][0] == ">"):
                    i += 1
                if lines[i].strip():
                    if string in translations.keys() and translations[string] != lines[i]:
                        print(translations[string].strip()+" replaced by "+lines[i].strip())
                    translations[string] = lines[i]
                    i+=1
                    while(lines[i][0] != ">"):
                        translations[string] += lines[i]
                        i+=1
                i += 1
            else:
                i += 1

        #print("===Updating mod translations===")
        #if "characters" in file.as_posix():
        #    sync(current_dir / "talk.txt", translations)
        else:
            #sync(current_dir / file.relative_to(main_dir), translations)
            if "Scripts" in file.as_posix():
                sync(current_dir / "mod_scripts.txt", translations, 1)
