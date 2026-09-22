# Sbox

CTF: FCSC 2020

Category: hardware

Author: Cryptanalyse

## Description

You are asked to evaluate the circuit provided (sbox.png) on the 4-bit binary value (x3, x2, x1, x0) = (1, 0, 1, 0) to find the value of y = (y3, y2, y1, y0) at the output of the circuit. The flag is FCSC{<y>}, with <y> the 4-bit binary output value.

Example: on the 4-bit input (x3, x2, x1, x0) = (1, 0, 0, 0), the output value would be (y3, y2, y1, y0) = (0, 0, 1, 1) and the flag would be FCSC{0011}.

## Overview

This chalenge is made of the image of a circuit.

## Solution

The request is pretty straightfoward, it could be done by hand but I wrote a python script to simulate the circuit.

```python
def XOR(x, y):
    return 1 if (x != y) else 0

def NOR(x, y):
    return 1 if (x == 0 and y == 0) else 0

X = [0, 1, 0, 1]
Y = [0, 0, 0, 0]

Y[0] = XOR(X[0], NOR(X[2], X[3]))
Y[1] = XOR(X[3], NOR(X[1], X[2]))
Y[2] = XOR(X[2], NOR(X[1], Y[0]))
Y[3] = XOR(X[1], NOR(Y[0], Y[1]))

print("FCSC{" + "".join([str(y) for y in Y]) + "}")
```

The flag is *FCSC{0101}*