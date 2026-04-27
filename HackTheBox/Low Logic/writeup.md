# Low Logic

CTF: Hack The Box

Category: hardware

Author: 0xSn4k3000

## Description

I have this simple chip, I want you to understand how it's works and then give me the output.

## Overview

This challenge is composed by a .jpg file that contains a circuit and a .csv that contains the inputs.

## Solution

The circuit takes four bit as input and gives one bit as output. The circuit is made of npn transistors, a 6V generator and some 1ohm resistors. I saw that each input is connected only to the base of a transistor. The ones connected with input 0 and input 1 are in series so they must be both '1' to make corrent flows. Idem for input 2 and input 3. To get a '1' as output, the input must be '11xx' or 'xx11'. The .csv has 192 rows, that means the result will be 24 byte, probably the flag. I wrote a script to do the job.

```python
import csv

table = ["0011", "1100", "1111", "1011", "0111", "1101", "1110"]
extracted = ""

with open('input.csv', mode='r', encoding='utf-8') as file:
    content = list(csv.reader(file, delimiter=','))
    for i in range(1, len(content)):
        logic_input = ""
        for j in range(4):
            logic_input += content[i][j]
        if logic_input not in table:
            extracted += "0"
        else:
            extracted += "1"

flag = ""
bytes_extracted = [extracted[i:i+8] for i in range(0, 192, 8)]
for i in range(24):
    flag += chr(int("0b" + bytes_extracted[i], 2))
print(flag)
```

I got the flag *HTB{4_G00d_Cm05_3x4mpl3}*
