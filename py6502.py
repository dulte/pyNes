import numpy as np


class Py6502:
    def __init__(self):
        # Variables for storing bus
        self.bus = None


        #Variables for holding the registers and pointers
        self.a              = np.uint8(0x00)
        self.x              = np.uint8(0x00)
        self.y              = np.uint8(0x00)
        self.stkp           = np.uint8(0x00)
        self.pc             = np.uint16(0x0000)
        self.status         = np.uint8(0x00)

        #Variables for holding the internal state of the cpu
        self.fetched        = np.uint8(0x00)
        self.temp           = np.uint16(0x0000)
        self.addr_abs       = np.uint16(0x0000)
        self.addr_rel       = np.uint8(0x00)
        self.opcode         = np.uint8(0x00)
        self.cycles         = np.uint8(0x00)
        self.clock_count    = np.uint32(0x00)

        # Different Flags:
        self.flags = {
            "C" : (1 << 0), # Carry
            "Z" : (1 << 1), # Zero
            "I" : (1 << 2), # Disable Interrupts
            "D" : (1 << 3), # Decimal Mode (not used)
            "B" : (1 << 4), # Break
            "U" : (1 << 5), # Unused
            "V" : (1 << 6), # Overflow
            "N" : (1 << 7)  # Negative
        }

        # Sets up the lookup table for different reads
        self.lookup = [ 
            {"name": "BRK", "operate": self.BRK, "addrmode": self.IMM, "cycles": 7},     {"name": "ORA", "operate": self.ORA, "addrmode": self.IZX, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 8},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 3},     {"name": "ORA", "operate": self.ORA, "addrmode": self.ZP0, "cycles": 3},     {"name": "ASL", "operate": self.ASL, "addrmode": self.ZP0, "cycles": 5},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 5},     {"name": "PHP", "operate": self.PHP, "addrmode": self.IMP, "cycles": 3},     {"name": "ORA", "operate": self.ORA, "addrmode": self.IMM, "cycles": 2},     {"name": "ASL", "operate": self.ASL, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 4},     {"name": "ORA", "operate": self.ORA, "addrmode": self.ABS, "cycles": 4},     {"name": "ASL", "operate": self.ASL, "addrmode": self.ABS, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 6}, 
            {"name": "BPL", "operate": self.BPL, "addrmode": self.REL, "cycles": 2},     {"name": "ORA", "operate": self.ORA, "addrmode": self.IZY, "cycles": 5},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 8},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 4},     {"name": "ORA", "operate": self.ORA, "addrmode": self.ZPX, "cycles": 4},     {"name": "ASL", "operate": self.ASL, "addrmode": self.ZPX, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 6},     {"name": "CLC", "operate": self.CLC, "addrmode": self.IMP, "cycles": 2},     {"name": "ORA", "operate": self.ORA, "addrmode": self.ABY, "cycles": 4},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 7},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 4},     {"name": "ORA", "operate": self.ORA, "addrmode": self.ABX, "cycles": 4},     {"name": "ASL", "operate": self.ASL, "addrmode": self.ABX, "cycles": 7},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 7}, 
            {"name": "JSR", "operate": self.JSR, "addrmode": self.ABS, "cycles": 6},     {"name": "AND", "operate": self.AND, "addrmode": self.IZX, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 8},     {"name": "BIT", "operate": self.BIT, "addrmode": self.ZP0, "cycles": 3},     {"name": "AND", "operate": self.AND, "addrmode": self.ZP0, "cycles": 3},     {"name": "ROL", "operate": self.ROL, "addrmode": self.ZP0, "cycles": 5},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 5},     {"name": "PLP", "operate": self.PLP, "addrmode": self.IMP, "cycles": 4},     {"name": "AND", "operate": self.AND, "addrmode": self.IMM, "cycles": 2},     {"name": "ROL", "operate": self.ROL, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "BIT", "operate": self.BIT, "addrmode": self.ABS, "cycles": 4},     {"name": "AND", "operate": self.AND, "addrmode": self.ABS, "cycles": 4},     {"name": "ROL", "operate": self.ROL, "addrmode": self.ABS, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 6}, 
            {"name": "BMI", "operate": self.BMI, "addrmode": self.REL, "cycles": 2},     {"name": "AND", "operate": self.AND, "addrmode": self.IZY, "cycles": 5},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 8},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 4},     {"name": "AND", "operate": self.AND, "addrmode": self.ZPX, "cycles": 4},     {"name": "ROL", "operate": self.ROL, "addrmode": self.ZPX, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 6},     {"name": "SEC", "operate": self.SEC, "addrmode": self.IMP, "cycles": 2},     {"name": "AND", "operate": self.AND, "addrmode": self.ABY, "cycles": 4},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 7},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 4},     {"name": "AND", "operate": self.AND, "addrmode": self.ABX, "cycles": 4},     {"name": "ROL", "operate": self.ROL, "addrmode": self.ABX, "cycles": 7},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 7}, 
            {"name": "RTI", "operate": self.RTI, "addrmode": self.IMP, "cycles": 6},     {"name": "EOR", "operate": self.EOR, "addrmode": self.IZX, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 8},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 3},     {"name": "EOR", "operate": self.EOR, "addrmode": self.ZP0, "cycles": 3},     {"name": "LSR", "operate": self.LSR, "addrmode": self.ZP0, "cycles": 5},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 5},     {"name": "PHA", "operate": self.PHA, "addrmode": self.IMP, "cycles": 3},     {"name": "EOR", "operate": self.EOR, "addrmode": self.IMM, "cycles": 2},     {"name": "LSR", "operate": self.LSR, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "JMP", "operate": self.JMP, "addrmode": self.ABS, "cycles": 3},     {"name": "EOR", "operate": self.EOR, "addrmode": self.ABS, "cycles": 4},     {"name": "LSR", "operate": self.LSR, "addrmode": self.ABS, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 6}, 
            {"name": "BVC", "operate": self.BVC, "addrmode": self.REL, "cycles": 2},     {"name": "EOR", "operate": self.EOR, "addrmode": self.IZY, "cycles": 5},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 8},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 4},     {"name": "EOR", "operate": self.EOR, "addrmode": self.ZPX, "cycles": 4},     {"name": "LSR", "operate": self.LSR, "addrmode": self.ZPX, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 6},     {"name": "CLI", "operate": self.CLI, "addrmode": self.IMP, "cycles": 2},     {"name": "EOR", "operate": self.EOR, "addrmode": self.ABY, "cycles": 4},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 7},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 4},     {"name": "EOR", "operate": self.EOR, "addrmode": self.ABX, "cycles": 4},     {"name": "LSR", "operate": self.LSR, "addrmode": self.ABX, "cycles": 7},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 7}, 
            {"name": "RTS", "operate": self.RTS, "addrmode": self.IMP, "cycles": 6},     {"name": "ADC", "operate": self.ADC, "addrmode": self.IZX, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 8},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 3},     {"name": "ADC", "operate": self.ADC, "addrmode": self.ZP0, "cycles": 3},     {"name": "ROR", "operate": self.ROR, "addrmode": self.ZP0, "cycles": 5},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 5},     {"name": "PLA", "operate": self.PLA, "addrmode": self.IMP, "cycles": 4},     {"name": "ADC", "operate": self.ADC, "addrmode": self.IMM, "cycles": 2},     {"name": "ROR", "operate": self.ROR, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "JMP", "operate": self.JMP, "addrmode": self.IND, "cycles": 5},     {"name": "ADC", "operate": self.ADC, "addrmode": self.ABS, "cycles": 4},     {"name": "ROR", "operate": self.ROR, "addrmode": self.ABS, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 6}, 
            {"name": "BVS", "operate": self.BVS, "addrmode": self.REL, "cycles": 2},     {"name": "ADC", "operate": self.ADC, "addrmode": self.IZY, "cycles": 5},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 8},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 4},     {"name": "ADC", "operate": self.ADC, "addrmode": self.ZPX, "cycles": 4},     {"name": "ROR", "operate": self.ROR, "addrmode": self.ZPX, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 6},     {"name": "SEI", "operate": self.SEI, "addrmode": self.IMP, "cycles": 2},     {"name": "ADC", "operate": self.ADC, "addrmode": self.ABY, "cycles": 4},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 7},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 4},     {"name": "ADC", "operate": self.ADC, "addrmode": self.ABX, "cycles": 4},     {"name": "ROR", "operate": self.ROR, "addrmode": self.ABX, "cycles": 7},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 7}, 
            {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 2},     {"name": "STA", "operate": self.STA, "addrmode": self.IZX, "cycles": 6},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 6},     {"name": "STY", "operate": self.STY, "addrmode": self.ZP0, "cycles": 3},     {"name": "STA", "operate": self.STA, "addrmode": self.ZP0, "cycles": 3},     {"name": "STX", "operate": self.STX, "addrmode": self.ZP0, "cycles": 3},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 3},     {"name": "DEY", "operate": self.DEY, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 2},     {"name": "TXA", "operate": self.TXA, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "STY", "operate": self.STY, "addrmode": self.ABS, "cycles": 4},     {"name": "STA", "operate": self.STA, "addrmode": self.ABS, "cycles": 4},     {"name": "STX", "operate": self.STX, "addrmode": self.ABS, "cycles": 4},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 4}, 
            {"name": "BCC", "operate": self.BCC, "addrmode": self.REL, "cycles": 2},     {"name": "STA", "operate": self.STA, "addrmode": self.IZY, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 6},     {"name": "STY", "operate": self.STY, "addrmode": self.ZPX, "cycles": 4},     {"name": "STA", "operate": self.STA, "addrmode": self.ZPX, "cycles": 4},     {"name": "STX", "operate": self.STX, "addrmode": self.ZPY, "cycles": 4},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 4},     {"name": "TYA", "operate": self.TYA, "addrmode": self.IMP, "cycles": 2},     {"name": "STA", "operate": self.STA, "addrmode": self.ABY, "cycles": 5},     {"name": "TXS", "operate": self.TXS, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 5},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 5},     {"name": "STA", "operate": self.STA, "addrmode": self.ABX, "cycles": 5},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 5},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 5}, 
            {"name": "LDY", "operate": self.LDY, "addrmode": self.IMM, "cycles": 2},     {"name": "LDA", "operate": self.LDA, "addrmode": self.IZX, "cycles": 6},     {"name": "LDX", "operate": self.LDX, "addrmode": self.IMM, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 6},     {"name": "LDY", "operate": self.LDY, "addrmode": self.ZP0, "cycles": 3},     {"name": "LDA", "operate": self.LDA, "addrmode": self.ZP0, "cycles": 3},     {"name": "LDX", "operate": self.LDX, "addrmode": self.ZP0, "cycles": 3},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 3},     {"name": "TAY", "operate": self.TAY, "addrmode": self.IMP, "cycles": 2},     {"name": "LDA", "operate": self.LDA, "addrmode": self.IMM, "cycles": 2},     {"name": "TAX", "operate": self.TAX, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "LDY", "operate": self.LDY, "addrmode": self.ABS, "cycles": 4},     {"name": "LDA", "operate": self.LDA, "addrmode": self.ABS, "cycles": 4},     {"name": "LDX", "operate": self.LDX, "addrmode": self.ABS, "cycles": 4},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 4}, 
            {"name": "BCS", "operate": self.BCS, "addrmode": self.REL, "cycles": 2},     {"name": "LDA", "operate": self.LDA, "addrmode": self.IZY, "cycles": 5},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 5},     {"name": "LDY", "operate": self.LDY, "addrmode": self.ZPX, "cycles": 4},     {"name": "LDA", "operate": self.LDA, "addrmode": self.ZPX, "cycles": 4},     {"name": "LDX", "operate": self.LDX, "addrmode": self.ZPY, "cycles": 4},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 4},     {"name": "CLV", "operate": self.CLV, "addrmode": self.IMP, "cycles": 2},     {"name": "LDA", "operate": self.LDA, "addrmode": self.ABY, "cycles": 4},     {"name": "TSX", "operate": self.TSX, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 4},     {"name": "LDY", "operate": self.LDY, "addrmode": self.ABX, "cycles": 4},     {"name": "LDA", "operate": self.LDA, "addrmode": self.ABX, "cycles": 4},     {"name": "LDX", "operate": self.LDX, "addrmode": self.ABY, "cycles": 4},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 4}, 
            {"name": "CPY", "operate": self.CPY, "addrmode": self.IMM, "cycles": 2},     {"name": "CMP", "operate": self.CMP, "addrmode": self.IZX, "cycles": 6},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 8},     {"name": "CPY", "operate": self.CPY, "addrmode": self.ZP0, "cycles": 3},     {"name": "CMP", "operate": self.CMP, "addrmode": self.ZP0, "cycles": 3},     {"name": "DEC", "operate": self.DEC, "addrmode": self.ZP0, "cycles": 5},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 5},     {"name": "INY", "operate": self.INY, "addrmode": self.IMP, "cycles": 2},     {"name": "CMP", "operate": self.CMP, "addrmode": self.IMM, "cycles": 2},     {"name": "DEX", "operate": self.DEX, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "CPY", "operate": self.CPY, "addrmode": self.ABS, "cycles": 4},     {"name": "CMP", "operate": self.CMP, "addrmode": self.ABS, "cycles": 4},     {"name": "DEC", "operate": self.DEC, "addrmode": self.ABS, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 6}, 
            {"name": "BNE", "operate": self.BNE, "addrmode": self.REL, "cycles": 2},     {"name": "CMP", "operate": self.CMP, "addrmode": self.IZY, "cycles": 5},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 8},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 4},     {"name": "CMP", "operate": self.CMP, "addrmode": self.ZPX, "cycles": 4},     {"name": "DEC", "operate": self.DEC, "addrmode": self.ZPX, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 6},     {"name": "CLD", "operate": self.CLD, "addrmode": self.IMP, "cycles": 2},     {"name": "CMP", "operate": self.CMP, "addrmode": self.ABY, "cycles": 4},     {"name": "NOP", "operate": self.NOP, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 7},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 4},     {"name": "CMP", "operate": self.CMP, "addrmode": self.ABX, "cycles": 4},     {"name": "DEC", "operate": self.DEC, "addrmode": self.ABX, "cycles": 7},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 7}, 
            {"name": "CPX", "operate": self.CPX, "addrmode": self.IMM, "cycles": 2},     {"name": "SBC", "operate": self.SBC, "addrmode": self.IZX, "cycles": 6},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 8},     {"name": "CPX", "operate": self.CPX, "addrmode": self.ZP0, "cycles": 3},     {"name": "SBC", "operate": self.SBC, "addrmode": self.ZP0, "cycles": 3},     {"name": "INC", "operate": self.INC, "addrmode": self.ZP0, "cycles": 5},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 5},     {"name": "INX", "operate": self.INX, "addrmode": self.IMP, "cycles": 2},     {"name": "SBC", "operate": self.SBC, "addrmode": self.IMM, "cycles": 2},     {"name": "NOP", "operate": self.NOP, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.SBC, "addrmode": self.IMP, "cycles": 2},     {"name": "CPX", "operate": self.CPX, "addrmode": self.ABS, "cycles": 4},     {"name": "SBC", "operate": self.SBC, "addrmode": self.ABS, "cycles": 4},     {"name": "INC", "operate": self.INC, "addrmode": self.ABS, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 6}, 
            {"name": "BEQ", "operate": self.BEQ, "addrmode": self.REL, "cycles": 2},     {"name": "SBC", "operate": self.SBC, "addrmode": self.IZY, "cycles": 5},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 8},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 4},     {"name": "SBC", "operate": self.SBC, "addrmode": self.ZPX, "cycles": 4},     {"name": "INC", "operate": self.INC, "addrmode": self.ZPX, "cycles": 6},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 6},     {"name": "SED", "operate": self.SED, "addrmode": self.IMP, "cycles": 2},     {"name": "SBC", "operate": self.SBC, "addrmode": self.ABY, "cycles": 4},     {"name": "NOP", "operate": self.NOP, "addrmode": self.IMP, "cycles": 2},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 7},     {"name": "???", "operate": self.NOP, "addrmode": self.IMP, "cycles": 4},     {"name": "SBC", "operate": self.SBC, "addrmode": self.ABX, "cycles": 4},     {"name": "INC", "operate": self.INC, "addrmode": self.ABX, "cycles": 7},     {"name": "???", "operate": self.XXX, "addrmode": self.IMP, "cycles": 7}, 
        ]

    """ 
    Connects the cpu to the bus
    """

    def connectBus(self, bus):
        self.bus = bus

    """
    Function for reading and writing through the bus
    """

    def read(self, address: np.uint16) -> np.uint8:
        return self.bus.read(address)

    def write(self, address: np.uint16, data: np.uint8):
        return self.bus.write(address, data)



    """
    Function for fetching next piece of data
    """
    def fetch(self) -> np.uint8:
        if(not self.lookup[self.opcode]["addrmode"] == self.IMP):
            self.fetched = self.read(self.addr_abs)
        return self.fetched
    """
    Function for getting and setting flags
    """
    def getFlag(self,flag: str) -> np.uint8:
        if self.status & self.flags[flag] > 0:
            return 1
        else:
            return 0

    def setFlag(self,flag: str, data: bool):
        if data:
            self.status |= self.flags[flag]
        else:
            self.status &= ~self.flags[flag]



    """
    Function for interupts, reset and most importantly CLOCK
    """

    def reset(self):
        pass

    def irq(self):
        pass

    def nmi(self):
        pass

    def clock(self):
        pass
    """
    Below are the addressing mode functions
    """
    def ABS(self) -> np.uint8:
        lo = np.uint16(self.read(self.pc))
        self.pc += 1
        hi = np.uint16(self.read(self.pc))
        self.pc += 1

        self.addr_abs = (hi << 8) | lo

        return 0

    def ABX(self) -> np.uint8:
        lo = np.uint16(self.read(self.pc))
        self.pc += 1
        hi = np.uint16(self.read(self.pc))
        self.pc += 1

        self.addr_abs = (hi << 8) | lo

        self.addr_abs += self.x

        if (self.addr_abs & 0xFF00) != (hi << 8):
            return 1
        else:
            return 0

    def ABY(self) -> np.uint8:
        lo = np.uint16(self.read(self.pc))
        self.pc += 1
        hi = np.uint16(self.read(self.pc))
        self.pc += 1

        self.addr_abs = (hi << 8) | lo

        self.addr_abs += self.y

        if (self.addr_abs & 0xFF00) != (hi << 8):
            return 1
        else:
            return 0

    def IMM(self) -> np.uint8:
        self.addr_abs = self.pc + 1 #Might be wrong 
        return 0

    def IMP(self) -> np.uint8:
        self.fetched = self.a
        return 0

    def IND(self) -> np.uint8:
        ptr_lo = np.uint16(self.read(self.pc))
        self.pc += 1
        ptr_hi = np.uint16(self.read(self.pc))
        self.pc += 1

        ptr = np.uint16( (ptr_hi << 8) | ptr_lo)

        if ptr_lo == 0x00FF:
            lo = self.read(ptr)
            hi = self.read(ptr & 0xFF00)
            self.addr_abs = (hi << 8) | lo

        else:
            lo = self.read(ptr)
            hi = self.read(ptr + 1)
            self.addr_abs = (hi << 8) | lo
        
        return 0

    def IZX(self) -> np.uint8:
        temp = np.uint16(self.read(self.pc))
        self.pc += 1

        lo = self.read(np.uint16(temp + self.x) & 0x00FF)
        hi = self.read(np.uint16(temp + self.x + 1) & 0x00FF)

        self.addr_abs = (hi << 8) | lo

        return 0

    def IZY(self) -> np.uint8:
        temp = np.uint16(self.read(self.pc))
        self.pc += 1

        lo = self.read(np.uint16(temp) & 0x00FF)
        hi = self.read(np.uint16(temp + 1) & 0x00FF)

        self.addr_abs = (hi << 8) | lo
        self.addr_abs += self.y

        if (self.addr_abs & 0xFF00) != (hi << 8):
            return 1
        else:
            return 0

    def REL(self) -> np.uint8:
        self.addr_rel = self.read(self.pc)
        self.pc += 1
        if self.addr_rel & 0x80: # if negative
            self.addr_rel |= 0xFF00
        return 0

    def ZP0(self) -> np.uint8:
        self.addr_abs = self.read(self.pc)
        self.pc += 1
        self.addr_abs &= 0x00FF
        return 0

    def ZPX(self) -> np.uint8:
        self.addr_abs = self.read(self.pc + self.x)
        self.pc += 1
        self.addr_abs &= 0x00FF
        return 0

    def ZPY(self) -> np.uint8:
        self.addr_abs = self.read(self.pc + self.y)
        self.pc += 1
        self.addr_abs &= 0x00FF
        return 0


    """
    Below are the operation functions
    """

    def ADC(self) -> np.uint8:
        self.fetch()
        self.temp = np.uint16(self.a) + np.uint16(self.fetched) + np.uint16(self.getFlag("C"))

        self.setFlag("C", self.temp > 255)
        self.setFlag("Z", (self.temp & 0x00FF) == 0)

        self.setFlag("V", (~(np.uint16(self.a) ^ np.uint16(self.fetched)) & (np.uint16(self.a) ^ np.uint16(self.temp))) & 0x0080)
        self.setFlag("N", self.temp & 0x80)

        self.a = self.temp & 0x00FF

        return 1

    def AND(self) -> np.uint8:
        self.fetch()

        self.a = self.a & self.fetched

        self.setFlag("Z", self.a == 0x00)
        self.setFlag("N", self.a & 0x80)

        return 1

    def ASL(self) -> np.uint8:
        self.fetch()
        self.temp = np.uint16(self.fetched) << 1
        self.setFlag("C", (self.temp & 0xFF00) > 0)
        self.setFlag("Z", (self.temp & 0xFF00) == 0x00)
        self.setFlag("N", self.temp & 0x80)

        if self.lookup[self.opcode]["addrmode"] == self.IMP:
            self.a = self.temp & 0x00FF
        else:
            self.write(self.addr_abs, self.temp & 0x00FF)
        
        return 0

    def BCC(self) -> np.uint8:
        if self.getFlag("C") == 0:
            self.cycles += 1
            self.addr_abs = self.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.pc & 0xFF00): #Check if jump page
                self.cycles += 1

            self.pc = self.addr_abs
        
        return 0

    def BCS(self) -> np.uint8:
        if self.getFlag("C") == 1:
            self.cycles += 1
            self.addr_abs = self.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.pc & 0xFF00): #Check if jump page
                self.cycles += 1

            self.pc = self.addr_abs
        
        return 0

    def BEQ(self) -> np.uint8:
        if self.getFlag("Z") == 1:
            self.cycles += 1
            self.addr_abs = self.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.pc & 0xFF00): #Check if jump page
                self.cycles += 1

            self.pc = self.addr_abs
        
        return 0

    def BIT(self) -> np.uint8:
        self.fetch()
        self.temp = self.a & self.fetched

        self.setFlag("Z", (self.temp & 0x00FF) == 0x00)
        self.setFlag("N", self.fetched & (1 << 7))
        self.setFlag("V", self.fetched & (1 << 6))

        return 0

    def BMI(self) -> np.uint8:
        if self.getFlag("N") == 1:
            self.cycles += 1
            self.addr_abs = self.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.pc & 0xFF00): #Check if jump page
                self.cycles += 1

            self.pc = self.addr_abs
        
        return 0

    def BNE(self) -> np.uint8:
        if self.getFlag("Z") == 0:
            self.cycles += 1
            self.addr_abs = self.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.pc & 0xFF00): #Check if jump page
                self.cycles += 1

            self.pc = self.addr_abs
        
        return 0

    def BPL(self) -> np.uint8:
        if self.getFlag("N") == 0:
            self.cycles += 1
            self.addr_abs = self.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.pc & 0xFF00): #Check if jump page
                self.cycles += 1

            self.pc = self.addr_abs
        
        return 0

    def BRK(self) -> np.uint8:
        self.pc += 1

        self.setFlag("I", 1)
        self.write(0x0100 + self.stkp, (self.pc << 8) & 0x00FF) # Writes high bits of pc

        self.stkp -= 1
        self.write(0x0100 + self.stkp, self.pc & 0x00FF) # Writes low bits of pc

        self.setFlag("B", 1)
        self.write(0x0100 + self.stkp, self.status)

        self.stkp -= 1

        self.setFlag("B", 0)

        self.pc = np.uint16(self.read(0xFFFE)) | (np.uint16(self.read(0xFFFF)) << 8) # Reads low and high bits for break pc 

        return 0

    def BVC(self) -> np.uint8:
        if self.getFlag("V") == 0:
            self.cycles += 1
            self.addr_abs = self.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.pc & 0xFF00): #Check if jump page
                self.cycles += 1

            self.pc = self.addr_abs
        
        return 0

    def BVS(self) -> np.uint8:
        if self.getFlag("V") == 1:
            self.cycles += 1
            self.addr_abs = self.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.pc & 0xFF00): #Check if jump page
                self.cycles += 1

            self.pc = self.addr_abs
        
        return 0

    def CLC(self) -> np.uint8:
        self.setFlag("C", 0)

    def CLD(self) -> np.uint8:
        self.setFlag("D", 0)

    def CLI(self) -> np.uint8:
        self.setFlag("I", 0)

    def CLV(self) -> np.uint8:
        self.setFlag("V", 0)

    def CMP(self) -> np.uint8:
        pass

    def CPX(self) -> np.uint8:
        pass

    def CPY(self) -> np.uint8:
        pass

    def DEC(self) -> np.uint8:
        pass

    def DEX(self) -> np.uint8:
        pass

    def DEY(self) -> np.uint8:
        pass

    def EOR(self) -> np.uint8:
        pass

    def INC(self) -> np.uint8:
        pass

    def INX(self) -> np.uint8:
        pass

    def INY(self) -> np.uint8:
        pass

    def JMP(self) -> np.uint8:
        pass

    def JSR(self) -> np.uint8:
        pass

    def LDA(self) -> np.uint8:
        pass

    def LDX(self) -> np.uint8:
        pass

    def LDY(self) -> np.uint8:
        pass

    def LSR(self) -> np.uint8:
        pass

    def NOP(self) -> np.uint8:
        pass

    def ORA(self) -> np.uint8:
        pass

    def PHA(self) -> np.uint8:
        pass

    def PHP(self) -> np.uint8:
        pass

    def PLA(self) -> np.uint8:
        pass

    def PLP(self) -> np.uint8:
        pass

    def ROL(self) -> np.uint8:
        pass

    def ROR(self) -> np.uint8:
        pass

    def RTI(self) -> np.uint8:
        pass

    def RTS(self) -> np.uint8:
        pass

    def SBC(self) -> np.uint8:
        self.fetch()

        value = np.uint16(self.fetched) ^ 0x00FF

        self.temp = np.uint16(self.a) + value + np.uint16(self.getFlag("C"))

        self.setFlag("C", self.temp & 0xFF00)
        self.setFlag("Z", (self.temp & 0x00FF) == 0)

        self.setFlag("V", (self.temp ^ np.uint16(self.a)) & (self.temp ^ value) &0x0080)
        self.setFlag("N", self.temp & 0x0080)

        self.a = self.temp & 0x00FF

        return 1

    def SEC(self) -> np.uint8:
        pass

    def SED(self) -> np.uint8:
        pass

    def SEI(self) -> np.uint8:
        pass

    def STA(self) -> np.uint8:
        pass

    def STX(self) -> np.uint8:
        pass

    def STY(self) -> np.uint8:
        pass

    def TAX(self) -> np.uint8:
        pass

    def TAY(self) -> np.uint8:
        pass

    def TSX(self) -> np.uint8:
        pass

    def TXA(self) -> np.uint8:
        pass

    def TXS(self) -> np.uint8:
        pass

    def TYA(self) -> np.uint8:
        pass

    def XXX(self) -> np.uint8:
        pass