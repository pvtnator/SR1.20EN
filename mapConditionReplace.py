import os
import re

def replace_strings_in_files(folder_path, mod_path, replace_dict):
    for filename in os.listdir(folder_path):
        if (filename.startswith("Map") or filename.startswith("Common")) and os.path.isfile(os.path.join(folder_path, filename)):
            with open(os.path.join(folder_path, filename), 'rb') as file:
                content = file.read()

            utf8_parts = re.findall(rb'\(\".{3,30}\"\)', content)
            utf8_parts += re.findall(rb'== \".{3,30}\"', content)
            replaced = False

            savedspot = -1
            saveddiff = 0

            for part in utf8_parts:
                replacement = replace_dict.get(part)
                if replacement:
                    diff = len(part)-len(replace_dict[part])
                    #replacement += " ".encode('utf-8')*diff
                    print(filename+replacement.decode())
                    replaced = True
                    lensymbol = content.rfind(rb"$", 0, content.find(part))-1
                    lensymbol = max(content.rfind(rb"@", 0, content.find(part))-1, lensymbol)
                    ifspot = content.rfind(rb"if", lensymbol-4, lensymbol)-1
                    elseifspot = content.rfind(rb"elseif", lensymbol-8, lensymbol)-1
                    notspot = content.rfind(rb"not", lensymbol-5, lensymbol)-1
                    if ifspot > 0:
                        lensymbol = ifspot
                        print("ifspot")
                    if elseifspot > 0:
                        lensymbol = elseifspot
                        print("elseifspot")
                    if notspot > 0:
                        lensymbol = notspot
                        print("notspot")
                    if ifspot < 0 and savedspot >= 0:
                        lensymbol = savedspot
                        savedspot = -1
                    elif ifspot < 0 and notspot < 0 and content.find(rb"$", lensymbol+2) < content.find(rb";", lensymbol+2):
                        savedspot = lensymbol
                        saveddiff = diff
                        print(lensymbol)
                        content = content.replace(part, replacement, 1)
                        continue
                    newbyte = bytes(chr(content[lensymbol]-(diff+saveddiff)),'utf-8')
                    content = content[:lensymbol]+newbyte+content[lensymbol+1:]
                    content = content.replace(part, replacement, 1)
                    saveddiff = 0
            #utf8_parts = re.findall(rb'.\$game_actors\[101\]\.have_ability\?\("[^;]*"\).*?;', content)
            #utf8_parts += re.findall(rb'.\$game_variables\[\d\] {0,}== {0,}"[^;]*".*?;', content)
            #for part in utf8_parts:
            #    replacement = part[1:]
            #    replacement = bytes(chr(len(part)+3),'utf-8')+replacement
            #    content = content.replace(part, replacement)

            newContent = content.replace("ギルゴーン".encode(), "Gilgorn".encode())
            newContent = newContent.replace("ロウラット".encode(), "Lauratt".encode())
            if newContent != content:
                content = newContent
                replaced = True
                print("special case: "+filename)
                
            if replaced:
                with open(os.path.join(mod_path, filename), 'wb') as modified_file:
                    modified_file.write(content)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    folder_name = current_dir.split("\\")[-1].replace("_patch", "_translated")
    folder_path = os.path.join(parent_dir, folder_name+"\\Data")
    mod_path = os.path.join(parent_dir, folder_name+"\\Mod\\Mod_Data")
    #mod_path = folder_path
    
    replacements = {}

    lines = []
    with open("mod_scripts.txt", 'r', encoding='utf-8') as trans_file:
        lines = trans_file.readlines()
    i = 0
    while i < len(lines):
        if lines[i].strip() == "> BEGIN STRING":
            i += 1
            string = lines[i].strip()
            i += 1
            while(lines[i][0] == ">"):
                i += 1
            if lines[i].strip():
                rep = "(\""+lines[i].strip()+"\")"
                replacements["(\""+string+"\")"] = rep
                rep = "== \""+lines[i].strip()+"\""
                replacements["== \""+string+"\""] = rep
            i += 2
        else:
            i += 1

    
    binary_replacements = {}
    for key in replacements.keys():
        binary_replacements[key.encode('utf-8')] = replacements[key].encode('utf-8')
    replace_strings_in_files(folder_path, mod_path, binary_replacements)
