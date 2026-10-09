import tkinter as tk
from tkinter import simpledialog, ttk, filedialog
from assembler import assemble

# Registers
pc = 0
mar = 0
mdr = 0
ir = 0
acc = 0

# Settings

ram = 1024

memory = [None] * ram

program = [None] * ram

instruction_set = ["ADD", "SUB", "STA", "LDA", "BRA", "OUT", "HLT", "INP", "BRZ", "BRP"]

def load_file():
    path =  filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not path:
        return
    with open(path) as f:
        editor.delete("1.0", "end")
        editor.insert("1.0", f.read())

def save_file():
    assembled, counter = assemble(editor.get("1.0", "end"))
    path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if not path:
        return
    with open(path, "w") as f:
        for address in range(counter):
            f.write(str(assembled[address]) + "\n")

def fde():
    global pc, mar, mdr, ir, acc

    # Fetch

    mar = pc
    mdr = memory[pc]
    ir = mdr

    pc +=1

    # Decode

    if ir is None:
        write_output(f"ERROR: attempted to read empty memory address {mar}")
        return False

    operand = None

    ins = str(ir)[:3]
    #print(f"INS: {ins}")

    if ins not in instruction_set and not ins.isdigit():
        write_output(f"ERROR: '{ir}' at address {mar} is not a recognised instruction")
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
                mem_list.delete(operand)
                mem_list.insert(operand, mem_row(operand))

            if ins == "LDA":
                acc = int(memory[operand])

            if ins == "BRA":
                pc = operand

            if ins == "OUT":
                write_output(str(acc))

            if ins == "HLT":
                return False

            if ins == "INP":
                value = simpledialog.askinteger("Input", "INPUT: ")
                if value is None:
                    write_output("Stopped: No input given")
                    return False
                acc = value

            if ins == "BRZ":
                if acc == 0:
                    pc = operand

            if ins == "BRP":
                if acc >= 0:
                    pc = operand

        except:
            write_output(f"ERROR: Address {operand} does not contain a number")
            return False

        return True

root = tk.Tk()
root.title("LMC Emulator")
root.geometry('700x500')

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

asm_tab = tk.Frame(notebook)
cpu_tab = tk.Frame(notebook)
notebook.add(asm_tab, text="Assembler")
notebook.add(cpu_tab, text="CPU")

def update_registers():
    pc_label.config(text=f"PC: {pc}")
    mar_label.config(text=f"MAR: {mar}")
    mdr_label.config(text=f"MDR: {mdr}")
    ir_label.config(text=f"IR: {ir}")
    acc_label.config(text=f"ACC: {acc}")
    mem_list.selection_clear(0, "end")
    if pc < ram:
        mem_list.selection_set(pc)
        mem_list.see(pc)

def step():
    running = fde()
    update_registers()
    if not running:
        step_button.config(state="disabled")
        run_button.config(state="disabled")
    return running

def run():
    step_button.config(state="disabled")
    run_button.config(state="disabled")
    run_loop()

def reset():
    global memory, pc, mar, mdr, ir, acc
    memory = program.copy()
    pc = mar = mdr = ir = acc = 0
    mem_list.delete(0, "end")
    for address in range(ram):
        mem_list.insert("end", mem_row(address))
    update_registers()
    output_box.config(state="normal")
    output_box.delete("1.0", "end")
    output_box.config(state="disabled")
    step_button.config(state="normal")
    run_button.config(state="normal")

# Frames

reg_frame = tk.LabelFrame(cpu_tab, text="Registers", padx=8, pady=8)
reg_frame.grid(row=0, column=0, sticky="n", padx=8, pady=8)

out_frame = tk.LabelFrame(cpu_tab, text="Output", padx=8, pady=8)
out_frame.grid(row=0, column=2, sticky="nsew", padx=8, pady=8)

controls = tk.Frame(cpu_tab)
controls.grid(row=1, column=0, columnspan=3, sticky="w", padx=8, pady=(0,8))

# Registers

pc_label = tk.Label(reg_frame, text="PC: 0", width=14, anchor="w", font="TkFixedFont")
pc_label.grid(row=0, column=0, sticky="w")

mar_label = tk.Label(reg_frame, text="MAR: 0", width=14, anchor="w", font="TkFixedFont")
mar_label.grid(row=1, column=0, sticky="w")

mdr_label = tk.Label(reg_frame, text="MDR: 0", width=14, anchor="w", font="TkFixedFont")
mdr_label.grid(row=2, column=0, sticky="w")

ir_label = tk.Label(reg_frame, text="IR: 0", width=14, anchor="w", font="TkFixedFont")
ir_label.grid(row=3, column=0, sticky="w")
 
acc_label = tk.Label(reg_frame, text="ACC: 0", width=14, anchor="w", font="TkFixedFont")
acc_label.grid(row=4, column=0, sticky="w")

step_button = tk.Button(controls, text="Step", command=step, state="disabled")
step_button.grid(row=5, column=0)

run_button = tk.Button(controls, text="Run", command=run, state="disabled")
run_button.grid(row=5, column=1)

reset_button = tk.Button(controls, text="Reset", command=reset)
reset_button.grid(row=5, column=2)

output_box = tk.Text(out_frame, width=20, height=10, state="disabled")
output_box.pack(fill="both", expand=True)

cpu_tab.columnconfigure(2, weight=1)
cpu_tab.rowconfigure(0, weight=1)

# memory viewer

mem_frame = tk.LabelFrame(cpu_tab, text="Memory", padx=8, pady=8)
mem_frame.grid(row=0, column=1, sticky="ns", padx=8, pady=8)

mem_list = tk.Listbox(mem_frame, width=16, font="TkFixedFont", exportselection=False)
mem_scroll = tk.Scrollbar(mem_frame, command=mem_list.yview)
mem_list.config(yscrollcommand=mem_scroll.set)
mem_list.pack(side="left", fill="both", expand=True)
mem_scroll.pack(side="right", fill="y")

def mem_row(address):
    value = memory[address]
    if value is None:
        value = "---"
    return f"{address:04}  {value}"

def write_output(text):
    output_box.config(state="normal")
    output_box.insert("end", text + "\n")
    output_box.see("end")
    output_box.config(state="disabled")

def push_to_memory():
    global program
    program, counter = assemble(editor.get("1.0", "end"))
    reset()
    notebook.select(cpu_tab)

def run_loop():
    if step():
        root.after(100, run_loop)

# Assembler

editor = tk.Text(asm_tab, width=40, height=14)
editor.grid(row=0, column=0)

push_button = tk.Button(asm_tab, text="Push to memory", command=push_to_memory)
push_button.grid(row=1, column=0, sticky="e")

load_button = tk.Button(asm_tab, text="Load from file", command=load_file)
load_button.grid(row=1, column=0, sticky="w")

save_button = tk.Button(asm_tab, text="Save to file", command=save_file)
save_button.grid(row=2, column=0, sticky="w")

root.mainloop()