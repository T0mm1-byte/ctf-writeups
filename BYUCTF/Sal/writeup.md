# Sal(Hardware)

CTF: BYUCTF 2024(Jeopardy)

Category: IoT

Author: Legoclones

## Description

A few friends and I recently hacked into a consumer-grade home router. Our first goal was to obtain the firmware. To do that, we hooked up a SOIC-8 clip to the external flash memory chip, connected a Saleae Logic Pro 8 logic analyzer, and captured data using Logic 2 as we booted up the IoT device. The external flash memory chip was Winbond 25Q128JVSQ.


What's the md5sum of /etc/passwd?


Flag format - byuctf{hash}

## Overview

The challenge is composed by seven .bin files and a meta.json file. They are the results of an extraction from a .sal file where each of the .bin contains the data of one channel and the .json file contains the metadata. The goal is to understand the way the communiction works to build the firmware and get the hash of passwd.

## Solution

The first thing I did was to read the datasheet of the flash memory chip.

<img width="831" height="292" alt="Screenshot 2026-04-03 191656" src="https://github.com/user-attachments/assets/b7e4053b-8a63-42ba-8132-27f14e7b54bc" />
<img width="867" height="832" alt="Screenshot 2026-04-03 191630" src="https://github.com/user-attachments/assets/9920a87d-00d5-4b0f-9b4d-0b4fdb6da498" />
<img width="846" height="779" alt="Screenshot 2026-04-03 191540" src="https://github.com/user-attachments/assets/9c5efa6f-9c76-445d-aea6-fce76215d353" />

There are eight signals: /CS, DO(MISO), /WP, GND, DI(MOSI), CLK, /HOLD e VCC. I recomposed the original .sal file using the command "zip -0 capture.sal meta.json digital-0.bin ... digital-6.bin" and opened it in Saleae Logic to see the waves. Knowing how SPI works it was pretty easy to recognize channel 1 as CLK, channel 2 as /CS, channel 3 as DI and channel 4 as DO. Saleae offers an embedded SPI Analyzer so I used it to map the protocol.

<img width="659" height="796" alt="Screenshot 2026-04-03 191732" src="https://github.com/user-attachments/assets/259f2072-a71d-4af5-aec4-a68ef9dd7fdd" />

I then used the extension SPI Flash to translate the bytes to instructions.

<img width="1482" height="965" alt="Screenshot 2026-04-04 124120" src="https://github.com/user-attachments/assets/68554848-c0d1-4a4a-bb05-13d09d5615b7" />

They are almost all read data instructions (0x03) with some read status instructions (0x05) near the end. Each instruction is composed like this: the first byte of MOSI is the opcode (only 0x03 and 0x05 in this case), the next three bytes of MOSI are the address to read. Starting from the fifth byte of MISO there are the data bytes (the firmware in this case). There are usually four byte of data per instructions but it can vary, for example in some instruction there is only one byte of data. Knowing that I exported the table as a .csv file and wrote a script to read from the .csv and build the firmware. The flash memory is 16MB so I inizialized the firmware as 0x10000000 0xFF. This way I avoided problems like reading more times the same bytes and I had already set the unutilized bytes as 0xFF that is the standard.

```python
import csv

MOSI = list()
MISO = list()

with open('SPI_results.csv', mode='r', encoding='utf-8') as file:
    content = csv.reader(file, delimiter=',')
    mosi = b""
    miso = b""

    for row in content:
        if row[0] == "SPI" and row[3] != "0.000000004":
            mosi += bytes([int(row[4], 16)])
            miso += bytes([int(row[5], 16)])
        else:
            if mosi != b"" and miso != b"":
                MOSI.append(mosi)
                MISO.append(miso)
                mosi = b""
                miso = b""


firmware = bytearray(b'\xff'*0x1000000)

with open("firmware.bin", "wb") as firm:

    for i in range(len(MOSI)):

        if MOSI[i][0] != 0x03:
            print(f"Problem, found a different opcodes in position {i}: {MOSI[i][0]}")
            continue

        addr = int.from_bytes(MOSI[i][1:4], byteorder="big")
        data = MISO[i][4:]
        firmware[addr:addr+len(data)] = data

    firm.write(firmware)
```

The next thing I did was to run "binwalk --term firmware.bin" to see if the script did a good job.

<img width="1899" height="204" alt="Screenshot 2026-04-04 103835" src="https://github.com/user-attachments/assets/f21fafb6-ef21-44a4-bb1e-ed01a1dca47d" />

All seemed fine so I extracted all using "binwalk -e firmware.bin" and then I found the hash using "md5sum _firmware.bin.extracted/squashfs-root/etc/passwd".

<img width="496" height="23" alt="Screenshot 2026-04-04 104245" src="https://github.com/user-attachments/assets/89d9efa3-a4ea-4786-b51c-35a0dfcd8f71" />

So the flag is *byuctf{c8ef3ad94c6eb97f4fa94a0f0ed33980}*

