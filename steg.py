import sys
import argparse

global SENTINEL
SENTINEL = bytearray([0, 255, 0, 0, 255, 0])

OP = ''
MODE = ''
OFFSET = 1024
INTERVAL = 1
WRAPPER = bytearray()
HIDDEN = bytearray()
DEBUG = True
KEYWORD = "panda"

def writeBit(wrapper: bytearray, hidden: bytearray, offset: int, out: str):

    global KEYWORD

    for i in range(0,len(hidden)+len(SENTINEL)):
        KEYWORD += KEYWORD[i%len(KEYWORD)]

    for i in range(0,len(hidden)):
        offset += ord(KEYWORD[i])
        for j in range(0,8):
            wrapper[offset] &= 0b11111110
            wrapper[offset] |= ((hidden[i] & 0b10000000) >> 7)
            hidden[i] = (hidden[i] << 1) & (2 ** 8 - 1)
            offset += 1

    for i in range(0,len(SENTINEL)):
        for j in range(0,8):
            wrapper[offset] &= 0b11111110
            wrapper[offset] |= ((SENTINEL[i]  & 0b10000000) >> 7)
            SENTINEL[i] = (SENTINEL[i] << 1) & (2 ** 8 - 1)
            offset += 1

    f = open(out, "wb")
    f.write(wrapper)
            
def getBit(wrapper, offset, interval):

    hidden = bytearray()
    sent = bytearray()
    i = 0
    
    while (offset < len(wrapper)):
        b = 0
        for j in range(0,8):
            b |= (wrapper[offset] & 0b00000001)
            if (j < 7):
                b = (b << 1) & (2 ** 8 - 1)
                offset += interval
                
        if(b == SENTINEL[i]):
            sent.append(b)
            hidden.append(b)
            i += 1
            if(sent == SENTINEL):
                sys.stdout.buffer.write(hidden[:len(hidden)-len(sent)])
                exit(0)
        else:
            sent = bytearray()
            hidden.append(b)
            i = 0

        offset += interval
        

#########################################################################
if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("-s", action="store_true")
    parse.add_argument("-r", action="store_true")
    parse.add_argument("-w", type=str, default="wrapper.jpg")
    parse.add_argument("-m", type=str, default="message.txt")
    parse.add_argument("-o", type=str, default="test.jpg")

    args = parse.parse_args()

    if args.s:
        WRAPPER += open(args.w, "rb").read()
        HIDDEN += open(args.m, "rb").read()
        out = args.o
        writeBit(WRAPPER, HIDDEN, OFFSET, out)

    elif args.r:
        WRAPPER += open(args.w, "rb").read()
        getBit(WRAPPER, OFFSET, INTERVAL)

