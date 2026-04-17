# Brick by Brick

CTF: UMassCTF 2026

Category: hardware

Author: vdm_0x

## Description

We intercepted a signal from the Master Builder's workshop. Looks like someone was communicating with a custom LEGO controller, but all we captured was this raw data. Can you piece together the message?

## Overview

This file is composed by a .csv file.

## Solution

I opened the .csv file and then I searched for the protocols used by Lego controllers. I searched for a match between the bits in the .csv and the protocols' formats. I looked at LEGO Power Functions RC, LEGO Powered UP, LEGO EV3 and even LEGO SPIKE Prime but I didn't find anything. I was kinda lost so I checked the hints. It was just UART. I don't know why to mention LEGO in the description if the challenge doesn't use any LEGO protocols but okay I guess. Since I had a .csv I opend it with PulseView and used the embedded UART analyzer. From the .csv I found the sampling frequency of 33377KHz and it worked.




I then exported the result in a .txt file and wrote a simple script to concatenate each char in a message.

```python
message = ""

with open("message.txt", "r") as f:
    rows = f.read().split("\n")

    for i in range(1, len(rows), 3):
        line = rows[i].split()
        if len(line) < 5:
            flag += " "
        else:
            flag += line[4]

print(message)
```




The field secretflag was clearly the flag in hex so I just translated it to ascii.





I got the flag *UMASS{U4R7_15_7h3_b357,_r1gh7?}*
