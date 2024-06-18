import os
import re
import time
import sys
from pathlib import Path

def extract_strings(folder_path, output_file, update={}):
    strings = {}

    # Walk through all files in the folder and its subfolders
    for file in folder_path.rglob("*.rb"):
        relative = file.relative_to(folder_path)
        context = relative.as_posix()
        with file.open(encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Find all strings in the file
        found_strings = re.findall(r'"「{0,}(.*?)」{0,}"', content)
        found_strings += re.findall(r'\/.*?\/', content)
        
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
            if len(contexts) > 30:
                outfile.write(f"> CONTEXT: global\n")
            else:
                for context in contexts:
                    outfile.write(f"> CONTEXT: {context}\n")

            if string in update["global"]:
                outfile.write(update["global"][string])
            else:
                for c in contexts:
                    if (c in update and string in update[c]):
                        outfile.write(update[c][string])
                        break
            #else:
            #    print(string)
            outfile.write("\n> END STRING\n\n")

def autotranslate(translations_file, lines, multiline=20):
    import pyperclip
    i = 930845
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
            if lines[i].strip() == "" and len(string.strip())>3 and ("\\\\H" in string or "\\n" in string or \
                                           (not "global" in contexts and not "System" in str(contexts))):
                batchi.append(i)
                string = string.replace("#{myname}", "私").replace("#{target}", "あなた").replace("#{master}", "あなた")
                string = string.replace("#{$msg.t_target.name}", "あなた")
                string = string.replace("アソコ", "おまんこ").replace("ココ", "おまんこ")
                string = string.replace(r"\\H", r".\\H")
                numbered = len(batchi)
                string = str(numbered)+". "+string.rstrip()+"\r\n"
                batcht += string
                if i > len(lines)-10 or len(batchi)>=multiline:
                    batcht = batcht.strip()
                    #print("\n"+batcht+"\n")
                    print(str(100*i/len(lines))+"%\n")
                    pyperclip.copy(batcht)
                    paste = []
                    while(pyperclip.paste() == batcht or len(paste) != len(batcht.split("\n"))):
                        time.sleep(0.2)
                        #print(len(paste))
                        #print(len(batcht.split("\n")))
                        if len(paste) != len(batcht.split("\n")) and len(paste) > max(multiline-15,5) and pyperclip.paste() != batcht:
                            print("Switched to 2 lines")
                            return 2
                        pasted = pyperclip.paste()
                        if pasted!=batcht:
                            pasted = re.sub(r'\r\n(?!\d)', r'\\n', pasted)
                            paste = pasted.split("\n")
                            print(paste)
                    return 0
                    trlines = paste
                    multiline = 20
                    for j in range(len(trlines)):
                        translated = trlines[j].strip()
                        if len(translated) > 3:
                            #print(translated)
                            if translated[-1] == "." and translated[-2] != ".":
                                translated = translated[:-1]
                            translated = translated.replace("\\n", "\\n　")
                            translated = translated.replace("　　", "　").replace("　 ", "　")
                            translated = translated.replace("…", "...")
                            translated = translated.replace("#", "").replace("{", "#{")
                            translated = translated.replace("\\ \\", "\\\\")
                            translated = translated.replace(" \\\\H", "\\\\H")
                            translated = re.sub("([^\\\\])\\\\H", "\\1\\\\\\\\H", translated)
                            translated = translated.replace(".\\\\H", "\\\\H")
                            translated = translated.replace("Giggle", "*Giggle*")
                            translated = re.sub("\"(.*)\"", "「\\1」", translated)
                            translated = re.sub("\.{2,}", "...", translated)
                            translated = re.sub("([a-zA-Z])\\1{3,}", "\\1\\1", translated)
                            #translated = re.sub(r"([^\.])\.\\H", r"\1\\H", translated)
                            parts = translated.split("\\n")
                            translated = ""
                            for p in parts:
                                if len(p) > 60 and p.find(",", 30) >= 0:
                                    p = p[:p.find(",", 30)+1]+"\\n　"+p[p.find(",", 30)+2:]
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
    return 0

def apply_translations(folder_path, apply_path, regexes, translations, mustinclude=""):
    glpattern = re.compile("|".join(key for key in sorted(regexes["global"], key=len, reverse=True)))
    for file in folder_path.rglob("*"):
        relative = file.relative_to(folder_path)
        if "omake" in relative.as_posix():
            continue
        target_path = apply_path / relative
        if file.is_dir():
            print(target_path)
            target_path.mkdir(parents=True, exist_ok=True)
        elif mustinclude in relative.as_posix() and ".rb" in file.name:
            #file_path = Path.join(root, file)
            with file.open(encoding='utf-8', errors='surrogateescape') as f:
                content = f.read()

            context = relative.as_posix()
            if context in translations:
                pattern = re.compile("|".join(key for key in sorted(regexes[context], key=len, reverse=True)))
                content = pattern.sub(lambda match: translations[context][match.group(0)], content)
            if translations["global"]:
                content = glpattern.sub(lambda match: translations["global"][match.group(0)], content)
            with target_path.open(mode='w', encoding='utf-8', errors='surrogateescape') as outfile:
                outfile.write(content)

if __name__ == "__main__":
    current_dir = Path.cwd()
    mode = sys.argv[1] if len(sys.argv)>1 else "autotranslate"
    source = sys.argv[2] if len(sys.argv)>2 else "talk"
    dest = sys.argv[3] if len(sys.argv)>3 else "Mod_Talk"
    translated_dir = Path(sys.argv[4]) if len(sys.argv)>4 else current_dir.parent / Path().resolve().name.replace("patch","translated")
    talk_dir = translated_dir / "System" / source
    modtalk_dir = translated_dir / "Mod" / dest
    translations_file = source+".txt"
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
            string = lines[i].rstrip()
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
                    if source == "mod_scripts" and mode=="apply" and string[0]!='/' \
                                                and not '"' in string:
                        regexes[c].append(re.escape('"'+string+'"'))
                        translations[c]['"'+string+'"'] = '"'+lines[i].rstrip()+'"'
                        regexes[c].append(re.escape("'"+string+"'"))
                        translations[c]["'"+string+"'"] = "'"+lines[i].rstrip()+"'"
                    else:
                        regexes[c].append(re.escape(string))
                        translations[c][string] = lines[i].rstrip()
                    #print(string)
                    #print(r'"「{0,}('+re.escape(string)+r')」{0,}"')
            i += 2
        else:
            i += 1

    #print(translations["global"])
    print("Mode: "+mode+"\nThis might take a minute")
    if mode == "extract":
        extract_strings(talk_dir, translations_file, translations)
        print("Extraction completed.")
    elif mode == "apply":       
        apply_translations(talk_dir, modtalk_dir, regexes, translations)
        print("Translations applied.")
    elif mode == "autotranslate":
        multiline = autotranslate(translations_file, lines)
        while multiline > 0:
            multiline = autotranslate(translations_file, lines, multiline)
        print("Autotranslate done.")
