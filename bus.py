from py6502 import Py6502
import numpy as np

class Bus:
    def __init__(self):
        self.cpu = Py6502()

        # Connects cpu to bus
        self.cpu.connectBus(self)

        # Makes and "connects" RAM
        self.ram = np.zeros(64*1024, dtype=np.uint8)


        

    def read(self, address: np.uint16) -> np.uint8:
        if address >= 0x0000 and address <= 0xFFFF:
            return self.ram[address]
        else:
            return 0x00

    def write(self, address: np.uint16, data: np.uint8):
        if address >= 0x0000 and address <= 0xFFFF:
            self.ram[address] = np.uint8(data)


    



if __name__ == "__main__":
    bus = Bus()

    s = "A2 0A 8E 00 00 A2 03 8E 01 00 AC 00 00 A9 00 18 6D 01 00 88 D0 FA 8D 02 00 EA EA EA".split()
    offset = 0x8000

    for val in s:
        
        bus.ram[offset] = int(val, 16)
        offset += 1

    bus.ram[0xFFFC] = 0x00
    bus.ram[0xFFFD] = 0x80
    bus.cpu.reset()

    

    while(bus.cpu.pc != 0):
        print("pc: ",hex(bus.cpu.pc), "op: ", hex(bus.ram[bus.cpu.pc]), "ram 0:", hex(int(bus.ram[0])), "ram 1:", hex(int(bus.ram[1])), "a: ",hex(bus.cpu.a),"x: ", hex(bus.cpu.x), "y: ", hex(bus.cpu.y))
        while(True):
            
        
            bus.cpu.clock()
            if bus.cpu.complete():
                break

    print("10*3 = ",bus.ram[2])

    


        