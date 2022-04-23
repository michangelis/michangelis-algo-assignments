import hashlib
import math
import sys

input = []
name = sys.argv
with open(name[1]) as f:
    for line in f:
        input.append(int(line))

l = int(math.log2(input[len(input)-1] / len(input)))
u = int(math.log2(input[len(input)-1])-l)
sizeU = int(len(input) + input[len(input)-1]/math.pow(2,l))

def extractbits(num, k, pos):
    return (((1<<k)-1) & (num>>(pos-1)))

def createL() :
    L = bytearray()
    i = 0
    count = 1
    for x in input:
        j = 0
        while j < l:
            bit = extractbits(x, 1, l-j)
            if count == 1:
                L.append(bit)
                count += 1
            else:
                if count >= 2:
                    L[i] = L[i] << 1
                    L[i] = L[i] | bit
                    count += 1
                    if count > 8:
                        count = 1
                        i += 1
            j += 1
    if count >1 & count < 8:
        L[i] = L[i] << 8-count+1
    return L

def insertbits(U, count, j, b):
    a = 1 << 8 - count
    if b:
        U.append(a)
    else:
        U[j] = U[j] | a

def createU() :
    U = bytearray()
    i = 0
    prev = 0
    count = 0
    b = True
    j = 0
    while i < len(input):
        bit = extractbits(input[i], u+1, l+1)
        diff = bit-prev
        prev = bit
        if count == 0:
            b = True
        else:
            b = False
        count += diff + 1
        if count > 8:
            count = count - 8
            b = True
            j += 1
        insertbits(U, count, j, b)
        i += 1
    return U

if __name__ == '__main__':
    L = createL()
    U = createU()
    print('l ' + str(l))
    print('L')
    for x in L:
        print("{0:08b}".format(x))
    print('U')
    for x in U:
        print("{0:08b}".format(x))
    m = hashlib.sha256()
    m.update(L)
    m.update(U)
    digest = m.hexdigest()
    print(digest)


