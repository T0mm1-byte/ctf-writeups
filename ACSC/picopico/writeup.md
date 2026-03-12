# picopico

CTF: Asian Cyber Security Challenge 2024(Jeopardy)

Category: hardware

Author: op

## Description

Security personnel in our company have spotted a suspicious USB flash drive. They found a Raspberry Pi Pico board inside the case, but no flash drive board. Here's the firmware dump of the Raspberry Pi Pico board. Could you figure out what this 'USB flash drive' is for?

## Overview

This challenge is composed by a .bin file.

We have to discover what this firmware does.

## Solution

First thing first let's run binwalk on firmware.bin.



Nothing interesting. Since it's a Raspberry Pi it's likely that there is some high level code somewhere.

Let's search for it using strings firmware.bin > strings.txt.

At the end of strings.txt there's a python code (just the interesting part):

```python
import storage
storage.disable_usb_drive()
import time
L=len
o=bytes
l=zip
import microcontroller
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
w=b"\x10\x53\x7f\x2b"
a=0x04
K=43
if microcontroller.nvm[0:L(w)]!=w:
    microcontroller.nvm[0:L(w)]=w
O=microcontroller.nvm[a:a+K]
h=microcontroller.nvm[a+K:a+K+K]
F=o((kb^fb for kb,fb in l(O,h))).decode("ascii")
S=Keyboard(usb_hid.devices)
C=KeyboardLayoutUS(S)
time.sleep(0.1)
S.press(Keycode.WINDOWS,Keycode.R)
time.sleep(0.1)
S.release_all()
time.sleep(1)
C.write("cmd",delay=0.1)
time.sleep(0.1)
S.press(Keycode.ENTER)
time.sleep(0.1)
S.release_all()
time.sleep(1)
C.write(F,delay=0.1)
time.sleep(0.1)
S.press(Keycode.ENTER)
time.sleep(0.1)
S.release_all()
time.sleep(0xFFFFFFFF)
```

This code verifies that the first 4 bytes of non volatile memory (nvm) are equal to w, then extracts the next 86 bytes, splits them in two blocks of 43 bytes each and xors them to get a cmd instruction. Then it opens the cmd and executes the instruction.

The nvm is somewhere in firmware.bin. To find the offset we can use hexdump -C firmware.bin | grep "10 53 7f 2b".



The next move is to get the 90 bytes from that offset using hexdump -s 0xff000 -n 90 -C firmware.bin



Now we can just write a script to retrieve the cmd instruction:

```python
nvm = [0x10, 0x53, 0x7f, 0x2b, 0x41, 0xa0, 0x71, 0x51, 0x9f,
       0xca, 0xfd, 0x84, 0x35, 0x0a, 0xd2, 0xb0, 0x1e, 0xa8,
       0xa9, 0xb7, 0x10, 0x1f, 0x55, 0x7a, 0x8c, 0x98, 0xb2,
       0x69, 0xef, 0x92, 0xc5, 0x15, 0xd0, 0x4b, 0xff, 0x87,
       0x17, 0x63, 0xe4, 0x62, 0xc6, 0xa5, 0xb2, 0xbc, 0x8e,
       0xef, 0xd8, 0x24, 0xc3, 0x19, 0x3e, 0xbf, 0x8b, 0xbe,
       0xd7, 0x76, 0x71, 0xe1, 0x84, 0x27, 0x98, 0x9d, 0x87,
       0x73, 0x2e, 0x63, 0x19, 0xbf, 0xae, 0xd4, 0x0b, 0x8d,
       0xf3, 0xfd, 0x76, 0xe4, 0x73, 0xcb, 0xe5, 0x25, 0x5b,
       0xdd, 0x07, 0xf6, 0xc1, 0xd3, 0xd9, 0xb8, 0x89, 0xa5]

a = 4
K = 43
instr = ""
O = nvm[a:a+K]
h = nvm[a+K:a+K+K]

for i in range(K):
    instr += chr(O[i]^h[i])

print(instr)
```

Running the script we find:



So the instruction is just an echo that prints the flag *ACSC{349040c16c36fbba8c484b289e0dae6f}*
