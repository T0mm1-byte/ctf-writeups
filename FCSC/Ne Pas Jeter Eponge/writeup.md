# Ne Pas Jeter l'Eponge

CTF: FCSC 2022

Category: hardware

Author: Cryptanalyse

## Description

You are given the logic circuit of the image circuit.png, and you need to give the binary output corresponding to the input (x0, x1, x2, x3, x4) = (1, 0, 0, 1, 1). Wrap your answer within FCSC{} to get the flag.

For example, (x0, x1, x2, x3, x4) = (1, 0, 0, 0, 0) would give (y0, y1, y2, y3, y4) = (1, 0, 1, 0, 0), which would make FCSC{10100} as flag.

## Overview

This chalenge is made of the image of a circuit.

## Solution

The request is pretty straightfoward, it could be done by hand but I wrote a python script to simulate the circuit.

```python
def NOT(x):
    return 1 if x == 0 else 0

def AND(x, y):
    return 1 if (x == 1 and y == 1) else 0

def XOR(x, y):
    return 1 if (x != y) else 0

X = [1, 0, 0, 1, 1]
Y = [0, 0, 0, 0, 0]

for i in range(len(X)):
    Y[i] = XOR(X[i], AND(X[i-2], NOT(X[i-1])))

print("FCSC{" + "".join([str(y) for y in Y]) + "}")
```

The flag is *FCSC{10111}*