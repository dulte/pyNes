import numpy as np
from mapper import Mapper

class Mapper_0000(Mapper):

    def __init__(self, prgBanks: np.uint8, chrBanks: np.uint8):
        Mapper.__init__(self,prgBanks, chrBanks)

    """
    Functions for reading and writing
    """
    def cpuMapRead(self, addr: np.uint16, mapped_addr: np.uint32) -> [bool,np.uint32]:
        if addr >= 0x8000 and addr <= 0xFFFF:
            mapped_addr = addr & (0x7FFF if self.nRPGBanks > 1 else 0x3FFF)
            return True, mapped_addr
        else:
            return False, 0

    def cpuMapWrite(self, addr: np.uint16, mapped_addr: np.uint32) -> [bool,np.uint32]:
        if addr >= 0x8000 and addr <= 0xFFFF:
            mapped_addr = addr & (0x7FFF if self.nRPGBanks > 1 else 0x3FFF)
            return True, mapped_addr
        else:
            return False, 0

    def ppuMapRead(self, addr: np.uint16, mapped_addr: np.uint32) -> [bool,np.uint32]:
        if addr >= 0x0000 and addr <= 0x1FFF:
            mapped_addr = addr 
            return True, mapped_addr
        else:
            return False, 0

    def ppuMapWrite(self, addr: np.uint16, mapped_addr: np.uint32) -> [bool,np.uint32]:
        if addr >= 0x0000 and addr <= 0x1FFF:
            mapped_addr = addr 
            return True, mapped_addr
        else:
            return False, 0