def get_replacement(text):
    rep = {"レッサーサキュバス": "Lesser Succubus",
           "サキュバスロード": "Succubus Lord",
       "インプ": "Imp",
       "プチウィッチ": "Petite Witch",
       "ナイトメア": "Nightmare",
       "ウィッチ": "Witch",
       "ファミリア": "Familiar",
       "ワーウルフ": "Werewolf",
       "キャスト": "Cast",
       "サキュバス": "Succubus",
       "プリーステス": "Priestess",
       "ゴブリン": "Goblin",
       "ギャングコマンダー": "Gang Commander",
       "デビル": "Devil",
       "アルラウネ": "Alraune",
       "マタンゴ": "Matango",
       "スライム": "Slime",
       "リリム": "Lilim",
       "ダークエンジェル": "Dark Angel",
       "デーモン": "Demon",
       "ガーゴイル": "Gargoyle",
       "ミミック": "Mimic",
       "ワーキャット": "Werecat",
       "スレイヴ": "Slave",
       "タマモ": "Tamamo",
        "カースメイガス": "Curse Magus"}
    
    for key in rep.keys():
        text = text.replace(key, rep[key])
    return text

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        begin_string_found = False
        pending_line = None
        context_found = False
        linecount = 0

        for line in infile:
            if pending_line:
                if not context_found or line.startswith(">"):
                    outfile.write(line)
                    if line.startswith(">"):
                        context_found = True
                    else:
                        linecount += 1
                elif context_found:
                    newtext = get_replacement(pending_line)
                    outfile.write(newtext if newtext!=pending_line else line if linecount > 0 else "\n")

                    pending_line = None
                    begin_string_found = False
                    context_found = False
                    linecount = 0
            else:
                if line.strip() == "> BEGIN STRING":
                    begin_string_found = True
                outfile.write(line)

                if line.strip() and begin_string_found and not line.startswith(">"):
                    pending_line = line

if __name__ == "__main__":
    input_file = "troops.txt"  # Change to your input file name
    output_file = "newtroops.txt"  # Change to your output file name
    process_file(input_file, output_file)
