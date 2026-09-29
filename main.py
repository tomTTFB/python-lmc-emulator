import tkinter as tk

# Registers
pc = 0
mar = 0
mdr = 0
ir = 0
acc = 0

# Settings

ram = 1024

memory = [None] * ram

instruction_set = ["ADD", "SUB", "STA", "LDA", "BRA", "OUT", "HLT", "INP", "BRZ", "BRP"]

# Program Code Loader

counter = 0
with open("program_assembled.txt") as f:
  for line in f:
    line = line.strip('\n')
    memory[counter] = line
    counter += 1

def fde():
    global pc, mar, mdr, ir, acc

    # Fetch

    mar = pc
    mdr = memory[pc]
    ir = mdr

    pc +=1

    # Decode

    if ir is None:
        print("ERROR: attempted to read empty memory address " + mar)
        return False

    operand = None

    ins = str(ir)[:3]
    #print(f"INS: {ins}")

    if ins not in instruction_set:
        print(f"ERROR: '{ir}' at address {mar} is not a recognised instruction")
        return False

    if len(ir) > 3:
        operand = int(ir[4:])

    #print(f"OP: {operand}")

    if ins in instruction_set:

        # Execute
        try:
            if ins == "ADD":
                acc = acc + int(memory[operand])

            if ins == "SUB":
                acc = acc - int(memory[operand])

            if ins == "STA":
                memory[operand] = acc

            if ins == "LDA":
                acc = int(memory[operand])

            if ins == "BRA":
                pc = operand

            if ins == "OUT":
                print("OUTPUT: " + str(acc))

            if ins == "HLT":
                return False

            if ins == "INP":
                acc = int(input("INPUT: "))

            if ins == "BRZ":
                if acc == 0:
                    pc = operand

            if ins == "BRP":
                if acc >= 0:
                    pc = operand

        except:
            print(f"ERROR: Address {operand} does not contain a number")
            return False

        return True    

while fde():
    pass