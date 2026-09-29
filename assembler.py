import os

labels = {}
counter = 0
ram = 1024
memory = [None] * ram

instruction_set = ["ADD", "SUB", "STA", "LDA", "BRA", "OUT", "HLT", "INP", "BRZ"]

file = input("File: ")

with open(file) as f:
    for line in f:
        # Strip out any invalid instructions while keeping data
        word = line.split()
        if word[0] not in instruction_set and not word[0].isdigit():
            labels[word[0]] = counter
            word.pop(0)
        memory[counter] = " ".join(word)
        counter += 1

for address in range(counter):
    words = memory[address].split()
    if len(words) > 1 and words[1] in labels:
        memory[address] = words[0] + " " + str(labels[words[1]])

originalfilename = os.path.splitext(f.name)[0]
filename = originalfilename + "_assembled.txt"
with open(filename, "w") as f:
    for address in range(counter):
        f.write(memory[address] + "\n")