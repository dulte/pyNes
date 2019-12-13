from py6502 import Py6502
import numpy as np

class Bus:
    def __init__(self):
        self.cpu = Py6502()

        # Connects cpu to bus
        self.cpu.connectBus(self)

        # Makes and "connects" RAM
        self.cpuRam = np.zeros(2048, dtype=np.uint8)

        # Creates the ppu
        self.ppu = None

        # Creates the cartridge
        self.cart = None

        # Varibles for time
        self.nSystemClockCounter = 0



    """
    Function for the cpu to read/write
    """  

    def cpuRead(self, address: np.uint16) -> np.uint8:
        data = np.uint8(0)
        if address >= 0x0000 and address <= 0x1FFF:
            data = self.cpuRam[address & 0x07FF]
        elif address >= 0x2000 and address <= 0x3FFF:
            data = self.ppu.cpuRead(address & 0x0007)
        
        return data

    def cpuWrite(self, address: np.uint16, data: np.uint8):

        if address >= 0x0000 and address <= 0x1FFF:
            self.cpuRam[address & 0x07FF] = np.uint8(data)
        
        elif (address >= 0x2000 and address <= 0x3FFF):
            self.ppu.cpuWrite(address & 0x0007, np.uint8(data))


    """
    Function for inserting Cartridge
    """

    def insertCartridge(self, cart):
        self.cart = cart
        ppu.ConnectCartridge(cart)

    
    """
    Functions for reseting and CLOCK
    """
    def reset(self):
        self.cpu.reset()

        self.nSystemClockCounter = 0

    def clock(self):
        self.ppu.clock()

        if (self.nSystemClockCounter % 3 == 0):
            self.cpu.clock()

        self.nSystemClockCounter += 1


    """
    Functions for test program
    """
    def load_test(self):
        s = "A2 0A 8E 00 00 A2 03 8E 01 00 AC 00 00 A9 00 18 6D 01 00 88 D0 FA 8D 02 00 EA EA EA".split()
        offset = 0x0100

        for val in s:
            
            self.cpuRam[offset & 0x07FF] = int(val, 16)
            offset += 1

        self.cpuRam[0xFFFC & 0x07FF] = 0x00
        self.cpuRam[0xFFFD & 0x07FF] = 0x0100
        self.cpu.reset()

        self.cpu.pc = 0x0100
        
        asm = self.cpu.disassemble(0x0000, 0x0200)
        return asm

    def step_test(self):
        while(True):
 
            self.cpu.clock()
            if self.cpu.complete():
                break




    





























if __name__ == "__main__":
    bus = Bus()

    

    
    
    while(bus.cpu.pc != 0):
        print("pc: ",hex(bus.cpu.pc), "op: ", hex(bus.cpuRam[bus.cpu.pc]), "ram 0:", hex(int(bus.cpuRam[0])), "ram 1:", hex(int(bus.cpuRam[1])), "a: ",hex(bus.cpu.a),"x: ", hex(bus.cpu.x), "y: ", hex(bus.cpu.y))
        

    print("10*3 = ",bus.cpuRam[2])

    


        