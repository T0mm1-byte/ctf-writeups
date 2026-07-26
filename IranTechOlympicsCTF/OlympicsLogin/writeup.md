# Olympics Login

CTF: Iran Tech Olympics CTF 2025(Jeopardy)

Category: hardware

## Description

We're facing another Olympic login challenge for an IoT device. If you can log in correctly, the flag will be displayed.

## Overview

This challenge is composed by a .bin file that is a Cortex-M firmware.

## Solution

Using the "file" command I saw the binary has the Flash at 0x8000000 and the RAM at 0x20000000 so it's clearly an STM. I opened it in IDA and went to the reset handler.

<img width="767" height="675" alt="Screenshot 2026-07-26 110016" src="https://github.com/user-attachments/assets/0083ca20-f5f1-4746-82d8-90100dd230fd" />

Cortex-M standard logic: the reset handler calls SystemInit to setup some stuff, copies bytes from Flash to RAM (.data), fills a part of RAM with 0s (.bss), calls __libc_init_array and finally calls main. Nothing strange since here so I checked the main.

<img width="676" height="450" alt="Screenshot 2026-07-26 110245" src="https://github.com/user-attachments/assets/0040eb1a-3cf4-4b74-aa17-e7ff5d9f506d" />

This isn't a classic STM32 main, it looks like an arduino code with a rsetup and an infinite loop. My conclusion was that I was looking at a STM32duino such as a blue pill. initVariant is labeled "weak" since it's not useful for most boards (like this one) and the linker replaced the BL instruction to it with a NOP.W. serialEventRun is useless as well since there isn't any serial Event defined. I focused on setup() and loop().

<img width="287" height="357" alt="Screenshot 2026-07-26 111145" src="https://github.com/user-attachments/assets/d759d145-3004-4587-9de1-b31baa2b13c3" />

Setup calls a function with three parameters and it' clearly an inizialization of a serial communication sinche these parameters are a RAM address (that I called serial_conn), 9600 (the baudrate) and 6 (UART 8N1). So I knew loop() would expect some type of communication and from the description it's clear it will be some type of authentication. Looking at loop() I found this theory correct.

<img width="707" height="657" alt="Screenshot 2026-07-26 111645" src="https://github.com/user-attachments/assets/1285c043-bba7-4aae-8e98-474c8c54cf93" />

I saw two functions. The first one it's used to receive chars and buffer them so I called it receive_line. Nothing strange with it.

<img width="697" height="690" alt="Screenshot 2026-07-26 111749" src="https://github.com/user-attachments/assets/a53fb629-1582-4f54-8436-d4d425c51310" />

The second one is more interesting since it's a simple two-state machine that takes two inputs (username and password as I would've discovered later) and then calls a function to validate them. 

<img width="356" height="400" alt="Screenshot 2026-07-26 112218" src="https://github.com/user-attachments/assets/431a02df-cbf4-4311-a360-aa962ee7d209" />

The function I called inputValidation contains the true logic of the challenge. There is a function to validate username and password (as it's written in the error messages) that are the first part of the flag, and then there are some functions to calcolate v4 that is the last part of the flag.

<img width="837" height="602" alt="Screenshot 2026-07-26 112525" src="https://github.com/user-attachments/assets/95392e47-008d-4c8f-8c5a-d38892018694" />

The function that checks username and password is the same but with different parameters and it's extremely simple to reverse since it's just a xor.

<img width="1012" height="268" alt="Screenshot 2026-07-26 113224" src="https://github.com/user-attachments/assets/3a80d03e-12fc-462f-a6b2-dd3ee85441ac" />

The eight functions to calculate v4 can be divided in two blocks of 4 functions that have the look of hashing function: Init, Update, Final and a conversion from hex to string. Looking at the Init functions of the two blocks I saw, from their costants, they are two different hashes: SHA-256 and MD5. So the last part of the flag is MD5(SHA256(x)) where x is the string conversion of some bytes in the Flash.

<img width="388" height="305" alt="Screenshot 2026-07-26 113646" src="https://github.com/user-attachments/assets/3ec00300-061c-44a7-bdb4-cb4c56db75d2" />

<img width="383" height="222" alt="Screenshot 2026-07-26 113657" src="https://github.com/user-attachments/assets/36adb373-1448-48eb-9f2d-0ef0cdbf1cab" />

At this point I just coded a script to get the flag.

```python
import hashlib

first_buff = [0x70, 0x11, 0xEB, 0x34, 0x19, 0x1B, 0x18, 0xCC]
second_buff = [0x1E, 0x22, 0x9F, 0x75, 0x7D, 0x76, 0x39, 0xA2]

username_buff = [x ^ y for x, y in zip(first_buff, second_buff)]
username = "".join([chr(c) for c in username_buff])

third_buff = [0x02, 0x03, 0x1A, 0x06, 0x3B, 0x01, 0x10, 0x18, 0x5D, 0x6C, 0x2B, 0x31,
              0x24, 0x1E, 0x14, 0x19, 0x5E, 0x41, 0x30, 0x32, 0x45, 0x4C, 0x00, 0x51]
user_3 = username * 3
user_buff = [ord(c) for c in user_3]

password_buff = [x ^ y for x, y in zip(third_buff, user_buff)]
password = "".join([chr(c) for c in password_buff])

msg = b"1e229f757d7639a2"
d1  = hashlib.sha256(msg).hexdigest()          
v4  = hashlib.md5(d1.encode()).hexdigest() 

print("flag: ASIS{" + username + "_" + password + "_" + v4 + "!}")
```

I got the flag *ASIS{n3tAdm!n_l0nG_l1v3__p@s5w0rDs!!!?_35390bed4dc7055a9d26f610c454ab2d!}*
