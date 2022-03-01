import sys
import collections
import os.path

bsb = "BACKKING_STORE.bin"
valid = ["FIFO", "LRU", "OPT"]


class page:
    def __init__(self, pNum, frame):
        self.pNum = pNum
        self.frame = frame

class TLB:
    def __init__(self, page, frame):
        self.page = page
        self.frame = frame

class physicalMemory:
    def __init__(self, fNum):
        self.fNum = fNum
        # self.frames

class FIFO:
    def __init__(self, ):
        pass


class OPT:
    def __init__(self) -> None:
        pass


class LRU:
    def __init__(self, fNum):
        self.fNum = fNum
        self.pages = []

    def get(self, page):



def main():
    if os.path.isfile(bsb) == False:
        print("BACKING_STORE.bin is missing")
        sys.exit()
    
    if (len(sys.argv)) < 4 or (len(sys.argv)) > 4:
        print("Order must be as follows")
        print("Input: python3 memSim <reference-sequence-file.txt> <FRAMES> <PRA>")
        print("Use FRAMES = 256 and PRA = FIFO for default settings")
        sys.exit()

    inputFile = sys.argv[1]
    frames = sys.argv[2]
    pra = sys.argv[3]
    




if __name__ == "__main__":
    main()