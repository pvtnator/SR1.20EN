def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        begin_string_found = False
        context_found = False

        for line in infile:
            if begin_string_found and context_found:
                if line.startswith(">"):
                    outfile.write(line)
                else:
                    outfile.write(line.replace("\\\\q", "​q​"))
                    begin_string_found = False
            else:
                if line.strip() == "> BEGIN STRING":
                    begin_string_found = True
                    context_found = False
                if "> CONTEXT" in line:
                    context_found = True		
                outfile.write(line)

if __name__ == "__main__":
    input_file = "patch/Scripts.txt"  # Change to your input file name
    output_file = "patch/NewScripts.txt"  # Change to your output file name
    process_file(input_file, output_file)
