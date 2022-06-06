

import os
import pin
import assembly as ASM


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "micro.bin")

micro = [pin.HLT for _ in range(0x10000)]

def compile_addr2(addr, ir, psw, idx):
    global micro
    op = ir & 0xf0
    amd = (ir >> 2) & 3
    ams = ir & 3

    INST = ASM.INSTRUCTIONS[2]
    if op not in INST:
        micro[addr] = pin.CYC
        return 
    am = (amd, ams)
    if am not in INST[op]:
        micro[addr] = pin.CYC
        return

    EXEC = INST[op][am] 
    if idx < len(EXEC):
        micro[addr] = EXEC[idx]
    else:
        micro[addr] = pin.CYC    

def compile_addr1(addr, ir, psw, idx):
    pass

def compile_addr0(addr, ir, psw, idx):

    global micro
    op = ir

    INST = ASM.INSTRUCTIONS[0]
    
    if op not in INST:
        micro[addr] = pin.CYC
        return 

    EXEC = INST[op]
    if idx < len(EXEC):
        micro[addr] = EXEC[idx]
    else:
        micro[addr] = pin.CYC


for addr in range(0x10000):
    ir = addr >> 8
    psw = (addr >> 4) & 0xf
    cyc = addr & 0xf
    
    if(cyc < len(ASM.FETCH)):
        micro[addr] = ASM.FETCH[cyc]
        continue
    
    addr2 = ir & (1 << 7)
    addr1 = ir & (1 << 6)

    idx = cyc - len(ASM.FETCH)

    if addr2:
        compile_addr2(addr, ir, psw, idx)
    elif addr1:
        compile_addr1(addr, ir, psw, idx)
    else :
        compile_addr0(addr, ir, psw, idx)

with open(filename, 'wb') as file:
    for val in micro:
        value = val.to_bytes(4, byteorder='little')
        file.write(value)



print('compile micor finished !!')

 

