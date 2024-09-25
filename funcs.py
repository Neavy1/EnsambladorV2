def rd_loader(rd):
    while len(rd) != 5 and len(rd) < 6:
        rd = "0" + rd
    rd_bits = list(rd)
    return rd_bits

def rs1_loader(rs1):
    while len(rs1) != 5 and len(rs1) < 6:
        rs1 = "0" + rs1
    rs1_bits = list(rs1)
    return rs1_bits

def rs2_loader(rs2):
    while len(rs2) != 5 and len(rs2) < 6:
        rs2 = "0" + rs2
    rs2_bits = list(rs2)
    return rs2_bits

def func3_loader(func3):
    while len(func3) != 3 and len(func3) < 4:
        func3 = "0" + func3
    func3_bits = list(func3)
    return func3_bits

def func7_loader(func7):
    while len(func7) != 7 and len(func7) < 8:
        func7 = "0" + func7
    func7_bits = list(func7)
    return func7_bits

def imm_loader(imm, bitlen):
    if imm.startswith("-"):
        imm = imm[3:]
        while len(imm) != bitlen and len(imm) < bitlen+1:
            imm = "0" + imm
        imm = ''.join('1' if bit == '0' else '0' for bit in imm)
        imm = bin(int(imm,2)+1)[2:]
        bin_0 = "1"
    else:
        imm = imm[2:]
        while len(imm) != bitlen and len(imm) < bitlen+1:
            imm = "0" + imm
        bin_0 = "0"
    imm_bits = list(imm)
    return imm_bits, bin_0

def opcode_loader(opcode):
    while len(opcode) != 7 and len(opcode) < 8:
        opcode = "0" + opcode  
    opcode_bits = list(opcode)
    return opcode_bits

def formater(bin_ins, object):
    instruction_hex = hex(int("".join(bin_ins), 2))[2:]
    while len(instruction_hex) < 8:
        instruction_hex = "0"+instruction_hex
    instruction_bin = bin(int("".join(bin_ins), 2))[2:]
    while len(instruction_bin) < 32:
        instruction_bin = "0"+instruction_bin
    fillMem = ''
    if len(object.mem[2:]) <= 5:
        iters = 5 - len(object.mem[2:])
        for i in range(iters):
            fillMem = "0" + fillMem
    finalMem = fillMem+object.mem
    intMem = int(object.mem,16)
    return instruction_hex, instruction_bin, finalMem, intMem

def rectificate():
    return open("binary_out.txt", "w"), open("binary_out.hex", "w")

def writingFiles(file, core, instruction, hex, intMem):
    file.write(instruction)
    if (intMem%16 == 0) and (intMem != 0):
        core.write("\n")
    hex_chain = f"{hex[0]}{hex[1]} {hex[2]}{hex[3]} {hex[4]}{hex[5]} {hex[6]}{hex[7]} "
    core.write(hex_chain)

def fuller(memory, file, core, total_memory=1500):
    hex_line = "00 00 00 00 "
    bin_line = "00000000000000000000000000000000\n"
    while memory < total_memory:
        if memory % 16 == 0 and memory != 0:
            core.write("\n")
            file.write("\n")
        core.write(hex_line)
        file.write(bin_line)
        memory += 4
