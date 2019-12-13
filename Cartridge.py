import numpy as np

class Cartridge:

    def __init__(self, name: str):

        loaded = np.fromfile(name,dtype='uint8')

        print(loaded[:10])
        for i in loaded[:4]:
            print(chr(i))





if __name__ == "__main__":
    cart = Cartridge("../branch_timing_tests/1.Branch_Basics.nes")

