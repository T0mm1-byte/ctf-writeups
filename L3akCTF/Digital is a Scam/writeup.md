# Digital is a Scam

CTF: L3akCTF 2026(Jeopardy+KOTH)

Category: hardware

Author: Suvoni

## Description

Venture into a world of strange circuits, where nothing is as simple as 0 or 1

## Overview

This challenge is made of a .spice file that describes a circuit and a .txt file that contains the output of the circuit

## Solution

I have to say this may be the wickest challenge I've seen so far. The .spice describes a 336-bit DAC (Digital to Analog Converter) that transforms the flag in a voltage. 336 bit means 42 byte of flag and the VREF is 1V. So a standard DAC that can be easily reversed with the complementary ADC. The problem is that the value in output.txt isn't the true flag value since it's altered by the many gains in the circuit. Each code block in the .spice introduces a gain and all the gains must be multiplied by themselves to get the final value G. So the idea was to do output/G and use the result as input for the ADC to retrieve the bits and so the flag. Esier said than done unfortunately. The first block is a network of 45 resistors and the output is the tension in a precise point so I had a 45 equations system to solve (with Gauss obv). The other blocks were conceptually esier but still...let's add the fact that each value needs I don't know how many digits and I had no idea how to manage it. I almost had a stroke trying to implement it by hand and had to rely on AI to correct the infinite series of errors I was getting and to effectively implement my ideas. This is the final script:

```python
import re
from decimal import Decimal, getcontext
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
NETLIST = (HERE / "digital_is_a_scam.spice").read_text()
OUTPUT = F((HERE / "output.txt").read_text().strip())

P = {k: int(v) for k, v in re.findall(r"(\w+)=(\d+)(?=\s|$)", NETLIST)}

def network_gain():
    resistors = re.findall(r"^R(?:\d+|_U1_BIAS) (\S+) (\S+) (\d+)\s*$", NETLIST, re.M)
    names = {n for a, b, _ in resistors for n in (a, b)} - {"0", "circus_dac"}
    index = {n: i for i, n in enumerate(sorted(names))}
    size = len(index)
    m = [[F(0)] * (size + 1) for _ in range(size)]

    for a, b, r in resistors:
        g = F(1, int(r))
        for p, q in ((a, b), (b, a)):
            if p not in index:
                continue
            m[index[p]][index[p]] += g
            if q in index:
                m[index[p]][index[q]] -= g
            elif q == "circus_dac":
                m[index[p]][size] += g  

    for col in range(size):
        pivot = next(r for r in range(col, size) if m[r][col] != 0)
        m[col], m[pivot] = m[pivot], m[col]
        d = m[col][col]
        m[col] = [x / d for x in m[col]]
        for r in range(size):
            if r != col and m[r][col] != 0:
                f = m[r][col]
                m[r] = [x - f * y for x, y in zip(m[r], m[col])]

    return m[index["net_tap"]][size]


def non_inverting(u):
    a, rg, rf = P[f"{u}_A"], P[f"{u}_RG"], P[f"{u}_RF"]
    return F(a) / (1 + a * F(rg, rg + rf))


def inverting(u):
    a, rin, rf = P[f"{u}_A"], P[f"{u}_RIN"], P[f"{u}_RF"]
    return -a * F(rf, rin + rf) / (1 + a * F(rin, rin + rf))


def mirror(c):
    ratio = F(P[f"{c}_WO"], P[f"{c}_LO"]) / F(P[f"{c}_WR"], P[f"{c}_LR"])
    return ratio * F(P[f"{c}_RLOAD"], P[f"{c}_RSET"])


def to_decimal(x):
    return Decimal(x.numerator) / Decimal(x.denominator)

def ADC(Vin):
    bits = list()
    start = F(1, 2)  
    Vin += F(1, 2**337)  
    for _ in range(336):
        if Vin >= start:
            bits.append(1)
            Vin -= start
        else:
            bits.append(0)
        start /= 2
    return bits


def main():
    G = (
        network_gain()
        * non_inverting("U1")
        * -mirror("CM1")  
        * inverting("U2")
        * mirror("CM2") 
        * non_inverting("U3")
        * -mirror("CM3")  
        * inverting("U4")
    )
    vdac = OUTPUT / G
    values = ADC(vdac)
    byte_values = [sum(b << (7 - i) for i, b in enumerate(values[j:j + 8])) for j in range(0, len(values), 8)]
    flag = "".join(chr(b) for b in byte_values)
    print(flag)


if __name__ == "__main__":
    main()
```

The flag is *L3AK{Cl0wN1nG_4r0uNd_w1th_4n4LoG_ciRcu1t5}*