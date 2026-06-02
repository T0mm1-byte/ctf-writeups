# Smart Coffee

CTF: QnQSecCTF 2025

Category: hardware

Author: Azadin

## Description

A firmware update introduced unexpected behavior to a SmartCoffee device. Investigate the firmware image for a hidden secret.

## Overview

This challenge is composed by an elf file and a .txt file.

## Solution

The .txt file is pretty useless and the elf file simply does a dump of the EEPROM that is clearly the encrypted flag.

<img width="450" height="371" alt="Screenshot 2026-06-02 165257" src="https://github.com/user-attachments/assets/a889e338-179f-4cb0-b5cc-7735c1d0c890" />

I noticed that the first and the third byte were the same and the format flag is QnQSec{} so I just tried to xor Q with 0x95 and use it as a key to xor each byte.

```python
dump = [0x95, 0xaa, 0x95, 0x97, 0xa1, 0xa7, 0xbf, 0xf7,
        0xbc, 0x9b, 0xb7, 0xf7, 0xb7, 0xaa, 0xb1, 0xa9,
        0x9b, 0xa7, 0xf0, 0xaa, 0x9b, 0xa0, 0xf4, 0x9b,
        0xac, 0xf0, 0xb6, 0xa0, 0xb3, 0xf0, 0xb6, 0xf7,
        0xb9]

key = dump[0] ^ ord('Q')

for i in range(len(dump)):
    dump[i] ^= key

flag = "".join([chr(n) for n in dump])
print(flag)
```

I ran the script and got the flag *QnQSec{3x_s3snum_c4n_d0_h4rdw4r3}*



