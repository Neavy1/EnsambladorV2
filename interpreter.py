import re
import sys
from models import Labels, InstructionB, InstructionI, InstructionJ, InstructionR, InstructionS, InstructionU
from pseudo_t import pseudo_translate
from funcs import *


def analyzer(assembler_code):
    memory = pseudo_translate(assembler_code)
    file, core = rectificate()
    core.write("v2.0 raw\n")
    for element in Labels:
        label_line = f"{element.mem:X} <{element.name}>\n"
        # file.write(label_line)
        for object in element.instructions:
            #Decodificacion si es tipo B
            if type(object) == InstructionB:
                bin_ins = [0]*32
                #Asignación del opcode
                opcode_bits = opcode_loader(bin(object.opcode)[2:])
                for i, j in zip(range(0,7), range(25,32)):
                    bin_ins[j] = opcode_bits[i]
                #Asignacion del inmediato
                if isinstance(object.imm, str):
                    for item in Labels:
                        if item.name == object.imm:
                            imm_bits, bin_ins[0] = imm_loader(bin(item.mem), 12)
                elif isinstance(object.imm, int):
                    imm_bits, bin_ins[0] = imm_loader(bin(object.imm), 12)
                for i, j in zip(range(1,7), range(1,7)):
                    bin_ins[i] = imm_bits[j]
                bin_ins[24] = imm_bits[0]
                for i, j in zip(range(20,24), range(7,11)):
                    bin_ins[i] = imm_bits[j]
                #Asignacion de rs2
                rs2_bits = rs2_loader(object.rs2[2:])
                for i, j in zip(range(7,12), range(0,5)):
                    bin_ins[i] = rs2_bits[j]
                #Asignacion de rs1
                rs1_bits = rs1_loader(object.rs1[2:])
                for i, j in zip(range(12,17), range(0,5)):
                    bin_ins[i] = rs1_bits[j]   
                #Asignacion de Func3
                func3_bits = func3_loader(bin(object.func3)[2:])
                for i, j in zip(range(17,20), range(0,3)):
                    bin_ins[i] = func3_bits[j]
                #Creacion de variables finales conviertiendo los valores
                instruction_hex, instruction_bin, finalMem, intMem = formater(bin_ins, object)
                instruction = f"{instruction_bin}\n"
                writingFiles(file, core, instruction, instruction_hex, intMem)
            
            #Decodificación si es tipo R
            elif type(object) == InstructionR:
                bin_ins = [0]*32
                #Asignacion del func7
                func7_bits = func7_loader(object.func7[2:])
                for i in range(0,7):
                    bin_ins[i] = func7_bits[i]
                #Asignacion del rs2
                rs2_bits = rs2_loader(object.rs2[2:])
                for i, j in zip(range(0,6),range(7,12)):
                    bin_ins[j] = rs2_bits[i]
                #Asignacion del rs1
                rs1_bits = rs1_loader(object.rs1[2:])
                for i, j in zip(range(0,6),range(12,17)):
                    bin_ins[j] = rs1_bits[i]  
                #Asignacion del func3
                func3_bits = func3_loader(object.func3[2:])
                for i, j in zip(range(0,3), range(17,20)):
                    bin_ins[j] = func3_bits[i]
                #Asignacion del rd
                rd_bits = rd_loader(object.rd[2:])
                for i, j in zip(range(0,6), range(20,25)):
                    bin_ins[j] = rd_bits[i]
                #Asignacion opcode
                opcode_bits = opcode_loader(bin(object.opcode)[2:])
                for i, j in zip(range(0,7), range(25,32)):
                    bin_ins[j] = opcode_bits[i]
                #Variables finales
                instruction_hex, instruction_bin, finalMem, intMem = formater(bin_ins, object)
                instruction = f"{instruction_bin}\n"
                writingFiles(file, core, instruction, instruction_hex, intMem)
            #Instrucciones tipo I
            elif type(object) == InstructionI:
                bin_ins = [0]*32
                #Asignación del imm
                imm_bits, bin_ins[0] = imm_loader(object.imm, 12)
                for i in range(0,12):
                    bin_ins[i] = imm_bits[i]
                #Asignacion del rs1
                rs1_bits = rs1_loader(object.rs1[2:])
                for i, j in zip(range(0,5), range(12, 17)):
                    bin_ins[j] = rs1_bits[i]
                #Asignación de func3
                func3_bits = func3_loader(object.func3[2:])
                for i, j in zip(range(0,3), range(17,20)):
                    bin_ins[j] = func3_bits[i]
                #Asignación de rd
                rd_bits = rd_loader(object.rd[2:])
                for i, j in zip(range(0,5), range(20,25)):
                    bin_ins[j] = rd_bits[i]
                #Asignación de opcode
                opcode_bits = opcode_loader(bin(object.opcode)[2:])
                for i, j in zip(range(0,7), range(25,32)):
                    bin_ins[j] = opcode_bits[i]
                #Variables finales
                instruction_hex, instruction_bin, finalMem, intMem = formater(bin_ins, object)
                instruction = f"{instruction_bin}\n"
                # instruction = f"\t{intMem}\t\t\t{finalMem}\t\t{instruction_hex}\t\t{instruction_bin}\n"
                writingFiles(file, core, instruction, instruction_hex, intMem)
            #Asignación tipo S
            elif type(object) == InstructionS:
                bin_ins = [0]*32
                #Asignación del opcode
                opcode_bits = opcode_loader(bin(object.opcode)[2:])
                for i, j in zip(range(0,7), range(25,32)):
                    bin_ins[j] = opcode_bits[i]
                #Asignacion del inmediato
                imm_bits, bin_ins[0] = imm_loader(object.imm, 12)
                for m in range(0,7):
                    bin_ins[m] = imm_bits[m]
                for n, o in zip(range(7,12), range(20,25)):
                    bin_ins[o] = imm_bits[n]
                #Asignacion de rs2
                rs2_bits = rs2_loader(object.rs2[2:])
                for i, j in zip(range(7,12), range(0,5)):
                    bin_ins[i] = rs2_bits[j]
                #Asignacion de rs1
                rs1_bits = rs1_loader(object.rs1[2:])
                for i, j in zip(range(12,17), range(0,5)):
                    bin_ins[i] = rs1_bits[j]   
                #Asignacion de Func3
                func3_bits = func3_loader(bin(object.func3)[2:])
                for i, j in zip(range(17,20), range(0,3)):
                    bin_ins[i] = func3_bits[j]
                #Creacion de variables finales conviertiendo los valores
                instruction_hex, instruction_bin, finalMem, intMem = formater(bin_ins, object)
                instruction = f"{instruction_bin}\n"
                writingFiles(file, core, instruction, instruction_hex, intMem)
            #Instrucciones tipo U
            elif type(object) == InstructionU:
                bin_ins = [0]*32
                #Asignación del imm
                imm_bits, bin_ins[0] = imm_loader(object.imm, 20)
                for i in range(0,20):
                    bin_ins[i] = imm_bits[i]
                #Asignación de rd
                rd_bits = rd_loader(object.rd[2:])
                for i, j in zip(range(0,5), range(20,25)):
                    bin_ins[j] = rd_bits[i]
                #Asignación del opcode
                opcode_bits = opcode_loader(bin(object.opcode)[2:])
                for i, j in zip(range(0,7), range(25,32)):
                    bin_ins[j] = opcode_bits[i]
                #Creacion de variables finales conviertiendo los valores
                instruction_hex, instruction_bin, finalMem, intMem = formater(bin_ins, object)
                instruction = f"{instruction_bin}\n"
                writingFiles(file, core, instruction, instruction_hex, intMem)
            #Instrucciones tipo J
            elif type(object) == InstructionJ:
                bin_ins = [0]*32
                #Asignación del imm
                imm_bits, bin_ins[0] = imm_loader(object.imm, 20)
                for i, j in zip(range(1,11), range(9,19)):
                    bin_ins[i] = imm_bits[j]
                bin_ins[11] = imm_bits[8]
                for i, j in zip(range(0,8), range(12,20)):
                    bin_ins[j] = imm_bits[i]
                #Asignación de rd
                rd_bits = rd_loader(object.rd[2:])
                for i, j in zip(range(0,5), range(20,25)):
                    bin_ins[j] = rd_bits[i]
                #Asignación del opcode
                opcode_bits = opcode_loader(bin(object.opcode)[2:])
                for i, j in zip(range(0,7), range(25,32)):
                    bin_ins[j] = opcode_bits[i]
                #Creacion de variables finales conviertiendo los valores
                instruction_hex, instruction_bin, finalMem, intMem = formater(bin_ins, object)
                instruction = f"{instruction_bin}\n"
                writingFiles(file, core, instruction, instruction_hex, intMem)
    return memory, file, core

#Función para ejecutar el programa desde consola
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Correct use: python interpreter.py assembler_code.asm")
    else:
        assembler_code = sys.argv[1]
        memory, file, core = analyzer(assembler_code)
        fuller(memory, file, core, total_memory=1500)
##'''