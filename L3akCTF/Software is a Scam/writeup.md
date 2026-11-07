# Software is a Scam

CTF: L3akCTF 2026(Jeopardy+KOTH)

Category: hardware

Author: JAGIC

## Description

Why use software when hardware gets the job done just fine?

## Overview

This challenge is made of a .png file that contains the image of a circuit

## Solution

The circuit has 20 entries, named from C1 to C20, and a single exit. I supposed each C_i is a byte of the flag and that the right combination should get a 1 as a output. The idea was to recreate the circuit in python and to use z3 to solve it. Here some assunctions I made: 
- each line should be made of 8 bits so overflows or underflows of ADD, SUB and MUL gates must be ignored. Practically I did a logic AND 0xFF to always keep the 8 least significant bits. These operations cosider the inputs as unsigned bytes.
- the point above isn't true for the output of COMP blocks that produce a boolean value.
- there is a block with just a <-, since it has two inputs and one of those is 2 I considered it as a logical shift left.
- each logic gate operates bitwise.
- The behaviour of COMP blocks depends on inputs: if its inputs a and b are 8 bits values then it performs a == b and returns a boolean, else if they are 1 bit boolean values (from other COMP blocks) it performs a & b to filter out the cases where a = b = 0 so the output will be 1 only if a = b = 1.
- A COMP block can also do > and < operations only on 8 bits inputs and they are considered unsigned.
- The first 5 values are 'L3AK{'

After implementing it by hand and miraculously without errors, I ran it and got the flag.

