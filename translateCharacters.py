import os
import re
import pyperclip
import time
from pathlib import Path

def extract_strings(folder_path, output_file, update={}):
    strings = {}

    # Walk through all files in the folder and its subfolders
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".rb"):
                file_path = os.path.join(root, file)
                context = file_path[len(folder_path)+1:]
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all strings in the file
                found_strings = re.findall(r'"「(.*?)」"', content)
                
                # Add found strings to the dictionary with their contexts
                for string in found_strings:
                    if string:
                        if string not in strings:
                            strings[string] = [context]
                        elif not context in strings[string]:
                            strings[string].append(context)
    
    # Write the strings and their contexts to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for string, contexts in strings.items():
            outfile.write("> BEGIN STRING\n")
            outfile.write(f'{string}\n')
            for context in contexts[:10]:
                outfile.write(f"> CONTEXT: {context}\n")
            if string in update:
                outfile.write(update[string])
            outfile.write("\n> END STRING\n\n")

def autotranslate(translations_file, lines):
    i = 0
    batchi = []
    batcht = ""
    while i < len(lines):
        if lines[i].strip() == "> BEGIN STRING":
            i += 1
            string = lines[i]
            i += 1
            contexts = []
            while(lines[i][0] == ">"):
                context = lines[i][11:].strip()
                contexts.append(context)
                i += 1
            if lines[i].strip() == "" and len(contexts)<10 and len(string)>3:
                batchi.append(i)
                batcht += string.replace("#{myname}", "私").replace("#{target}", "あなた")
                if len(batchi)>=50:
                    print("\n"+batcht+"\n")
                    pyperclip.copy(batcht)
                    while(pyperclip.paste() == batcht or len(pyperclip.paste().split("\n")) != len(batcht.split("\n"))):
                        time.sleep(0.5)
                    trlines = pyperclip.paste().split("\n")
                    for j in range(50):
                        translated = trlines[j].strip()
                        if len(translated) > 3:
                            print(translated)
                            if translated[-1] == "." and translated[-2] != ".":
                                translated = translated[:-1]
                            translated = translated.replace("\\n", "\\n　")
                            translated = translated.replace("　　", "　").replace("　 ", "　")
                            #translated = re.sub("[^\.]\\\\H", "\\\\H", translated)
                            lines[batchi[j]] = translated+"\n"
                            print(lines[batchi[j]])
                    batchi.clear()
                    batcht = ""
                    with open(translations_file, 'w', encoding='utf-8') as trans_file:
                        trans_file.writelines(lines)
            i += 2
        else:
            i += 1

def apply_translations(folder_path, translations, mustinclude=""):
    glpattern = re.compile("|".join(re.escape(key) for key in sorted(translations["global"].keys(), key=len, reverse=True)))
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".rb") and mustinclude in root:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                context = file_path[len(folder_path)+1:]
                if context in translations:
                    pattern = re.compile("|".join(re.escape(key) for key in sorted(translations[context].keys(), key=len, reverse=True)))
                    content = pattern.sub(lambda match: translations[context][match.group(0)], content)
                content = glpattern.sub(lambda match: translations["global"][match.group(0)], content)
                
                #for string, translation in translations.items():
                #    content = content.replace(string, translation)

                outpath = file_path.replace("System\\talk", "Mod\\Mod_Talk")
                Path(outpath).parent.mkdir(parents=True, exist_ok=True)
                with open(outpath, 'w', encoding='utf-8') as outfile:
                    outfile.write(content)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    folder_name = current_dir.split("\\")[-1].replace("_patch", "_translated")
    folder_path = os.path.join(parent_dir, folder_name+"\\System\\talk")
    translations_file = "characterstest.txt"
    translations = {"global": {}}

    lines = []
    with open(translations_file, 'r', encoding='utf-8') as trans_file:
        lines = trans_file.readlines()
    i = 0
    while i < len(lines):
        if lines[i].strip() == "> BEGIN STRING":
            i += 1
            string = lines[i].strip()
            i += 1
            contexts = []
            while(lines[i][0] == ">"):
                context = lines[i][11:].strip()
                contexts.append(context)
                i += 1
            if lines[i].strip():
                if len(contexts)>=10:
                    translations["global"]["\""+string+"\""] = "\""+lines[i].strip()+"\""
                    translations["global"]["「"+string+"」"] = "「"+lines[i].strip()+"」"
                else:
                    for c in contexts:
                        if not c in translations:
                            translations[c] = {}
                        translations[c]["\""+string+"\""] = "\""+lines[i].strip()+"\""
                        translations[c]["「"+string+"」"] = "「"+lines[i].strip()+"」"
            i += 2
        else:
            i += 1

    print(translations["global"])
    mode = "autotranslate"
    if mode == "extract":
        extract_strings(folder_path, translations_file, translations)
        print("Extraction completed.")
    elif mode == "apply":       
        apply_translations(folder_path, translations)
        print("Translations applied.")
    elif mode == "autotranslate":
        autotranslate(translations_file, lines)
        print("Autotranslate done.")
