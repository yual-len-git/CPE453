import binascii
import sys
import os.path

bsb = "BACKING_STORE.bin"
valid = ["FIFO", "LRU", "OPT"]


class Page:
    def __init__(self, pNum, fNum, frame):
        self.pNum = pNum
        self.fNum = fNum
        self.frame = frame

class TLB:
    def __init__(self, page, frame):
        self.page = page
        self.frame = frame

class memoryTable:
    def __init__(self, addresses, frames, pra):
        self.addresses = addresses
        self.frames = frames
        self.pra = pra
        self.memory = [None] * frames
        self.hits = 0
        self.misses = 0
        self.pFaults = 0
        self.pHits = 0
        self.pageNum = 0
        self.count = 0
        self.tlb = FIFO(16)
        self.tHits = 0
        self.tMisses = 0
        # if pra == "LRU":
        #     self.pageTable = LRU(frames)
        # elif pra == "OPT":
        #     pageTable = OPT(frames, addresses)
        # else:
        self.pageTable = FIFO(frames)

class FIFO:
    def __init__(self, fNum):
        self.fNum = fNum
        self.pages = []

    def get(self, pNum):                #searches through pages for page number
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

    def get(self, pNum):                 #searches for page if it exists moves it bottom 
        for page in self.pages:
            if pNum == page.pNum:
                page.pop(page.index(pNum))
                page.insert(0, pNum)
                return page
        return page
        
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

def pageFault(ptable, pNum):
    ptable.pFaults += 1
    frame = readBin(pNum)
    page = Page(pNum, ptable.pageNum, frame)
    ptable.pageTable.set(page)
    ptable.tlb.set(page)
    ptable.pageNum += 1
    return ptable.pageNum

def simulate(ptable, address):
    pNum = address >> 8
    # print(pNum)
    offset = address & 0xFF
    page = ptable.tlb.get(pNum)
    try:
        page.frame != ptable.memory[page.fNum]
    except AttributeError:
        page = None
    if page == None:
        ptable.tMisses += 1
        page = ptable.pageTable.get(pNum)
        if page == None:
            pFault = pageFault(ptable, pNum)
            page = ptable.pageTable.get(pNum)
        else:
            ptable.pHits += 1
            ptable.tlb.set(page)
    else:
        ptable.pHits += 1
        ptable.tHits += 1

    data = page.frame[offset]
    if data > 127:
        data -= 256
    # print(ptable.pFaults, ptable.tMisses)
    printdata(address, data, page.fNum, page.frame)
    ptable.count += 1


def printdata(address, data, pNum, frame):
    print("%d, %s, %d" % (address, data, pNum))
    print("%s" % binascii.hexlify(frame).upper())

def printStats(ptable):
    print("Number of Translated Address = %d" % (ptable.pHits + ptable.pFaults))
    print("Page Faults = %d" % (ptable.pFaults))
    print("Page Fault Rate = %3.3f" % (ptable.pFaults / (ptable.pFaults + ptable.pHits)))
    print("TLB Hits = %d" % ptable.pHits)
    print("TLB Misses = %d" % ptable.tMisses)
    print("TLB Hit Rate = %3.3f" % (ptable.pHits / (ptable.tHits + ptable.tMisses)))

def main():
    addresses = getAddress()
    frames = getFrames()
    pra = getPRA()
    pt = memoryTable(addresses, frames, pra)
    for address in addresses:
        simulate(pt, address)
    printStats(pt)



if __name__ == "__main__":
    main()