```python
from z3 import *

def COMP(a, b):
    if is_bool(a) and is_bool(b):
        return And(a, b)
    return a == b

def LT(a, b):   
    return a < b

def GT(a, b):   
    return a > b

def XOR(a, b):
    return a ^ b

def NOT(a):
    return ~a

def AND(a, b):
    return a & b

def OR(a, b):
    return a | b

def NOR(a, b):
    return ~(a | b)

def XNOR(a, b):
    return ~(a ^ b)

def NAND(a, b):
    return ~(a & b)

def MUL(a, b):
    return (a * b) & 0xFF

def ADD(a, b):
    return (a + b) & 0xFF

def SUB(a, b):
    return (a - b) & 0xFF

def XNOR3(a, b, c):
    return ~((a & ~b & ~c) | (~a & b & ~c) | (~a & ~b & c))

def LSH(a, b):
    return (a << b) & 0xFF

def BLOCK_A(C1, C2, C3, C4):
    var_1_1 = MUL(C1, C4)
    var_1_2 = AND(C1, C3)
    var_1_3 = XOR(C2, C4)
    var_1_4 = XOR(C3, C4)
    var_1_5 = SUB(C2, C1)
    var_1_6 = SUB(C3, C1)
    var_2_1 = ADD(var_1_1, C1)
    var_2_2 = NOR(var_1_2, var_1_3)
    var_2_3 = COMP(var_1_4, 0x0a)
    var_2_4 = COMP(var_1_5, 0xe7)
    var_2_5 = LT(BitVecVal(0xf4, 8), var_1_6)   
    var_3_1 = XNOR(var_2_1, C2)
    var_3_2 = COMP(var_2_2, 0x87)
    var_4 = COMP(var_3_1, 0x5c)
    var_5 = COMP(var_4, var_3_2)
    var_6 = COMP(var_5, var_2_3)
    var_7 = COMP(var_6, var_2_4)
    return COMP(var_7, var_2_5)

def BLOCK_B(C5, C10, C15, C20):
    var_1_1 = SUB(C5, C20)
    var_1_2 = AND(C10, C20)
    var_1_3 = NOT(C5)
    var_1_4 = AND(C5, C10)
    var_1_5 = XNOR(C15, C20)
    var_1_6 = ADD(C10, C15)
    var_2_1 = COMP(var_1_1, 0xfe)
    var_2_2 = XOR(var_1_2, var_1_3)
    var_2_3 = AND(var_1_4, var_1_5)
    var_2_4 = GT(BitVecVal(0xd6, 8), var_1_6)   
    var_2_5 = LT(BitVecVal(0xbd, 8), var_1_6)  
    var_3_1 = COMP(var_2_2, 0xd9)
    var_3_2 = COMP(var_2_3, 0x59)
    var_4 = COMP(var_2_1, var_3_1)
    var_5 = COMP(var_4, var_3_2)
    var_6 = COMP(var_5, var_2_4)
    return COMP(var_6, var_2_5)

def BLOCK_C(C6, C7, C8, C9, C11, C12, C13, C14, C16, C17, C18, C19):
    var_1_1 = AND(C9, C13)
    var_1_2 = NAND(C9, C16)
    var_1_3 = ADD(C6, C13)
    var_1_4 = LSH(C6, 2)
    var_1_5 = XOR(C8, C16)
    var_1_6 = SUB(C13, C8)
    var_2_1 = XOR(var_1_1, var_1_2)
    var_2_2 = AND(var_1_2, C17)
    var_2_3 = COMP(var_1_3, 0xb5)
    var_2_4 = COMP(var_1_5, 0x2c)
    var_2_5 = SUB(C17, C8)
    var_3_1 = XNOR3(var_2_1, C16, C12)
    var_3_2 = XOR(var_2_2, C12)
    var_3_3 = NAND(C12, var_1_4)
    var_3_4 = COMP(var_2_5, 0xef)
    var_3_5 = XNOR3(var_1_4, C11, C13)
    var_4_1 = COMP(var_3_1, C7)
    var_4_2 = XOR(var_3_2, C14)
    var_4_3 = SUB(var_3_1, var_3_3)
    var_4_4 = NAND(C14, var_3_5)
    var_4_5 = COMP(var_1_6, 0x2e)
    var_4_6 = XOR(C9, C19)
    var_5_1 = COMP(var_4_2, 0x51)
    var_5_2 = COMP(var_4_3, 0x74)
    var_5_3 = XOR(var_4_4, var_3_5)
    var_5_4 = ADD(var_3_5, C19)
    var_6_1 = OR(var_5_3, C18)
    var_6_2 = COMP(var_5_4, 0x0d)
    var_6_3 = SUB(C17, C18)
    var_6_4 = ADD(C18, var_4_6)
    var_7_1 = COMP(var_6_1, 0x37)
    var_7_2 = AND(var_6_3, C9)
    var_7_3 = COMP(var_6_4, 0xab)
    var_8_1 = COMP(var_7_2, 0x33)
    var_9 = COMP(var_4_1, var_5_1)
    var_10 = COMP(var_9, var_2_3)
    var_11 = COMP(var_10, var_5_2)
    var_12 = COMP(var_11, var_2_4)
    var_13 = COMP(var_12, var_3_4)
    var_14 = COMP(var_13, var_7_1)
    var_15 = COMP(var_14, var_6_2)
    var_16 = COMP(var_15, var_4_5)
    var_17 = COMP(var_16, var_8_1)
    return COMP(var_17, var_7_3)

    
N = 20
flag = [BitVec(f'b{i}', 8) for i in range(N)]
s = Solver()

for i in range(N):
    s.add(flag[i] > 0x20)
    s.add(flag[i] < 0x7f)

for i, c in enumerate(b"L3AK{"):
    s.add(flag[i] == c)

s.add(COMP(COMP(BLOCK_A(flag[0], flag[1], flag[2], flag[3]), BLOCK_B(flag[4], flag[9], flag[14], flag[19])), BLOCK_C(flag[5], flag[6], flag[7], flag[8], flag[10], flag[11], flag[12], flag[13], flag[15], flag[16], flag[17], flag[18])))

if s.check() == sat:
    model = s.model()
    result = ''.join([chr(model[flag[i]].as_long()) for i in range(N)])
    print(result)
else:
    print("unsat")
```

The flag is *L3AK{CoD3_Hur7_h34D}*
