import numpy as np

class Py2C02:

    def __init__(self):
        # Variables for the screen and sprites
        self.palScreen = [0]*0x40
        self.sprScreen = np.zeros((256, 240, 3), dtype=np.uint8)
        self.sprNameTable = [np.zeros((256, 240, 3), dtype=np.uint8),np.zeros((256, 240, 3), dtype=np.uint8)]
        self.sprPatternTable = [np.zeros((128,128, 3), dtype=np.uint8),np.zeros((128,128, 3), dtype=np.uint8)]

        self.tblName = np.zeros((2,1024), dtype=np.uint8)
        self.tblPattern = np.zeros((2,1024), dtype=np.uint8)
        self.tblPalette = np.zeros(32, dtype=np.uint8)

        #Variables for the scanning of the screen
        self.scanline = 0
        self.cycle = 0
        self.frame_complete = False

        #Variable for holding the cartridge
        self.cart = None

        # Makes palScreen
        self.setpalScreen()

    """
    Function for filling the array holding the different pixel values
    """
    def setpalScreen(self):
        self.palScreen[0x00] = np.array([84, 84, 84])
        self.palScreen[0x01] = np.array([0, 30, 116])
        self.palScreen[0x02] = np.array([8, 16, 144])
        self.palScreen[0x03] = np.array([48, 0, 136])
        self.palScreen[0x04] = np.array([68, 0, 100])
        self.palScreen[0x05] = np.array([92, 0, 48])
        self.palScreen[0x06] = np.array([84, 4, 0])
        self.palScreen[0x07] = np.array([60, 24, 0])
        self.palScreen[0x08] = np.array([32, 42, 0])
        self.palScreen[0x09] = np.array([8, 58, 0])
        self.palScreen[0x0A] = np.array([0, 64, 0])
        self.palScreen[0x0B] = np.array([0, 60, 0])
        self.palScreen[0x0C] = np.array([0, 50, 60])
        self.palScreen[0x0D] = np.array([0, 0, 0])
        self.palScreen[0x0E] = np.array([0, 0, 0])
        self.palScreen[0x0F] = np.array([0, 0, 0])

        self.palScreen[0x10] = np.array([152, 150, 152])
        self.palScreen[0x11] = np.array([8, 76, 196])
        self.palScreen[0x12] = np.array([48, 50, 236])
        self.palScreen[0x13] = np.array([92, 30, 228])
        self.palScreen[0x14] = np.array([136, 20, 176])
        self.palScreen[0x15] = np.array([160, 20, 100])
        self.palScreen[0x16] = np.array([152, 34, 32])
        self.palScreen[0x17] = np.array([120, 60, 0])
        self.palScreen[0x18] = np.array([84, 90, 0])
        self.palScreen[0x19] = np.array([40, 114, 0])
        self.palScreen[0x1A] = np.array([8, 124, 0])
        self.palScreen[0x1B] = np.array([0, 118, 40])
        self.palScreen[0x1C] = np.array([0, 102, 120])
        self.palScreen[0x1D] = np.array([0, 0, 0])
        self.palScreen[0x1E] = np.array([0, 0, 0])
        self.palScreen[0x1F] = np.array([0, 0, 0])

        self.palScreen[0x20] = np.array([236, 238, 236])
        self.palScreen[0x21] = np.array([76, 154, 236])
        self.palScreen[0x22] = np.array([120, 124, 236])
        self.palScreen[0x23] = np.array([176, 98, 236])
        self.palScreen[0x24] = np.array([228, 84, 236])
        self.palScreen[0x25] = np.array([236, 88, 180])
        self.palScreen[0x26] = np.array([236, 106, 100])
        self.palScreen[0x27] = np.array([212, 136, 32])
        self.palScreen[0x28] = np.array([160, 170, 0])
        self.palScreen[0x29] = np.array([116, 196, 0])
        self.palScreen[0x2A] = np.array([76, 208, 32])
        self.palScreen[0x2B] = np.array([56, 204, 108])
        self.palScreen[0x2C] = np.array([56, 180, 204])
        self.palScreen[0x2D] = np.array([60, 60, 60])
        self.palScreen[0x2E] = np.array([0, 0, 0])
        self.palScreen[0x2F] = np.array([0, 0, 0])

        self.palScreen[0x30] = np.array([236, 238, 236])
        self.palScreen[0x31] = np.array([168, 204, 236])
        self.palScreen[0x32] = np.array([188, 188, 236])
        self.palScreen[0x33] = np.array([212, 178, 236])
        self.palScreen[0x34] = np.array([236, 174, 236])
        self.palScreen[0x35] = np.array([236, 174, 212])
        self.palScreen[0x36] = np.array([236, 180, 176])
        self.palScreen[0x37] = np.array([228, 196, 144])
        self.palScreen[0x38] = np.array([204, 210, 120])
        self.palScreen[0x39] = np.array([180, 222, 120])
        self.palScreen[0x3A] = np.array([168, 226, 144])
        self.palScreen[0x3B] = np.array([152, 226, 180])
        self.palScreen[0x3C] = np.array([160, 214, 228])
        self.palScreen[0x3D] = np.array([160, 162, 160])
        self.palScreen[0x3E] = np.array([0, 0, 0])
        self.palScreen[0x3F] = np.array([0, 0, 0])

    """
    Functions for returning screen properties
    """

    def GetScreen(self) -> np.zeros((256, 240, 3), dtype=np.uint8):
        return self.sprScreen

    def GetNameTable(self, i: np.uint8) -> np.zeros((256, 240, 3), dtype=np.uint8):
        return self.sprNameTable[i]
    
    def GetPatternTable(self, i: np.uint8) -> np.zeros((256, 240, 3), dtype=np.uint8):
        return self.sprPatternTable[i]

    """
    Functions for reading and writing
    """

    def cpuRead(self, addr: np.uint16) -> np.uint8:
        data = 0x00
        if addr == 0x0000: #Control
            pass
        elif addr == 0x0001: # Mask
            pass
        elif addr == 0x0002: # Status
            pass
        elif addr == 0x0003: # OAM Address
            pass
        elif addr == 0x0004: # OAM Data
            pass
        elif addr == 0x0005: # Scroll
            pass
        elif addr == 0x0006: # PPU Address
            pass
        elif addr == 0x0007: # PPU Data
            pass

        return data

    def cpuWrite(self, addr: np.uint16, data: np.uint8):
        
        if addr == 0x0000: #Control
            pass
        elif addr == 0x0001: # Mask
            pass
        elif addr == 0x0002: # Status
            pass
        elif addr == 0x0003: # OAM Address
            pass
        elif addr == 0x0004: # OAM Data
            pass
        elif addr == 0x0005: # Scroll
            pass
        elif addr == 0x0006: # PPU Address
            pass
        elif addr == 0x0007: # PPU Data
            pass

    def ppuRead(self, addr: np.uint16) -> np.uint8:
        data = 0x00

        addr &= 0x3FFF

        if self.cart.ppuRead(addr, data):
            pass

        return data

    def ppuWrite(self, addr: np.uint16, data: np.uint8):
        addr &= 0x3FFF

        if self.cart.ppuWrite(addr, data):
            pass


    """
    Function for connecting the cartridge
    """
    def connectCartridge(self, cart):
        self.cart = cart

    """
    Clock Function
    """
    def clock(self):
        try:
            self.sprScreen[self.cycle-1, self.scanline, :] = self.palScreen[np.random.choice([0x3F,0x30])]
        except:
            pass
        
        self.cycle += 1

        if self.cycle >= 341:

            self.cycle = 0

            self.scanline += 1

            if self.scanline >= 261:
                self.scanline = -1
                self.frame_complete = True

            


        