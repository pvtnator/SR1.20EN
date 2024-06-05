rep = {}

def get_replacement(text, allkeys=False):
    parts = text.strip().split("/")
    #if len(parts)>0 and parts[0] in rep:
    #    text = text.replace(parts[0], rep[parts[0]])
    if allkeys:
        for key in sorted(rep, key=len, reverse=True):
            text = text.replace(key, rep[key])
    else:
        for p in parts:
            if p in rep:
                text = text.replace(p, rep[p], 1)
    return text

def process_file(input_file):
    lines = []
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    with open(input_file, 'w', encoding='utf-8') as outfile:
        begin_string_found = False
        pending_line = None
        context_found = False
        linecount = 0

        i = 0
        while i < len(lines):
            line = lines[i]
            if pending_line:
                if not context_found or line.startswith(">"):
                    outfile.write(line)
                    if line.startswith(">"):
                        context_found = True
                    else:
                        linecount += 1
                elif context_found:
                    newtext = get_replacement(pending_line, "Troops" in input_file or "Enemies" in input_file)
                    outfile.write(newtext if newtext!=pending_line and linecount==1 else line if line or linecount>0 else "\n")
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
                    linecount = 1
            i += 1

if __name__ == "__main__":
    lines = []
    with open("patch/Classes.txt", 'r', encoding='utf-8') as trans_file:
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
            parts = string.strip().split("/")
            if lines[i].strip() and len(parts)>1:
                tparts = lines[i].strip().split("/")
                if len(parts) == len(tparts):
                    for k in range(len(parts)):
                        if not parts[k] in rep:
                            rep[parts[k]] = tparts[k]
                            #print(parts[k]+" = "+tparts[k])
                #print(string.strip()+" = "+lines[i].strip())

            i += 2
        else:
            i += 1

    
    process_file("patch/Enemies.txt")
    process_file("patch/Classes.txt")
    process_file("patch/Troops.txt")
