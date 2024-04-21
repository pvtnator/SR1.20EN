import os
import re

def replace_strings_in_files(folder_path, mod_path, replace_dict):
    for filename in os.listdir(folder_path):
        if filename.startswith("Map") and os.path.isfile(os.path.join(folder_path, filename)):
            with open(os.path.join(folder_path, filename), 'rb') as file:
                content = file.read()

            utf8_parts = re.findall(rb'\(\".{3,20}\"\)', content)
            replaced = False

            for part in utf8_parts:
                replacement = replace_dict.get(part)
                if replacement:
                    diff = len(part)-len(replace_dict[part])
                    replacement += " ".encode('utf-8')*diff
                    print(replacement.decode('utf-8'))
                    replaced = True
                    content = content.replace(part, replacement)
                
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
    
    replacements = {"(\"ネイジュレンジ\")": "(\"Neijurange\")",
                    "(\"リジェオ\")": "(\"Rigeo\")",
                    "(\"フルビュア\")": "(\"Fulbeua\")",
                    "(\"ギルゴーン\")": "(\"Gilgorn\")",
                    "(\"ユーガノット\")": "(\"Yuganot\")",
                    "(\"シルフェ\")": "(\"Silfe\")",
                    "(\"ヴェルミィーナ\")": "(\"Vermina\")",
                    "(\"ラーミル\")": "(\"Ramil\")",
                    "(\"カオシア\")": "(\"Chaosia\")"}
    binary_replacements = {}
    for key in replacements.keys():
        binary_replacements[key.encode('utf-8')] = replacements[key].encode('utf-8')
    replace_strings_in_files(folder_path, mod_path, binary_replacements)
