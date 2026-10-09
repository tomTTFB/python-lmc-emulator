import os

def assemble(source):

    labels = {}
    counter = 0
    ram = 1024
    memory = [None] * ram

    instruction_set = ["ADD", "SUB", "STA", "LDA", "BRA", "OUT", "HLT", "INP", "BRP", "BRZ"]

    for line in source.splitlines():
        # Strip out any invalid instructions while keeping data
        word = line.split()
        if not word:
            continue
        if word[0] not in instruction_set and not word[0].isdigit():
            labels[word[0]] = counter
            word.pop(0)
        memory[counter] = " ".join(word)
        counter += 1

    for address in range(counter):
        words = memory[address].split()
        if len(words) > 1 and words[1] in labels:
            memory[address] = words[0] + " " + str(labels[words[1]])

    return memory, counter

if __name__ == "__main__":
    with open("program.txt") as f:
        memory, counter = assemble(f.read())
    print(memory[:counter])