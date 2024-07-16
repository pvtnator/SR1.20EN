import os
import re
import time
import sys
from pathlib import Path

def extract_strings(folder_path, output_file, update={}, conv={}):
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
            stringconv = conv.get(string, string)
            outfile.write(f'{stringconv}\n')
            if len(contexts) > 30:
                outfile.write(f"> CONTEXT: global\n")
            else:
                for context in contexts:
                    outfile.write(f"> CONTEXT: {context}\n")

            if string.strip() in update["global"]:
                outfile.write(update["global"][string.strip()])
            else:
                for c in contexts:
                    if (c in update and string.strip() in update[c]):
                        outfile.write(update[c][string.strip()])
                        break
            #else:
            #    print(string)
            outfile.write("\n> END STRING\n\n")

def autotranslate(translations_file, lines, multiline=200):
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
            if lines[i].strip() == "" and re.search("[ぁ-んァ-ン]", string) and not "/" in string and \
                                    len(string.strip())>3 and ("\\\\H" in string or "\\n" in string or \
                                    (not "global" in contexts and not "System" in str(contexts))):
                batchi.append(i)
                string = string.replace("#{myname}", "私").replace("#{target}", "あなた")
                string = string.replace("#{$msg.t_target.name}", "あなた")
                string = string.replace("アソコ", "おまんこ").replace("ココ", "おまんこ")
                string = string.replace(r"\\H", r".\\H")
                string = string.replace("…", "...")
                string = re.sub("\.{2,}", "...", string)
                numbered = len(batchi)
                string = str(numbered)+". "+string.rstrip()+"\r\n"
                batcht += string
                if i > len(lines)-10 or len(batchi)>=multiline or len(batcht)>4800:
                    batcht = batcht.strip()
                    #print("\n"+batcht+"\n")
                    print(str(100*i/len(lines))+"%\n")
                    pyperclip.copy(batcht)
                    paste = []
                    while(pyperclip.paste() == batcht or len(paste) != len(batcht.split("\n"))):
                        time.sleep(0.2)
                        #print(len(paste))
                        #print(len(batcht.split("\n")))
                        if len(paste) != len(batcht.split("\n")) and len(paste) > 5 and pyperclip.paste() != batcht:
                            print("Switched to 10 lines")
                            return 10
                        pasted = pyperclip.paste()
                        if pasted!=batcht:
                            pasted = pasted.replace("\r\n\r\n", "\r\n")
                            pasted = re.sub(r'\r\n(?!\d)', r'\\n', pasted)
                            paste = re.findall("\d{1,2}\. ?(.*?(?=\d\.[A-Za-z ]|\n|$))", pasted)
                            #for p in range(len(paste)):
                            #    print(str(p+1)+". "+paste[p])
                    trlines = paste
                    multiline = 200
                    for j in range(len(trlines)):
                        translated = trlines[j].strip()
                        if len(translated) > 3:
                            #print(translated)
                            if translated[-1] == "." and translated[-2] != ".":
                                translated = translated[:-1]
                            translated = translated.replace("\\n", "\\n　")
                            translated = translated.replace(r"\n　\n　", r"\n　")
                            translated = translated.replace("　　", "　").replace("　 ", "　")
                            translated = translated.replace("…", "...")
                            translated = translated.replace("#", "").replace("{", "#{")
                            translated = translated.replace("\\ \\", "\\\\")
                            translated = translated.replace(" \\\\H", "\\\\H")
                            translated = translated.replace("\\\\　H", "\\\\H ")
                            translated = re.sub("([^\\\\])\\\\H", "\\1\\\\\\\\H", translated)
                            translated = translated.replace(".\\\\H", "\\\\H")
                            translated = re.sub("Giggle|Laughs{0,}|[Ll]ol", "*Giggle*", translated) 
                            translated = translated.replace("violent", "intense")
                            translated = re.sub("\\\\H　{0,}([a-zA-Z])", "\\\\H \\1", translated)
                            translated = re.sub("[Ss]{0,}[Ww]h{0,}oosh(?=[,\.\\\\])", "*woosh*", translated)
                            translated = re.sub("[Ll]ick(?=[,\.\\\\])", "*kiss*", translated)
                            translated = re.sub("[Kk]iss(?=[,\.\\\\])", "*kiss*", translated)
                            translated = re.sub("[Ss]mooch(?=[ ,\.\\\\])", "*smooch*", translated)
                            translated = re.sub("[Ss]lurp(?=[ ,\.\\\\])", "*slurp*", translated)
                            translated = re.sub(r"\* \*|\*, \*", ", ", translated)
                            translated = re.sub("\"(.*)\"", "「\\1」", translated)
                            translated = re.sub("\.{2,}", "...", translated)
                            translated = re.sub("([a-zA-Z])\\1{3,}", "\\1\\1", translated)
                            #translated = re.sub(r"([^\.])\.\\H", r"\1\\H", translated)
                            parts = translated.split("\\n")
                            brk = "" if "{speaker}" in translated or "{master}" in translated else "　"
                            translated = ""
                            pi = 0
                            while pi < len(parts):
                                p = parts[pi].replace("　", brk)
                                splitsymbols = [". ", "! ", "? ", ", ", " "]
                                for ss in splitsymbols:
                                    spot = 30 if ss==" " else 20
                                    if len(p) > 50 and p.find(ss, spot, spot+20) >= 0:
                                        parts[pi] = p[:p.find(ss, spot, spot+20)+1]
                                        parts.insert(pi+1, brk+p[p.find(ss, spot, spot+20)+len(ss):])
                                        #p = p[:p.find(ss, spot)+1]+brk+p[p.find(ss, spot)+len(ss):]
                                        break
                                translated += parts[pi] if translated=="" else "\\n"+parts[pi]
                                pi += 1
                            lines[batchi[j]] = translated+"\n"
                    batchi.clear()
                    batcht = ""
                    with open(translations_file, 'w', encoding='utf-8') as trans_file:
                        trans_file.writelines(lines)
            i += 2
        else:
            i += 1
    return 0

