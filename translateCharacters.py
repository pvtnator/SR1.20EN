import os
import re
import time
from pathlib import Path

def extract_strings(folder_path, output_file, update={}):
    strings = {}

    # Walk through all files in the folder and its subfolders
    for file in folder_path.rglob("*.rb"):
        relative = file.relative_to(folder_path)
        context = relative.as_posix()
        with file.open(encoding='utf-8') as f:
            content = f.read()
        
        # Find all strings in the file
        found_strings = re.findall(r'"「{0,}(.*?)」{0,}"', content)
        
        # Add found strings to the dictionary with their contexts
        for string in found_strings:
            if string:
                try:
                    string.encode("utf-8").decode("ascii")
                except UnicodeDecodeError:
                    if string not in strings:
                        strings[string] = [context]
                    elif not context in strings[string]:
                        strings[string].append(context)
    
    # Write the strings and their contexts to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for string, contexts in strings.items():
            outfile.write("> BEGIN STRING\n")
            outfile.write(f'{string}\n')
            if len(contexts) > 30:
                outfile.write(f"> CONTEXT: global\n")
            else:
                for context in contexts:
                    outfile.write(f"> CONTEXT: {context}\n")
                    
            qstring = "\""+string+"\""
            if (contexts[0] in update and qstring in update[contexts[0]]):
                outfile.write(update[contexts[0]][qstring][1:-1])
            elif qstring in update["global"]:
                outfile.write(update["global"][qstring][1:-1])
            else:
                print(string)
            outfile.write("\n> END STRING\n\n")

def autotranslate(translations_file, lines):
    import pyperclip
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
            if lines[i].strip() == "" and ("\\\\H" in string or "\\n" in string or len(contexts)<10):
                batchi.append(i)
                string = string.replace("#{myname}", "私").replace("#{target}", "あなた")
                string = string.replace("アソコ", "おまんこ").replace("ココ", "おまんこ")
                
                string = "女："+string
                batcht += string
                if i > len(lines)-10 or len(batcht)>4500:
                    batcht = batcht.strip()
                    #print("\n"+batcht+"\n")
                    print(str(100*i/len(lines))+"%\n")
                    pyperclip.copy(batcht)
                    while(pyperclip.paste() == batcht or len(pyperclip.paste().split("\n")) != len(batcht.split("\n"))):
                        time.sleep(0.5)
                    trlines = pyperclip.paste().split("\n")
                    for j in range(len(trlines)):
                        translated = trlines[j].strip()
                        if len(translated) > 3:
                            #print(translated)
                            if translated[-1] == "." and translated[-2] != ".":
                                translated = translated[:-1]
                            translated = translated[7:]
                            translated = translated.replace("\\n", "\\n　")
                            translated = translated.replace("　　", "　").replace("　 ", "　")
                            translated = translated.replace("…", "...")
                            translated = translated.replace("#", "").replace("{", "#{")
                            translated = translated.replace(" \\\\H", "\\\\H")
                            translated = translated.replace(".\\\\H", "\\\\H")
                            translated = translated.replace("Giggle", "*Giggle*")
                            translated = re.sub("\.{2,}", "...", translated)
                            translated = re.sub("a{3,}", "aaa", translated)
                            translated = re.sub("o{3,}", "ooo", translated)
                            #translated = re.sub(r"([^\.])\.\\H", r"\1\\H", translated)
                            parts = translated.split("\\n")
                            translated = ""
                            for p in parts:
                                if len(p) > 50 and p.find(" ", 40) >= 0:
                                    p = p[:p.find(" ", 40)]+"\\n　"+p[p.find(" ", 40)+1:]
                                translated += p if translated=="" else "\\n"+p
                                    
                            lines[batchi[j]] = translated+"\n"
                            #print(lines[batchi[j]])
                    batchi.clear()
                    batcht = ""
                    with open(translations_file, 'w', encoding='utf-8') as trans_file:
                        trans_file.writelines(lines)
            i += 2
        else:
            i += 1

def apply_translations(folder_path, apply_path, regexes, translations, mustinclude=""):
    glpattern = re.compile("|".join(re.escape(key) for key in sorted(regexes["global"], key=len, reverse=True)))
    for file in folder_path.rglob("*"):
        relative = file.relative_to(folder_path)
        if "omake" in relative.as_posix():
            continue
        target_path = apply_path / relative
        if file.is_dir():
            print(target_path)
            target_path.mkdir(parents=True, exist_ok=True)
        elif mustinclude in file.name and ".rb" in file.name:
            #file_path = Path.join(root, file)
            with file.open(encoding='utf-8') as f:
                content = f.read()

            context = relative.as_posix()
            if context in translations:
                pattern = re.compile("|".join(key for key in sorted(regexes[context], key=len, reverse=True)))
                content = pattern.sub(lambda match: translations[context][match.group(0)], content)
            content = glpattern.sub(lambda match: translations["global"][match.group(0)], content)

            with target_path.open(mode='w', encoding='utf-8') as outfile:
                outfile.write(content)

if __name__ == "__main__":
    current_dir = Path.cwd()
    translated_dir = current_dir.parent / Path().resolve().name.replace("patch","mod_translated")
    talk_dir = translated_dir / "System" / "talk"
    modtalk_dir = translated_dir / "Mod" / "Mod_Talk"
    translations_file = "characters.txt"
    translations = {"global": {}}
    regexes = {"global": []}
    print(talk_dir)

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
                context = context.replace("\\", "/")
                contexts.append(context)
                i += 1
            if lines[i].strip():
                for c in contexts:
                    if not c in translations:
                        translations[c] = {}
                        regexes[c] = []
                    regexes[c].append(re.escape(string))
                    translations[c][string] = lines[i].strip()
                    #print(string)
                    #print(r'"「{0,}('+re.escape(string)+r')」{0,}"')
            i += 2
        else:
            i += 1

    #print(translations["global"])
    mode = "extract"
    print("Mode: "+mode+"\nThis might take a minute")
    if mode == "extract":
        extract_strings(talk_dir, translations_file, translations)
        print("Extraction completed.")
    elif mode == "apply":       
        apply_translations(talk_dir, modtalk_dir, regexes, translations)
        print("Translations applied.")
    elif mode == "autotranslate":
        autotranslate(translations_file, lines)
        print("Autotranslate done.")
