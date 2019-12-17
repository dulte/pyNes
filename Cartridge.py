import numpy as np
from mapper_0000 import Mapper_0000


class Cartridge:

    def __init__(self, name: str):
        # Variables for values about the cartridge
        self.bImageValid = False
        self.nMapperID = np.uint8(0)
        self.nPRGBanks = np.uint8(0)
        self.nCHRBanks = np.uint8(0)

        self.mirror = "horizontal"

        # Variable for holding the Mapper class
        self.mapper = None

        # Arrys holding the cartrige memories
        self.vPRGMemory = []
        self.vCHRMemory = []

        # Call function for reading cartridge
        self.readCartridge(name)
        

    """
    Function for reading the cartridge from file
    """
    
    def readCartridge(self, name: str):
        loaded = np.fromfile(name,dtype='uint8')
        read_from = 0
        self.name = loaded[read_from:4]
        read_from = 4

        self.prg_rom_chunks = loaded[read_from]
        read_from += 1
        self.chr_rom_chunks = loaded[read_from]
        read_from += 1
        self.mapper1 = loaded[read_from]
        read_from += 1
        self.mapper2 = loaded[read_from]
        read_from += 1
        self.prg_ram_size = loaded[read_from]
        read_from += 1
        self.tv_system1 = loaded[read_from]
        read_from += 1
        self.tv_system2 = loaded[read_from]
        read_from += 1
        read_from += 5

        # IF there is a trainer:
        if self.mapper1 & 0x04:
            read_from += 512

        self.nMapperID = ((self.mapper2 >> 4) << 4) | (self.mapper1 >> 4)

        self.mirror = "vertical" if (self.mapper1 & 0x01) else "horizontal"

        nFileType = 1

        if nFileType == 0:
            pass
        
        if nFileType == 1:
            self.nPRGBanks = self.chr_rom_chunks
            self.vPRGMemory = loaded[read_from:read_from+16384]
            read_from += 16384

            self.nCHRBanks = self.chr_rom_chunks
            self.vCHRMemory = loaded[read_from:read_from+8192]
            read_from += 8129

        if nFileType == 2:
            pass

        if self.nMapperID == 0:
            self.mapper = Mapper_0000(self.nPRGBanks, self.nCHRBanks)

        
        self.bImageValid = True

        

    """
    Function for checking the validity of the cart
    """
    def imageValid(self) -> bool:
        return self.bImageValid

    """
    Functions for reading and writing
    """

    def cpuRead(self, addr: np.uint16) -> [bool, np.uint8]:
        mapped_addr = 0
        is_mapped, mapped_addr = self.mapper.cpuMapRead(addr, mapped_addr)
        if is_mapped:
            data = self.vPRGMemory[mapped_addr]
            return True, data
        else:
            return False, 0
            

    def cpuWrite(self, addr: np.uint16, data: np.uint8) -> bool:
        mapped_addr = 0
        is_mapped, mapped_addr = self.mapper.cpuMapWrite(addr, mapped_addr)
        if is_mapped:
            self.vPRGMemory[mapped_addr] = data
            return True
        else:
            return False

    
    def ppuRead(self, addr: np.uint16) -> [bool, np.uint8]:
        mapped_addr = 0
        is_mapped, mapped_addr = self.mapper.ppuMapRead(addr, mapped_addr)
        if is_mapped:
            data = self.vCHRMemory[mapped_addr]
            return True, data
        else:
            return False, 0
            

    def ppuWrite(self, addr: np.uint16, data: np.uint8) -> bool:
        mapped_addr = 0
        is_mapped, mapped_addr = self.mapper.ppuMapWrite(addr, mapped_addr)
        if is_mapped:
            self.vCHRMemory[mapped_addr] = data
            return True
        else:
            return False

        



if __name__ == "__main__":
    cart = Cartridge("../branch_timing_tests/1.Branch_Basics.nes")

