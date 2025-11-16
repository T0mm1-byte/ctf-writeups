# VHDLCG(crypto)

CTF: L3akCTF 2024(Jeopardy)

Category: hardware

Authors: Suvoni

## Description
VHDL: Very Happy Digital Leprechauns

Imagine a world where all digital logic and circuits are maintained by cheerful, tiny leprechauns who take great joy in ensuring that your hardware designs work flawlessly. They busily manage all the gates, flip-flops, and signals, always with a smile on their tiny faces!

## Overview
This challenge is composed by two .vhdl files and one .txt file. 
prng.vhdl is the description of a module that, as the name suggest, produces pseudo random numbers.
encrypt.vhdl is the description of the main module that encrypts the flag.
output.txt is the result of the encryption.

## Solution
Let's start with prng.vhdl. This module takes as input the signals clock, enable, reset and a seed made of 28 bits. It has as a byte as output.
When reset is high it sets his own 28 bit register prng_reg with the input seed. 
When reset is low and enable is high, on clock's posedges, it calculate a new 28 bits value that stores in prng_reg and sends as output its 8 most significant bits.
The module uses a linear congruential generator (as the challenge's name suggest) to change prng_reg and we know all the parameters used.
Let's analyze encrypt.vhdl now. This module reads the seed and the flag, uses the seed to generate a byte for each char of the flag, xors each byte got from prng.vhdl with a char and writes the result in output.txt.
It first sets reset high to let prng.vhdl store the seed and then sets reset low and enable high to use the module.
In output.txt we can see the encrypted flag that is 40 byte long.
LCG isn't random so, knowing the parameters, we can reproduce it. So we have potentially 28 bits to bruteforce. It's possible but we can do it much quicker.
We now that the flag must start with "L3AK{" so, xoring each of these chars with the encoded flag's respective one, we know the first 5 outputs of prng.vhdl.
```python
print(hex(ord('L') ^ 0x50)) #0x1C
print(hex(ord('3') ^ 0xE9)) #0xDA
print(hex(ord('A') ^ 0xA8)) #0xE9
print(hex(ord('K') ^ 0x7F)) #0x34
print(hex(ord('{') ^ 0x3B)) #0x40
```
This is a huge advantage: we don't know anything about the original seed but we know the first output must be 0x1C so we can directly start from here. 
This means that the seed after the first iteration is between 0x1C00000 and 0x1CFFFFF and we have to bruteforce only 20 bits.
Using the other 4 values as conditions for the next iterations we can select only the initial seed that produces "L3AK{".
With that we can reverse xor the encrypted flag and retrieve the original one.

## Exploit
```python
def generateXorKey(seed):
    A = 73067557
    C = 111837721
    M = 2**28
    return (seed * A + C) % M


def printFlag(xor_key):
    enc_flag = [0x50, 0xE9, 0xA8, 0x7F, 0x3B, 0x31, 0x71, 0x19,
                0x31, 0x9E, 0x28, 0x63, 0x13, 0x52, 0x0A, 0xFD,
                0xE0, 0x0A, 0x71, 0x0D, 0x15, 0x6B, 0x75, 0x48,
                0x23, 0x73, 0xF4, 0x33, 0x24, 0x73, 0xA8, 0x76,
                0xE2, 0xBA, 0xD7, 0x78, 0xB6, 0x7F, 0xD5, 0xB4]
    flag = ""
    for x in range(40):
        flag += chr(enc_flag[x] ^ xor_key[x])
    print(flag)


for seed in range(0x1C00000, 0x1D00000):
    xor_key = [0x1C]
    init_seed = seed
    for i in range(1, 40):
        init_seed = generateXorKey(init_seed)
        next_byte = (init_seed >> 20) & 0xFF
        if i == 1:
            if next_byte != 0xDA:
                break
        elif i == 2:
            if next_byte != 0xE9:
                break
        elif i == 3:
            if next_byte != 0x34:
                break
        elif i == 4:
            if next_byte != 0x40:
                break
        xor_key.append(next_byte)
        if i == 39:
            printFlag(xor_key)

```
This will print the flag *L3AK{Y0u_C4N_d0_M4NY_Th1ngS_w1Th_VHDL!!}*
