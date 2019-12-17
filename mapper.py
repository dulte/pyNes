import numpy as np

class Mapper:

    def __init__(self, prgBanks: np.uint8, chrBanks: np.uint8):
        self.nRPGBanks = 0
        self.nCHRBanks = 0

    """
    Virtuel Functions for reading and writing
    """
    def cpuMapRead(self, addr: np.uint16, mapped_addr: np.uint32) -> [bool,np.uint32] :
        return None

    def cpuMapWrite(self, addr: np.uint16, mapped_addr: np.uint32) -> [bool,np.uint32]:
        return None

    def ppuMapRead(self, addr: np.uint16, mapped_addr: np.uint32) -> [bool,np.uint32]:
        return None

    def ppuMapWrite(self, addr: np.uint16, mapped_addr: np.uint32) -> [bool,np.uint32]:
        return None