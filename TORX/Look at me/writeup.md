# Look At Me

CTF: TORX Finals 2026

Category: hardware

## Description

I'm nicer in a dark room, maybe a little fast, but nice

## Overview

This was the second of six hardware challenges available in place at TORX finals 2026. They gave us a custom board with a STM32F103C8T6, a FT232H USB and a Saleae clone. The challenges were all stored in the board and could be solved in any order besides the first one, Sanity. I suggest to look at Sanity writeup before reading this writeup.

## Solution

I typed "load 1" and then "jump" in the shell. I saw the "SIG" led blink pretty fast and periodically. I thought it was morse code so I tried to use the logic analyzer to sample it. The problem was that apparently no pin was connected to the led so I just sampled directly the led base. Once I got the sequence I tried to analyze it as morse code but it didn't make sense. I noticed that che "CHALL" led blinked with the "SIG" one but at a higher frequency. I sampled both of them I undertood that CHALL was the clock for SIG so I applied to them the SPI analyzer of Saleae Logic.




The SIG led communicates with block of three bytes where the first one is always 0xF7 (MSB)/ 0xEF (LSB). This isn't a know protocol. After a wild guess I discovered that the flag was the second byte of each block LSB and with its bits negated. So I exported the data from Saleae Logic as data.csv and wrote a python script to get the flag.

```python
import csv

with open('solve.csv', 'r') as file:
    content = list(csv.reader(file, delimiter=','))
    flag = ""

    for i in range(2, len(content), 3):
        flag += chr(~int(content[i][4], 16) & 0xff)
        
print(flag)
```

The flag is *TORX{l00k_4t_m3_1m_4ll_sn1ny_4nd_bl1nky}*