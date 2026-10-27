import os

def is_number(text):
    try:
        int(text)
        return True
    except ValueError:
        return False
    
def strip_comment(line):
    for marker in ("//", ";"):
        if marker in line:
            line = line.split(marker, 1)[0]

def assemble(source):

    labels = {}
    counter = 0
    ram = 1024
    memory = [None] * ram

    instruction_set = ["ADD", "SUB", "STA", "LDA", "BRA", "OUT", "HLT", "INP", "BRP", "BRZ"]

    for line in source.splitlines():
        # Strip out any invalid instructions while keeping data
        word = strip_comment(line).split()
        if not word:
            continue
        if word[0] not in instruction_set and not is_number(word[0]):
            labels[word[0]] = counter
            word.pop(0)
            if not word:
                continue
        memory[counter] = " ".join(word)
        counter += 1

    for address in range(counter):
        words = memory[address].split()
        if len(words) > 1:
            operand = words[1]
            if operand in labels:
                memory[address] = words[0] + " " + str(labels[operand])
            else:
                try:
                    int(operand)
                except ValueError:
                    raise ValueError(f"Unknown label '{operand}' at address {address}")

    return memory, counter

if __name__ == "__main__":
    with open("program.txt") as f:
        memory, counter = assemble(f.read())
    print(memory[:counter])