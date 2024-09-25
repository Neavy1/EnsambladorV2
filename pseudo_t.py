import re
from regs import regs
from models import Labels, Program, InstructionB, InstructionI, InstructionJ, InstructionR, InstructionS, InstructionU, Label
from ins_type import r_list, i_list, j_list, s_list, u_list, b_list
from funcs import fuller
from typing import Callable

def pseudo_translate(assembler_code):
    label_patt = r'(\s*)(\D+\w*)(\:)'
    mv_patt = r'(\s*)([m][v])(\s+)(.+)($)'
    call_patt = r'(\s*)(call)(\s+)(\w+)(\s*)($)'
    jr_patt = r'(\s*)(jr)(\s+)(\w+)(\s*)($)'
    ret_patt = r'(\s*)(ret)(\s*)($)'
    ins_patt = r'(\s*)([a-z]+)(\s+)(.+)(\n|$)'
    li_patt = r'(\s*)(li)(\s+)(\w+)(\s*\,\s*)(\-?\d+)(\s*)($)'
    not_patt = r'(\s*)(not)(\s+)(\w+)(\s*\,\s*)(\w+)(\s*)($)'
    neg_patt = r'(\s*)(neg)(\s+)(\w+)(\s*\,\s*)(\w+)(\s*)($)'
    nop_patt = r'(\s*)(nop)(\s*)($)'
    j_patt = r'(\s*)(j)(\s+)(\w+)(\s*)($)'

    # Variable de memoria
    memory = 0
    transactional_instrs: list[TransactionalInstruction] = []

    # Código en assembler recibido desde la consola
    with open(assembler_code, 'r') as f:
        for line in f:
            if re.match(label_patt, line):
                l = re.match(label_patt, line)
                new = Label(memory, l.group(2))
                Labels.append(new)
                Program.append((line, memory))
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
            elif re.match(call_patt, line): #TODO: CALL
                call_ins = re.match(call_patt, line)
                label = call_ins.group(4)
                mem_dir = None
                for element in Labels:
                    if element.name == label:
                        mem_dir = element.mem
                        break
                
                # ?Create auipc instruction 
                new_ins_auipc = f"auipc x1, 0x0\n"
                obj_ins_auipc = InstructionU("auipc", 1, 0x0, memory)
                Program.append((new_ins_auipc, memory))
                memory += 4
                Labels[len(Labels)-1].instructions.append(obj_ins_auipc)

                # ? Check if label exists
                if mem_dir is not None:
                    # ?Create jalr instruction
                    new_ins_jalr = f"jalr x1, {mem_dir - memory}(x1)\n"
                    obj_ins_jalr = InstructionI("jalr", 1, 1, mem_dir - (memory - 4), memory)
                    Program.append((new_ins_jalr, memory))

                    Labels[len(Labels)-1].instructions.append(obj_ins_jalr)
                else:
                    # ?Create jalr instruction as transactional
                    # * It will be updated

                    inst_list = Labels[len(Labels)-1].instructions
                    inst_pos = len(inst_list)

                    transactional_instrs.append(
                        TransactionalInstruction(
                            inst_list,
                            inst_pos,
                            label,
                            InstructionI,
                            lambda x: ["jalr", 1, 1, x - (memory - 4), memory]
                        )
                    )
                    # print(f"Etiqueta {label} no encontrada.")
                memory += 4
            elif re.match(jr_patt, line):
                jr_ins = re.match(jr_patt, line)
                reg = jr_ins.group(4)
                for i in range(32):
                    if reg in regs[i]:
                        pos_rs1 = i
                        break
                new_ins = f"jalr x0, {reg}\n"
                obj_ins = InstructionI("jalr", 0, pos_rs1, 0, memory)
                Program.append((new_ins, memory))
                Labels[len(Labels)-1].instructions.append(obj_ins)
                memory += 4
            elif re.match(ret_patt, line):
                new_ins = "jalr x0, x1\n"
                obj_ins = InstructionI("jalr", 0, 1, 0, memory)
                Program.append((new_ins, memory))
                Labels[len(Labels)-1].instructions.append(obj_ins)
                memory += 4
            elif re.match(li_patt, line):
                li_ins = re.match(li_patt, line)
                reg = li_ins.group(4)
                imm = int(li_ins.group(6))
                for i in range(32):
                    if reg in regs[i]:
                        pos_rd = i
                        break
                new_ins = f"addi {reg}, x0, {imm}\n"
                obj_ins = InstructionI("addi", pos_rd, 0, imm, memory)
                Program.append((new_ins, memory))
                Labels[len(Labels)-1].instructions.append(obj_ins)
                memory += 4
            elif re.match(not_patt, line):
                not_ins = re.match(not_patt, line)
                reg_dest = not_ins.group(4)
                reg_src = not_ins.group(6)
                for i in range(32):
                    if reg_dest in regs[i]:
                        pos_rd = i
                        break
                for j in range(32):
                    if reg_src in regs[j]:
                        pos_rs1 = j
                        break
                new_ins = f"xori {reg_dest}, {reg_src}, -1\n"
                obj_ins = InstructionI("xori", pos_rd, pos_rs1, -1, memory)
                Program.append((new_ins, memory))
                Labels[len(Labels)-1].instructions.append(obj_ins)
                memory += 4
            elif re.match(neg_patt, line):
                neg_ins = re.match(neg_patt, line)
                reg_dest = neg_ins.group(4)
                reg_src = neg_ins.group(6)
                for i in range(32):
                    if reg_dest in regs[i]:
                        pos_rd = i
                        break
                for j in range(32):
                    if reg_src in regs[j]:
                        pos_rs1 = j
                        break
                new_ins = f"sub {reg_dest}, x0, {reg_src}\n"
                obj_ins = InstructionR("sub", pos_rd, 0, pos_rs1, memory)
                Program.append((new_ins, memory))
                Labels[len(Labels)-1].instructions.append(obj_ins)
                memory += 4
            elif re.match(nop_patt, line):
                new_ins = "addi x0, x0, 0\n"
                obj_ins = InstructionI("addi", 0, 0, 0, memory)
                Program.append((new_ins, memory))
                Labels[len(Labels)-1].instructions.append(obj_ins)
                memory += 4
            elif re.match(j_patt, line): #TODO: J
                j_ins = re.match(j_patt, line)
                label = j_ins.group(4)
                mem_dir = None
                for element in Labels:
                    if element.name == label:
                        mem_dir = element.mem
                        break
                if mem_dir is not None:
                    new_ins = f"jal x0, {mem_dir}\n"
                    obj_ins = InstructionJ("jal", 0, mem_dir, memory)
                    Program.append((new_ins, memory))
                    Labels[len(Labels)-1].instructions.append(obj_ins)
                else:

                    inst_list = Labels[len(Labels)-1].instructions
                    inst_pos = len(inst_list)

                    transactional_instrs.append(
                        TransactionalInstruction(
                            inst_list,
                            inst_pos,
                            label,
                            InstructionJ,
                            lambda x: ["jal", 0, x, memory]
                        )
                    )
                    # print(f"Etiqueta {label} no encontrada. para J")
                
                memory += 4
            # Otros patrones de instrucciones
            elif re.match(ins_patt, line):
                inst = re.match(ins_patt, line)
                inst_name = inst.group(2)
                inst_details = inst.group(4)
                # Verifica si es tipo R
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
                    # rs1_inst = j
                    # ? Código recién cambiado  
                    # for k in range(32):
                    #     if params.group(9) in regs[k]:
                    #         rs2_inst = k
                    #         break
                    if len(Labels) > 0:
                        new_ins = f"{inst_name} {rd_inst},{rs1_inst},{rs2_inst}\n"
                        obj_ins = InstructionR(inst_name, rd_inst, rs1_inst, rs2_inst, memory)
                        Program.append((new_ins, memory))
                        Labels[len(Labels)-1].instructions.append(obj_ins)
                        memory += 4
                # Verifica si es tipo I de la forma rd, rs1, imm
                elif inst_name in i_list:
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
                # Verifica si es tipo I de la forma rd,imm(rs1)
                elif inst_name in i_list:
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
                # Verifica si es tipo S
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
                # Verifica si es tipo U
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
                # Verifica si es tipo J
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
                # Verifica si es tipo B
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

        for transactional_instr in transactional_instrs:
            label = transactional_instr.label
            mem_dir = None
            for element in Labels:
                if element.name == label:
                    mem_dir = element.mem
                    break
            
            if mem_dir is None:
                print(f"Etiqueta {label} no encontrada.")
                continue

            inst_params = transactional_instr.inst_params(mem_dir)
            inst = transactional_instr.inst_constructor(*inst_params)
            transactional_instr.inst_list.insert(transactional_instr.inst_pos, inst)
    return memory


class TransactionalInstruction:
    def __init__(
        self,
        inst_list: list,
        inst_pos: int,
        label: str,
        inst_constructor: type,
        inst_params: Callable[[any], list[any]]
    ):
        self.inst_list = inst_list
        self.inst_pos = inst_pos
        self.label = label
        self.inst_constructor = inst_constructor
        self.inst_params = inst_params
    