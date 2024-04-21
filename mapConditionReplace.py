import os

def replace_strings_in_files(folder_path, mod_path, replace_dict):
    for filename in os.listdir(folder_path):
        if filename.startswith("Map") and os.path.isfile(os.path.join(folder_path, filename)):
            with open(os.path.join(folder_path, filename), 'rb') as file:
                content = file.read()
            
            for key, value in replace_dict.items():
                newContent = content.replace(key, value)
            
            if newContent != content:
                with open(os.path.join(mod_path, filename), 'wb') as modified_file:
                    modified_file.write(newContent)

if __name__ == "__main__":
    folder_path = "Data"
    mod_path = "Mod/Mod_Data"
    replacements = {"\"ネイジュレンジ\"": "\"Neijurange\"",
                    "\"リジェオ\"": "\"Rigeo\"",
                    "\"フルビュア\"": "\"Fulbeua\"",
                    "\"ギルゴーン\"": "\"Gilgorn\"",
                    "\"ユーガノット\"": "\"Yuganot\"",
                    "\"シルフェ\"": "\"Silfe\"",
                    "\"ヴェルミィーナ\"": "\"Vermina\"",
                    "\"ラーミル\"": "\"Ramil\"",
                    "\"カオシア\"": "\"Chaosia\""}
    binary_replacements = {key.encode(): value.encode() for key, value in replacements.items()}
    replace_strings_in_files(folder_path, mod_path, binary_replacements)
