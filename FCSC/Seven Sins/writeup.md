# Seven Sins

CTF: FCSC 2022

Category: hardware

Author: rbe

## Description

You are given a 7-segment display connected to inputs that you control, numbered from Bit 0 to Bit 8 as shown in the image 7segments.png. You need to provide the 8 sequences of 9 bits providing the sequential output shown in the image fcsc2022.png.

Note: the flag is FCSC{XXX}, where XXX is the sequence of bits found (so a sequence of characters ‘0’ and ‘1’).

Example: the flag for the sequence 789 would be FCSC{011100100111111111101101110}.

## Overview

This challenge is made of 2 .png files: one is the relationship between bits and segments and the second is the result to obtain.

## Solution

Pretty straightforward challenge, it could be done by hand but I prefered to write a python script.

```python
LetterDiode = {"D": 0, "C": 1, "B": 2, "A": 3, "E": 4, "F": 5, "N": 6, "G": 7, "P": 8}
CharLetter = {"F": "AEFNG", "C": "DAEFN", "S": "DCAFNG", "2": "DBAENG", "0": "DCBAEFN", "3": "DBAENGP"}
Chars = "FCSC2023"
# I choose to rappresent Enable as "N", DP as "P" and "2." as "3" for semplicity

res = list()

for i in range(8):
    n = 0
    for c in CharLetter[Chars[i]]:
        n += 1 << LetterDiode[c]
    n &= 0x1ff
    res.append(n)

print("FCSC{" + "".join(format(n, '09b')[::-1] for n in res) + "}")
```

The flag is *FCSC{000111110100111100110101110100111100101110110111111100101110110101110111}*