import os
import re
import time
from pathlib import Path

def sync(files, update, txstrdir=0):
    for file in files:
        lines = []
        with file.open(encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    
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
                    if not trans and string.strip() in update:
                        trans = string.replace(string.strip(),update[string.strip()])
                    if trans and lines[i].strip()!=trans.strip():
                        print(lines[i].strip()+" replaced by "+trans.strip())
                        lines[i] = trans.replace("\n\n","\n")
                    elif lines[i].strip():
                        if string[0]=='"' and txstrdir==0:
                            noquote = string.replace('"','')
                            trans = update.get(noquote)
                            if trans:
                                lines[i] = string.replace(noquote.strip(), trans.strip())
                                #print("Text to string: "+lines[i].strip())
                        elif txstrdir!=0:
                            withquote = '"'+string.strip()+'"'+"\n"
                            trans = update.get(withquote)
                            if trans:
                                lines[i] = trans.replace('"','')
                                #print("String to text: "+lines[i].strip())

                    i += 2
                else:
                    i += 1
                
            outfile.writelines(lines)

def ReduceLinebreaks(file):
    lines = []
    with file.open(encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

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
                brk = "\\n　" if "　" in string else "\\n"
                if "　" in string:
                    lines[i] = lines[i].replace("\\n","\\n　")
                    lines[i] = lines[i].replace("　　","　")
                elif "\\n" in string:
                    lines[i] = lines[i].replace("\\n　","\\n")
                if lines[i].count(brk)>3:
                    prevpos = 0
                    smallest = 999
                    smallestIndex = -1
                    while prevpos < len(lines[i].strip()):
                        index = lines[i].find(brk, prevpos+1)
                        newindex = lines[i].find(brk, index+1)
                        newindex = len(lines[i].strip()) if newindex<0 else newindex
                        newlen = newindex-prevpos
                        if newindex-index < smallest and newlen < 60:
                            smallestIndex = index
                            smallest = newindex-index
                        index = newindex
                        prevpos = index
                    if smallestIndex >= 0:
                        index = smallestIndex
                        lines[i] = lines[i][0:index]+" "+lines[i][index+len(brk):]
                        lines[i] = lines[i].replace("  ", " ")
                    #lines[i] = lines[i].replace(brk, "", 1)
                    #rindex = lines[i].rfind(brk)
                    #if len(lines[i])-rindex<20:
                    #    lines[i] = lines[i][0:rindex]+lines[i][rindex+len(brk):]
                    
            i += 2
        else:
            i += 1

    with file.open('w', encoding='utf-8') as outfile:  
        outfile.writelines(lines)

if __name__ == "__main__":
    current_dir = Path.cwd()
    translations = {}

    #source_files = [current_dir / "mod_scripts.txt"]
    source_files = [current_dir / "patch" / "Armors.txt"]
    source_files += [current_dir / "patch" / "Skills.txt"]
    source_files += [current_dir / "patch" / "Items.txt"]
    dest_files = [current_dir / "mod_scripts.txt"]
    #for file in (current_dir / "patch").rglob("*.txt"):
    #    if not "Unused" in str(file) and not "States" in str(file):
    #        dest_files.append(file)

    print("===Reading current translations===")
    for translations_file in source_files:
        print(translations_file.as_posix())
        lines = []
        with translations_file.open('r', encoding='utf-8') as trans_file:
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
                    if "/" in string:
                        translations[string.split("/")[0]] = lines[i].split("/")[0]
                        #print(string.split("/")[0]+" = "+lines[i].split("/")[0])
                    else:
                        translations[string] = lines[i]
                    #print(string.strip()+" = "+lines[i].strip())

                i += 2
            else:
                i += 1

    print("===Updating mod translations===")
    #ReduceLinebreaks(current_dir / "talk.txt")
    #sync([current_dir / "mod_scripts.txt"], translations, 0)
    #sync([current_dir / "mod_scripts.txt"], translations, 1)
    sync(dest_files, translations, 0)
    sync(dest_files, translations, 1)
