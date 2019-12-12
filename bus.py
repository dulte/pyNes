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


    



if __name__=="__main__":
    bus = Bus()
    
    bus.ram[4] = 0x0A

    bus.cpu.addr_abs = 2
    bus.cpu.opcode = 0

    print(bus.cpu.fetch())
    


        