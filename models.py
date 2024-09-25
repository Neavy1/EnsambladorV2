#Clase para guardar labels
class Label:
    
    def __init__(self, mem, name):
        self.name = name
        self.mem = mem
        self.instructions = []

#Clases para cada instrucción
class InstructionR:
    ins_0 = {
        "add": (0x0, 0x00), "sub": (0x0, 0x20), "xor": (0x4, 0x00), 
        "or": (0x6, 0x00), "and": (0x7, 0x00), "sll": (0x1, 0x00),
        "srl": (0x5, 0x00), "sra": (0x5, 0x20), "slt": (0x2, 0x00), 
        "sltu": (0x3, 0x00)
    }

    def __init__(self, name, rd, rs1, rs2, mem):
        self.name = name
        if self.name in self.ins_0:
            self.opcode = 0b0110011
            funcs = self.ins_0[self.name]
        self.func3 = bin(funcs[0])
        self.func7 = bin(funcs[1])
        self.rd = bin(rd)
        self.rs1 = bin(rs1)
        self.rs2 = bin(rs2)
        self.mem = hex(mem)

class InstructionI:
    ins_0 = {
        "addi": 0x0, "xori": 0x4, "ori": 0x6, "andi": 0x7,
        "slli": (0x1, 0x00), "srli": (0x5, 0x00), "srai": (0x5, 0x20),
        "slti": 0x2, "sltiu": 0x3
    }
    ins_1 = {
        "lb": 0x0, "lh": 0x1, "lw": 0x2, "lbu": 0x4, "lhu": 0x5
    }
    ins_2 = {
        "jalr": 0x0
    }

    def __init__(self, name, rd, rs1, imm, mem):
        self.name = name
        if self.name in self.ins_0:
            self.opcode = 0b0010011
            funcs = self.ins_0[self.name]
        elif self.name in self.ins_1:
            self.opcode = 0b0000011
            funcs = self.ins_1[self.name]
        elif self.name in self.ins_2:
            funcs = self.ins_2[self.name]
            self.opcode = 0b1100111
        if self.name != "slli" and self.name != "srli" and self.name != "srai":
            self.func3 = bin(funcs)
        else:
            self.func3 = bin(funcs[0])
            self.func7 = bin(funcs[1])
        self.rd = bin(rd)
        self.rs1 = bin(rs1)
        self.imm = bin(imm)
        self.mem = hex(mem)

class InstructionS:
    ins_0 = {
        "sb": 0x0, "sh": 0x1, "sw": 0x2
    }

    def __init__(self, name, rs1, rs2, imm, mem):
        self.name = name
        if self.name in self.ins_0:
            self.opcode = 0b0100011
            self.func3 = self.ins_0[self.name]
        self.rs1 = bin(rs1)
        self.rs2 = bin(rs2)
        self.imm = bin(imm)
        self.mem = hex(mem)

class InstructionB:
    ins_0 = {
        "beq": 0x0, "bne": 0x1, "blt": 0x4, "bge": 0x5,
        "bltu": 0x6, "bgeu": 0x7
    }

    def __init__(self, name, rs1, rs2, imm, mem):
        self.name = name
        if self.name in self.ins_0:
            self.opcode = 0b1100011
            self.func3 = self.ins_0[self.name]
        self.rs1 = bin(rs1)
        self.rs2 = bin(rs2)
        self.imm = imm
        self.mem = hex(mem)

class InstructionU:
    
    def __init__(self, name, rd, imm, mem):
        self.name = name
        if name == "lui":
            self.opcode = 0b0110111
        elif name == "auipc":
            self.opcode = 0b0010111
        self.rd = bin(rd)
        self.imm = bin(imm)
        self.mem = hex(mem)

class InstructionJ:
    
    def __init__(self, name, rd, imm, mem):
        self.name = name
        self.opcode = 0b1101111
        self.rd = bin(rd)
        self.imm = bin(imm)
        self.mem = hex(mem)

Labels = []
Program = []