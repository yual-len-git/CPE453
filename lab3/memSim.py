import sys
import os.path

bsb = "BACKING_STORE.bin"
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
    def __init__(self):
        pass

    def get(self):
        pass

    def set(self):
        pass


class OPT:
    def __init__(self, fNum):
        self.fNum = fNum
        
    def get(self):
        pass

    def set(self):
        pass

    def pop(self):
        pass

    def priority(self, input):
        pass

    def calculate(self):
        pass


class LRU:
    def __init__(self, fNum):
        self.fNum = fNum
        self.pages = []

    def get(self, page):
        pass

    def set(self, frame):
        pass

def setup():
    addresses = []
    frames = 256
    pra = "FIFO"

    if os.path.isfile(bsb) == False:
        print("BACKING_STORE.bin is missing")
        sys.exit()
    if (len(sys.argv)) < 2:
        print("Order must be as follows")
        print("Input: python3 memSim <reference-sequence-file.txt> <FRAMES> <PRA>")
        print("FRAMES = 256 and PRA = FIFO for default settings")
        sys.exit()
    if (len(sys.argv)) >= 3:
        try:
            if int(sys.argv[2]) < 0 or int(sys.argv[2]) > 256:
                frames = 256
            else:
                frames = int(sys.argv[2])
        except:
            print("Not valid integer default frames 256")
    if (len(sys.argv)) >= 4:
        if sys.argv[3] in valid:
            pra = sys.argv[3]

    inputFile = open(sys.argv[1], "r")
    for line in inputFile:
        print(line)
        addresses.append(int(line))
    inputFile.close()

    return addresses, frames, pra


def main():
    addresses, frames, pra = setup()
     









    print(addresses)
    print(frames)
    print(pra)
    


if __name__ == "__main__":
    main()