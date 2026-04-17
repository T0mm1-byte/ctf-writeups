# Crash Landing(Reverse)

CTF: DownUnderCTF 2024(Jeopardy)

Category: hardware

Author: HexF

## Description

Our little kiwi is trying to fly!

## Overview

This challenge is composed by a .bin file.

## Solution

I ran 'file crash_landing.bin' and saw that it's an ARM Cortex-M firmware.



Looking at the data I recognised it's the firmware of a STM32 since the flash start address is 0x08000000 and the ram start address is 0x20000000. I knew that the ram has a size of 128KB since the file command showed 'initial SP at 0x20020000' and initially the stack pointer is set to the end of the ram. The firmware's size is nearly 6.3KB. I searched for an STM32 with these qualities but it doesn't exist an STM32 with 128KB of ram and less than 128KB of flash memory.




I found two series of STM32 with the right properties: STM32F2 and STM32C5. Since I found the .svd file only for the STM32F2 I went that way. I downloaded the .svd and opened ghidra to analyze the firmware. I selected the right architecture and the offset from the options menu.




Then, before the autoanalysis, I created new memory partitions and ran svd-loader.py from the script manager using the .svd I downloaded. The smallest flash I found for a STM32F2 is 256KB so I used that as flash size.










I then went to 0x08000434 beacuse that's the address the program counter is initialised to ('reset at 0x08000434').




It's the classic start of a STM32 firmware where a part of the flash is copied in the ram, some setup functions are run and then the main is called. Ghidra did't a good job decompiling the thumb but it's clear that the main is FUN_08000268.




The main is pretty simple. It reads a char at a time from a USART interface until it encounters '\0' or '\n' or there are more than 0x80 chars. There is a first condition about the input length (0x24 chars) and then there is a loop that checks the input. The problem is DAT_20000000 is BEEF0000 and DAT_20000004 is DEAD0000. They are both beyond the memory limit and these instructions cause an hardfault. The hardfaul handler should be at 0x08000218 ('HardFault at 0x08000218'). 




Here the real control logic is implemented. I checked what is 'NVIC._3384_4' and that's the address of BFAR (Bus Fault Address Register) that contains the register that caused the fault. The 'if' applies a different logic for the case "BEEF" and the case "DEAD". These two cases are called one after the other and one of them returns the result from the lookup table at address 0x080017a7 while the other one returns a byte calculated from the respective char of the input. Once recovered the lookup table I made a python script to get the flag:

```python
table = [
    0x63, 0xFA, 0x3C, 0xD3, 0xB1, 0xC4, 0xA2, 0xCC,
    0xA2, 0xCC, 0x80, 0xA2, 0xF3, 0x17, 0x80, 0xF0,
    0x65, 0x80, 0xA2, 0xCC, 0xA2, 0xA2, 0xCE, 0x17,
    0x80, 0x43, 0xF3, 0x1A, 0x8F, 0xCC, 0xA5, 0xCE,
    0xA5, 0xB6, 0x43, 0x12,
]

flag = ""
for i in range(0x24):
    for c in range(0x20, 0x7F):
        if (c * 0x27 + 7) & 0xFF == table[i]:
            flag += chr(c)
            break
    else:
        flag += "<?>"

print(flag)
```

Running this I got the flag *DUCTF{m3m3_m4p_or_m3mmap_d45832a29d}*
