# Roman Wire

CTF: Iran Tech Olympics CTF(Jeopardy)

Category: hardware

## Description

A Roman device speaks with a flash memory over SPI, but something feels off. Somewhere in that uneasy exchange an important data is being passed.

## Overview

This challenge is composed by a .sal file.

## Solution

Firstly I opened the .sal file using saleae logic and applied the SPI analyzer. 



I saw that the whole interaction is divided in three small blocks and that in each of them the MISO channel and the MOSI channel have alternately a byte of information and a byte that is 0x00. Furthermore each information byte is ascii-printable so I exported all the data as a .csv and wrote a python script to see which strings each block contains.

```python
import csv

with open('roman.csv', mode='r', encoding='utf-8') as file:
    content = list(csv.reader(file, delimiter=','))

    first_block = ""
    for i in range(3, 23):
        if i%2 == 1:
            first_block += chr(int(content[i][4], 16))
        else:
            first_block += chr(int(content[i][5], 16))

    second_block = ""
    for i in range(1223, 1257):
        if i%2 == 1:
            second_block += chr(int(content[i][4], 16))
        else:
            second_block += chr(int(content[i][5], 16))

    third_block = ""
    for i in range(1321, 1341):
        if i%2 == 1:
            third_block += chr(int(content[i][4], 16))
        else:
            third_block += chr(int(content[i][5], 16))

    print(first_block)
    print(second_block)
    print(third_block)
```

The result is:



The first block is useless. The third one contains the encrypted flag. The second one suggests to read the third block as an ancient roman: it's a clear reference to Caesar's cipher. Knowing that the flag format is "ASIS{}" I added these lines at the previous script:

```python
    flag = ""
    shift = ord('S')-ord('L')
    Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabet = "abcdefghihklmnopqrstuvwxyz"
    for c in third_block:
        if c in Alphabet:
            flag += Alphabet[(Alphabet.index(c)+shift) % len(Alphabet)]
        elif c in alphabet:
            flag += alphabet[(alphabet.index(c)+shift) % len(alphabet)]
        else:
            flag += c
    print(flag)
```

I got the flag *ASIS{M0S1_M1S0_H4Lf}*
