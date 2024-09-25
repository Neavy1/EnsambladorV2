import re
from regs import regs
from models import Labels, Program, InstructionB, InstructionI, InstructionJ, InstructionR, InstructionS, InstructionU, Label
from ins_type import r_list, i_list, j_list, s_list, u_list, b_list

def pseudo_translate(assembler_code):
    label_patt = r'(\s*)(\D+\w*)(\:)'
    mv_patt = r'(\s*)([m][v])(\s+)(.+)($)'
    call_patt = r'(\s*)([c][a][l][l])(\s+)(.+)($)'
    jr_patt = r'(\s*)([j][r])(\s+)(.+)($)'
    ret_patt = r'(\s*)([r][e][t])(\s*)($)'
    ins_patt = r'(\s*)([a-z]+)(\s+)(.+)(\n|$)'
    #Variable de memoria
    memory = 0
    #Codigo en assembler recibido desde la consola
    with open(assembler_code, 'r') as f:
        for line in f:
            if re.match(label_patt, line):
                l = re.match(label_patt, line)
                new = Label(memory, l.group(2))
                Labels.append(new)
                Program.append((line,memory))
            elif re.match(mv_patt, line):
                mv_ins = re.match(mv_patt, line)
                det = mv_ins.group(4)
                regs_patt = r'(\w+)(\s*)(\,)(\s*)(\w+)(\s*)($)'
                regs_obt = re.match(regs_patt, det)
                new_ins = f"addi {regs_obt.group(1)},{regs_obt.group(5)},0\n"
                for i in range(32):
                    if regs_obt.group(1) in regs[i]:
                        pos_rd = i
                        break
                for j in range(32):
                    if regs_obt.group(5) in regs[j]:
                        pos_rs1 = j
                        break
                ins_i = InstructionI("addi", pos_rd, pos_rs1, 0, memory)
                if len(Labels) > 0:
                    Labels[len(Labels)-1].instructions.append(ins_i)
                    Program.append((new_ins, memory))
                    memory += 4
                else:
                    print("No existe un label para agregar instrucciones")
            elif re.match(call_patt, line):
                call_ins = re.match(call_patt, line)
                l = call_ins.group(4)
                get_name = r'(\w+)(\s*)($)'
                lab_name = re.match(get_name, l).group(1)
                find = False
                for element in Labels:
                    if element.name == lab_name:
                        find = True
                        mem_dir = element.mem
                if find == True:
                    if len(Labels) > 0:
                        ins_0 = "auipc x1,0x0\n"
                        ins_1 = f"jalr x1,{mem_dir-(memory)}(x1)\n"
                        objIns0 = InstructionU("auipc", 1, 0x0, memory)
                        Program.append((ins_0, memory))
                        memory += 4
                        objIns1 = InstructionI("jalr", 1, 1, mem_dir-(memory-4), memory)
                        Program.append((ins_1, memory))
                        memory += 4
                        Labels[len(Labels)-1].instructions.append(objIns0)
                        Labels[len(Labels)-1].instructions.append(objIns1)
            elif re.match(jr_patt, line):
                jr_rd = re.match(jr_patt, line).group(4)
                jr_rdPatt = r'(\w+)(\s*)($)'
                rd_jr = re.match(jr_rdPatt, jr_rd)
                for i in range(32):
                    if rd_jr.group(1) in regs[i]:
                        pos_rs1 = i
                        break
                if len(Labels) > 0:
                    new_ins = f"jalr x0,x{pos_rs1}\n"
                    obj_ins = InstructionI("jalr", 0, pos_rs1, 0, memory)
                    Program.append((new_ins, memory))
                    Labels[len(Labels)-1].instructions.append(obj_ins)
                    memory += 4
            elif re.match(ret_patt, line):
                if len(Labels) > 0:
                    new_ins = "jalr x0,x1\n"
                    obj_ins = InstructionI("jalr", 0, 1, 0, memory)
                    Program.append((new_ins, memory))
                    Labels[len(Labels)-1].instructions.append(obj_ins)
                    memory += 4
            #Verifica si es una instrucción común sin pseudo assembler
            elif re.match(ins_patt, line):
                inst = re.match(ins_patt, line)
                inst_name = inst.group(2)
                inst_details = inst.group(4)
                #Verifica si es tipo R
                if inst_name in r_list:
                    param_patt = r'(\w+)(\s*)(\,)(\s*)(\w+)(\s*)(\,)(\s*)(\w+)(\s*)($)'
                    params = re.match(param_patt, inst_details)
                    for i in range(32):
                        if params.group(1) in regs[i]:
                            rd_inst = i
                            break
                    for j in range(32):
                        if params.group(5) in regs[j]:
                            rs1_inst = j
                            break
                    for k in range(32):
                        if params.group(9) in regs[k]:
                            rs2_inst = k
                            break
                    if len(Labels) > 0:
                        new_ins = f"{inst_name} {rd_inst},{rs1_inst},{rs2_inst}\n"
                        obj_ins = InstructionR(inst_name, rd_inst, rs1_inst, rs2_inst, memory)
                        Program.append((new_ins, memory))
                        Labels[len(Labels)-1].instructions.append(obj_ins)
                        memory += 4
                #Verifica si es tipo I de la forma rd, rs1, imm
                elif inst_name in i_list[0]:
                    param_patt = r'(\w+)(\s*\,\s*)(\w+)(\s*\,\s*)(\-?\d+)(\s*)($)'
                    params = re.match(param_patt, inst_details)
                    for i in range(32):
                        if params.group(1) in regs[i]:
                            rd_inst = i
                            break
                    for j in range(32):
                        if params.group(3) in regs[j]:
                            rs1_inst = j
                            break
                    if len(Labels) > 0:
                        imm_inst = int(params.group(5))
                        new_ins = f"{inst_name} {rd_inst},{rs1_inst},{imm_inst}\n"
                        obj_ins = InstructionI(inst_name, rd_inst, rs1_inst, imm_inst, memory)
                        Program.append((new_ins, memory))
                        Labels[len(Labels)-1].instructions.append(obj_ins)
                        memory += 4
                #Verifica si es tipo I de la forma rd,imm(rs1)
                elif inst_name in i_list[1]:
                    param_patt = r'(\w+)(\s*\,\s*)(\-?\d+)(\s*\(\s*)(\w+)(\s*\))(\s*)($)'
                    params = re.match(param_patt, inst_details)
                    for i in range(32):
                        if params.group(1) in regs[i]:
                            rd_inst = i
                            break
                    for j in range(32):
                        if params.group(5) in regs[j]:
                            rs1_inst = j
                            break
                    imm_inst = int(params.group(3))
                    new_ins = f"{inst_name} {rd_inst},{imm_inst}({rs1_inst})\n"
                    obj_ins = InstructionI(inst_name, rd_inst, rs1_inst, imm_inst, memory)
                    Program.append((new_ins, memory))
                    Labels[len(Labels)-1].instructions.append(obj_ins)
                    memory += 4
                #Verifica si es tipo S
                elif inst_name in s_list:
                    param_patt = r'(\w+)(\s*\,\s*)(\-?\d+)(\s*\(\s*)(\w+)(\s*\))(\s*)($)'
                    params = re.match(param_patt, inst_details)
                    for i in range(32):
                        if params.group(1) in regs[i]:
                            rs2_inst = i
                            break
                    for j in range(32):
                        if params.group(5) in regs[j]:
                            rs1_inst = j
                            break
                    imm_inst = int(params.group(3))
                    new_ins = f"{inst_name} {rs2_inst},{imm_inst}({rs1_inst})\n"
                    obj_ins = InstructionS(inst_name, rs1_inst, rs2_inst, imm_inst, memory)
                    Program.append((new_ins, memory))
                    Labels[len(Labels)-1].instructions.append(obj_ins)
                    memory += 4
                #Verifica si es tipo U
                elif inst_name in u_list:
                    param_patt = r'(\w+)(\s*\,\s*)(\-?\d+)(\s*)($)'
                    params = re.match(param_patt, inst_details)
                    for i in range(32):
                        if params.group(1) in regs[i]:
                            rd_inst = i
                            break
                    imm_inst = int(params.group(3))
                    new_ins = f"{inst_name} {rd_inst},{imm_inst}\n"
                    obj_ins = InstructionU(inst_name, rd_inst, imm_inst, memory)
                    Program.append((new_ins, memory))
                    Labels[len(Labels)-1].instructions.append(obj_ins)
                    memory += 4
                #Verifica si es tipo J
                elif inst_name in j_list:
                    param_patt = r'(\w+)(\s*\,\s*)(\-?\d+)(\s*)($)'
                    params = re.match(param_patt, inst_details)
                    for i in range(32):
                        if params.group(1) in regs[i]:
                            rd_inst = i
                            break
                    imm_inst = int(params.group(3))
                    new_ins = f"{inst_name} {rd_inst},{imm_inst}\n"
                    obj_ins = InstructionJ(inst_name, rd_inst, imm_inst, memory)
                    Program.append((new_ins, memory))
                    Labels[len(Labels)-1].instructions.append(obj_ins)
                    memory += 4
                #Verifica si es tipo B
                elif inst_name in b_list:
                    param_patt = r'(\w+)(\s*\,\s*)(\w+)(\s*\,\s*)(\-?\d+)($)'
                    param_patt2 = r'(\w+)(\s*\,\s*)(\w+)(\s*\,\s*)(\D+\w*)($)'
                    if re.match(param_patt, inst_details):
                        params = re.match(param_patt, inst_details)
                        for i in range(32):
                            if params.group(1) in regs[i]:
                                rs1_inst = i
                                break
                        for j in range(32):
                            if params.group(3) in regs[j]:
                                rs2_inst = j
                                break
                        imm_inst = int(params.group(5))
                    elif re.match(param_patt2, inst_details):
                        params = re.match(param_patt2, inst_details)
                        for i in range(32):
                            if params.group(1) in regs[i]:
                                rs1_inst = i
                                break
                        for j in range(32):
                            if params.group(3) in regs[j]:
                                rs2_inst = j
                                break
                        imm_inst = str(params.group(5))
                    new_ins = f"{inst_name} {rs1_inst},{rs2_inst},{imm_inst}\n"
                    obj_ins = InstructionB(inst_name, rs1_inst, rs2_inst, imm_inst, memory)
                    Program.append((new_ins, memory))
                    Labels[len(Labels)-1].instructions.append(obj_ins)
                    memory += 4
    return memory