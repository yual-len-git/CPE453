import sys

file = open("BACKING_STORE.bin", 'rb')

for line in file:
    print(line)
    sys.exit()


