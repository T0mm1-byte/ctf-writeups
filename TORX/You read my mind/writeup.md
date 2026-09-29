# You read my mind

CTF: TORX Finals 2026

Category: hardware

## Description

I do not want to forget again! I will store it in my storage bin!

## Overview

This was the fourth of six hardware challenges available in place at TORX finals 2026. They gave us a custom board with a STM32F103C8T6, a FT232H USB and a Saleae clone. The challenges were all stored in the board and could be solved in any order besides the first one, Sanity. I suggest to look at Sanity writeup before reading this writeup.

## Solution

I typed "load 3" and then "jump" to start the challenge. In the console I saw two message periodically: "Saving what i remember, ..." and "done". The title and the description suggest that the board is storing something in a memory. The board has two flash memory with eight pins so i tried to sample on the DI e CLK pins of one of them and it worked, I saw the data transmitted and applied the SPI analyzer to them.

<img width="2109" height="2560" alt="photo_5897870918350999983_w" src="https://github.com/user-attachments/assets/825aa50e-753e-483e-8d3a-ccc8e5e0fe57" />

<img width="1390" height="274" alt="Screenshot From 2026-09-29 12-45-08" src="https://github.com/user-attachments/assets/94d9ac49-e927-4747-a6f7-c020b0b44c00" />

What I found was a firmware: there is a preamble made of 8 bytes followed by 215 blocks of 77 bytes each. The preamble is 0x9f (read id command) 0xff 0xff 0xff (dummy) 0x05 (read status command) 0xff (dummy) 0x05 (read status command) 0xff (dummy). It's clear that the STM32 is trying to write something in an external flash memory. Then there are the 215 blocks. All of them have 77 bytes: 13 of preamble and 64 of data. The preamble is 0x06 (write enable command) 0x42 (program security registers command) 0x80 0xkk 0x00 (external flash address) 0xyy 0xhh 0x00 0x08 (internal flash address in little endian) 0x00 0x00 0x00 0x00 (dummy). Then there are the 64 bytes of data that go from the internal to the external flash memory. Looking at internal flash address I saw they are a continuous block located at 0x08008000. Then I wrote a python script to rebuild the firmware

```python
import csv

pos = list()
data = list()

with open('data.csv', 'r') as file:
    content = list(csv.reader(file, delimiter=','))[9:]
    blocks = [content[i:i + 77] for i in range(0, 215*77, 77)]

    for block in blocks:
        pos.append(int.from_bytes(bytes(int(row[4], 16) for row in block[5:9]), 'little'))
        data.append(bytearray(int(row[4], 16) for row in block[13:]))

firmware = bytearray(b'\xff'*(215*64))

with open('firmware.bin', 'wb') as firm:
    for p, d in zip(pos, data):
        off = p - 0x8008000
        firmware[off:off+len(d)] = d
    firm.write(firmware)
```
Typing "file firmware.bin" I got "ARM Cortex-M firmware" so I knew the script was successful. I opened IDA Pro and loaded the file choosing ARM 32 little endian as processor type and ARMv7-M from ARM architecture options. I went straight to reset handler and it was the classic initial function of Cortex-M firmware. From here I went to the main (the last call as always) and found a pretty complex function with lots of calls. It was a trap. Near the end of the function there is the true logic that generates the flag and it's extremely simple. 

<img width="343" height="111" alt="Screenshot From 2026-09-29 16-06-04" src="https://github.com/user-attachments/assets/f91c5c64-40e3-4d7a-bc69-9a02edd7d202" />

The first function is a memset, it does prepare an array of 52 elements initialized at 0, the second one xors 52 bytes in the memory (let's call them data) as data[i] ^ (i+10) and stores the result in array[i], the third and last one is a printf, it just prints the flag. So I wrote a simple python script.

```python
data = bytearray([
    0x5E, 0x44, 0x5E, 0x55, 0x75, 0x3E, 0x4F, 0x7A,
    0x7C, 0x23, 0x63, 0x4A, 0x27, 0x48, 0x6B, 0x71,
    0x2A, 0x6E, 0x70, 0x42, 0x70, 0x70, 0x17, 0x7E,
    0x11, 0x5B, 0x54, 0x15, 0x55, 0x14, 0x77, 0x44,
    0x53, 0x74, 0x5F, 0x1E, 0x4D, 0x5D, 0x03, 0x45,
    0x07, 0x6C, 0x04, 0x43, 0x05, 0x45, 0x67, 0x6A,
    0x6A, 0x0A, 0x41
])

flag = ""

for i in range(len(data)):
    flag += chr(data[i] ^ (i+10))

print(flag)
```

I got the flag *TORX{1_kn0w_1_sh0ul_no7_3xp0s3_my_s3cr3t5_0v3r_SP1}*
