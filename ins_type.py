# ins_type.py

# Listas de instrucciones reales
r_list = ["add", "sub", "xor", "or", "and", "sll", "srl", "sra", "slt", "sltu"]
i_list = [["addi", "xori", "ori", "andi", "slli", "srli", "srai", "slti", "sltiu", "jalr"],
          ["lb", "lh", "lw", "lbu", "lhu"]]
s_list = ["sb", "sh", "sw"]
b_list = ["beq", "bne", "blt", "bge", "bltu", "bgeu"]
u_list = ["lui", "auipc"]
j_list = ["jal"]

# Lista de pseudo instrucciones
pseudo_list = ["li", "mv", "not", "neg", "nop", "j"]