def patch_file(file, context, translations, regexes, glpattern, target_path):
    with file.open(encoding='utf-8', errors='surrogateescape') as f:
        content = f.read()
        try:
            if context in translations:
                pattern = re.compile("|".join(key for key in sorted(regexes[context], key=len, reverse=True)))
                content = pattern.sub(lambda match: translations[context][match.group(0)], content)
            if translations["global"]:
                content = glpattern.sub(lambda match: translations["global"][match.group(0)], content)
            with target_path.open(mode='w', encoding='utf-8', errors='surrogateescape') as outfile:
                outfile.write(content)
                #print(context)
        except Exception as e:
            print(e)

def apply_translations(folder_path, apply_path, regexes, translations, mustinclude=""):
    import concurrent.futures
    glpattern = re.compile("|".join(key for key in sorted(regexes["global"], key=len, reverse=True)))
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for file in folder_path.rglob("*"):
            relative = file.relative_to(folder_path)
            if "omake" in relative.as_posix():
                continue
            target_path = apply_path / relative
            if file.is_dir():
                print(target_path)
                target_path.mkdir(parents=True, exist_ok=True)
            elif mustinclude in relative.as_posix() and ".rb" in file.name:                
                futures.append(executor.submit(patch_file, file, relative.as_posix(), \
                                            translations, regexes, glpattern, target_path))
    while any(not future.done() for future in futures):
        time.sleep(1)
        print("Processing...")
                
if __name__ == "__main__":
    current_dir = Path.cwd()
    mode = sys.argv[1] if len(sys.argv)>1 else "extract"
    source = sys.argv[2] if len(sys.argv)>2 else "mod_scripts"
    dest = sys.argv[3] if len(sys.argv)>3 else "Mod_Talk"
    quickpatch = ""
    translated_dir = current_dir.parent / Path().resolve().name.replace("patch","translated")
    if mode=="apply":
        quickpatch = sys.argv[4] if len(sys.argv)>4 else ""
    else:
        translated_dir = Path(sys.argv[4]) if len(sys.argv)>4 else current_dir.parent / Path().resolve().name.replace("patch","translated")
    talk_dir = translated_dir / "System" / source
    modtalk_dir = translated_dir / "Mod" / dest
    translations_file = source+".txt"
    translations = {"global": {}}
    conv = {}
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
                    if mode == "extract":
                        if source == "mod_scripts" and "\"" in string:
                            conv[string.replace("\"", "")] = string
                            string = string.replace("\"", "")
                        translations["global"][string.strip()] = lines[i].rstrip()
                        continue
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
        extract_strings(talk_dir, translations_file, translations, conv)
        print("Extraction completed.")
    elif mode == "apply":       
        apply_translations(talk_dir, modtalk_dir, regexes, translations, quickpatch)
        print("Translations applied.")
    elif mode == "autotranslate":
        multiline = autotranslate(translations_file, lines)
        while multiline > 0:
            multiline = autotranslate(translations_file, lines, multiline)
        print("Autotranslate done.")
