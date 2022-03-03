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
    def __init__(self, fNum):
        self.fNum = fNum
        self.pages = []

    def get(self, pNum):
        for page in self.pages:
            if page.pNum == pNum:
                return page
        return None

    def set(self, frame):
        page = None
        if len(self.pages) == self.fNum:
            page = self.pages.pop()
        self.pages.insert(0, frame)
        return page



class LRU:
    def __init__(self, fNum):
        self.fNum = fNum
        self.pages = []

    def get(self, page):
        pass

    def set(self, frame):
        pass


# class OPT:
#     def __init__(self, fNum):
#         self.fNum = fNum
        
#     def get(self):
#         pass

#     def set(self):
#         pass

#     def pop(self):
#         pass


def getAddress():
    addresses = []

    if os.path.isfile(bsb) == False:
        print("BACKING_STORE.bin is missing")
        sys.exit()
    if (len(sys.argv)) < 2:
        print("Order must be as follows")
        print("Input: python3 memSim <reference-sequence-file.txt> <FRAMES> <PRA>")
        print("FRAMES = 256 and PRA = FIFO for default settings")
        sys.exit()
    inputFile = open(sys.argv[1], "r")
    for line in inputFile:
        addresses.append(int(line))
    inputFile.close()

    return addresses

def getFrames():
    frames = 256
    if (len(sys.argv)) >= 3:
        try:
            if int(sys.argv[2]) < 0 or int(sys.argv[2]) > 256:
                frames = 256
            else:
                frames = int(sys.argv[2])
        except:
            print("Not valid integer default frames 256")
    return frames

def getPRA():
    pra = 'FIFO'
    if (len(sys.argv)) >= 4:
        if sys.argv[3] in valid:
            pra = sys.argv[3]
    return pra

def readBin(frames):
    file = open("BACKING_STORE.bin", "rb")
    size = 256
    file.seek(size * frames)
    return file.read(size)

def main():
    addresses = getAddress()
    frames = getFrames()
    pra = getPRA()
    memory = [None] * frames
    hits = 0
    misses = 0
    pFaults = 0
    phits = 0
    pageNum = 0
    count = 0
    tlb = FIFO(16)

    if pra == "LRU":
        page_table = LRU(frames)
    # elif pra == "OPT":
    #     page_table = OPT(frames, addresses)
    else:
        page_table = FIFO(frames)    
        






    print(addresses)
    print(frames)
    print(pra)
    


if __name__ == "__main__":
    main()