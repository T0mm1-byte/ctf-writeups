# eXORbitant

CTF: L3akCTF 2024(Jeopardy)

Category: hardware

Authors: Suvoni

## Description
What is this circuit doing to the flag?

## Overview
This challenge is composed by a .circ file and a .png file.

The .circ file shows a digital circuit that takes the flag as input and encrypts it using 16 Xor ports.

The .png file shows the result of the encryption in the memory.

## Solution
Looking at the circuit we can see that the flag is divided in hextet and each bit of each hextet is used by multiple xor ports.

Each xor port produces a bit of the encrypted hextet.

We have to find, for each encrypted hextet, which hextet makes it using that scheme.

## Exploit
Since a hextet is just 2 bytes there are only 2^16 possible configuration and we can find the correct one by bruteforce.

After getting all the correct hextet we can simply translate each byte in ascii and see the flag.

```python
def HextetToChar(hextet):
    first_byte = (hextet >> 8) & 0xff
    second_byte = hextet & 0xff
    return chr(first_byte) + chr(second_byte)


def Xor(hextet, pos):
    to_consider = ""
    for p in pos:
        to_consider += hextet[p]
    return to_consider.count('1') % 2


def RevXor(val):
    XOR_INDICES = [[15, 13, 10, 9, 7, 6, 5, 2, 1],                
                   [15, 14, 9, 3, 2, 1],                          
                   [14, 13, 12, 11, 10, 9, 7, 5, 4, 3, 1],        
                   [15, 14, 13, 12, 11, 8, 6, 5, 4, 3],           
                   [12, 11, 10, 6, 5, 2, 1],                   
                   [15, 11, 9, 6, 3, 0],                          
                   [14, 10, 9, 8, 7, 5, 4, 1, 0],                 
                   [11, 10, 9, 8, 7, 6, 4, 2, 0],                 
                   [15, 14, 12, 11, 9, 8, 7, 6, 5, 4, 2, 0],      
                   [15, 13, 12, 10, 9, 8, 6, 5, 1, 0],            
                   [11, 10, 7, 2],                                
                   [14, 7, 6, 3],                                 
                   [15, 14, 13, 12, 11, 10, 9, 8, 5, 4, 3, 0], 
                   [15, 13, 7, 5, 3, 2, 1, 0],                    
                   [15, 14, 11, 9, 7, 6, 5, 4, 1, 0],             
                   [14, 13, 12, 11, 9, 7, 5, 4, 3, 2]]
    bin_val = (bin(val)[2:].zfill(16))
    for x in range(2**16):
        bin_x = (bin(x)[2:].zfill(16))[::-1]
        cond = True
        cond &= (Xor(bin_x, XOR_INDICES[0]) == int(bin_val[0]))
        cond &= (Xor(bin_x, XOR_INDICES[1]) == int(bin_val[1]))
        cond &= (Xor(bin_x, XOR_INDICES[2]) == int(bin_val[2]))
        cond &= (Xor(bin_x, XOR_INDICES[3]) == int(bin_val[3]))
        cond &= (Xor(bin_x, XOR_INDICES[4]) == int(bin_val[4]))
        cond &= (Xor(bin_x, XOR_INDICES[5]) == int(bin_val[5]))
        cond &= (Xor(bin_x, XOR_INDICES[6]) == int(bin_val[6]))
        cond &= (Xor(bin_x, XOR_INDICES[7]) == int(bin_val[7]))
        cond &= (Xor(bin_x, XOR_INDICES[8]) == int(bin_val[8]))
        cond &= (Xor(bin_x, XOR_INDICES[9]) == int(bin_val[9]))
        cond &= (Xor(bin_x, XOR_INDICES[10]) == int(bin_val[10]))
        cond &= (Xor(bin_x, XOR_INDICES[11]) == int(bin_val[11]))
        cond &= (Xor(bin_x, XOR_INDICES[12]) == int(bin_val[12]))
        cond &= (Xor(bin_x, XOR_INDICES[13]) == int(bin_val[13]))
        cond &= (Xor(bin_x, XOR_INDICES[14]) == int(bin_val[14]))
        cond &= (Xor(bin_x, XOR_INDICES[15]) == int(bin_val[15]))
        if cond:
            return HextetToChar(x)


Nums = [0x8094, 0x6514, 0xe9f3, 0xcc9b, 0xa618, 0xf075, 0xeae8, 0x30db, 0x899f, 0x6c8d, 0x4bf2, 0x34eb, 0x30db, 0xb53a, 0xc777, 0xd65]
flag = ""
for n in Nums:
    flag += RevXor(n)
print(flag)

```
This will print the flag *L3AK{X0R_1s_EaS1lY_R3vErS1BLe!!}*
