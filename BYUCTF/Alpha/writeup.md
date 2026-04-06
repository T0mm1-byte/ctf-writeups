# Alpha

CTF: BYUCTF 2025(Jeopardy)

Category: Misc(Embedded)

Author: deltabluejay

## Description

I made a little Arduino program that displays a flag on a [14-segment display](https://www.adafruit.com/product/2157)! I captured the I2C data sent to the screen using my Saleae logic analyzer... can you decipher it and extract the flag?

## Overview

The challenge is composed by a .ino file with the source code of the program running on arduino and a .sal file that contains the data sent from the microcontroller to the display.

## Solution

The first thing I did was to look at the .ino code to understand what arduino does. It's really simple, it inizialized the display address on the bus as 0x70 and it sends 4 chars of the flag at a time to the display. Each new chunk of chars (so excluding the first one) contains the last 3 chars of the last chunk and a new char. The effect on the display is that the flag is shifting towards left. The I2C protocol uses a 2 lines bus. Opening the .sal file I could clearly see them as D0 is the SCL (Serial Clock) and D1 is the SDA (Serial Data). I directly applied the I2C analyzer embedded in Saleae Logic to understand the messages.

<img width="1910" height="1048" alt="Screenshot 2026-04-06 225300" src="https://github.com/user-attachments/assets/bb17c7a6-22cd-4a02-8620-81d57ad22251" />

After the first setup messagese where all the data section is made of 0x00s there is a the real series of packets to analyze. (Almost) Each of them is composed by 18 bytes. The first one is the address of the peripheral to which to send the data (0x70, the display). The second one is a delimeter and it's always 0x00. The next 8 bytes are the real data and the others are padding so they are always 0x00. The 8 bytes are divided in 4 hextet. Since the display has 14 segments it's necessary to use a hextet to encode each digit. Each hextet is LSB, that means that, for example 0x78 0x20 actually is 0x2078. I exported the table produced by the I2C Analyzer as a .csv. I saw that the useful packets starts at row 112 and ends after row 800. After that they just start repeating themselves. Unfortunately there are some malformed packets.

<img width="519" height="739" alt="Screenshot 2026-04-06 215409" src="https://github.com/user-attachments/assets/24fc4126-f57e-4cf0-bfab-0a0fc4f51a19" />

I found a mapping of hextet in char for a 14 segments display. Writing the solving script I decided to treat the malformed packets as edge cases: I wrote the general script to print the chars encoded in each packet as well as the position of the packet in the .csv. If the chars weren't found or there was a runtime error I checked the packet in the .csv and dedicated some lines of code to manage that packet. It's not very elegant and it was possible only because the .sal isn't really big. Still, it's the first idea I had and it was fast to implement.

```python
import csv

fourteen_seg = {
    0x0006: '1',
    0x0220: '"',
    0x12CE: '#',
    0x12ED: '$',
    0x0C24: '%',
    0x235D: '&',
    0x0400: "'",
    0x2400: '<',
    0x0900: '>',
    0x3FC0: '*',
    0x12C0: '+',
    0x0800: ',',
    0x00C0: '-',
    0x4000: '.',
    0x0C00: '/',
    0x0C3F: '0',
    0x00DB: '2',
    0x008F: '3',
    0x00E6: '4',
    0x2069: '5',
    0x00FD: '6',
    0x0007: '7',
    0x00FF: '8',
    0x00EF: '9',
    0x1200: '|',
    0x0A00: ';',
    0x00C8: '=',
    0x1083: '?',
    0x02BB: '@',
    0x00F7: 'A',
    0x128F: 'B',
    0x0039: '[',
    0x120F: 'D',
    0x00F9: 'E',
    0x0071: 'f',
    0x00BD: 'G',
    0x00F6: 'H',
    0x1209: 'I',
    0x001E: 'J',
    0x2470: 'K',
    0x0038: 'L',
    0x0536: 'M',
    0x2136: 'N',
    0x003F: 'O',
    0x00F3: 'P',
    0x203F: 'Q',
    0x20F3: 'R',
    0x00ED: 'S',
    0x1201: 'T',
    0x003E: 'U',
    0x0C30: 'V',
    0x2836: 'W',
    0x2D00: 'X',
    0x1500: 'Y',
    0x0C09: 'Z',
    0x2100: '\\',
    0x000F: ']',
    0x0C03: '^',
    0x0008: '_',
    0x0100: '`',
    0x1058: 'a',
    0x2078: 'b',
    0x00D8: 'c',
    0x088E: 'd',
    0x0858: 'e',
    0x048E: 'g',
    0x1070: 'h',
    0x1000: 'i',
    0x000E: 'j',
    0x3600: 'k',
    0x0030: 'l',
    0x10D4: 'm',
    0x1050: 'n',
    0x00DC: 'o',
    0x0170: 'p',
    0x0486: 'q',
    0x0050: 'r',
    0x2088: 's',
    0x0078: 't',
    0x001C: 'u',
    0x2004: 'v',
    0x2814: 'w',
    0x28C0: 'x',
    0x200C: 'y',
    0x0848: 'z',
    0x0949: '{',
    0x2489: '}',
    0x0520: '~',
}

with open('arduino.csv', mode='r', encoding='utf-8') as file:
    content = list(csv.reader(file, delimiter=','))
    row = 113
    space_cnt = 0
    flag = ""

    while row < 800:
        chars = []

        if row == 774:
            chars.append(int(content[row+2][7] + content[row+1][7][2:], 16))
            chars.append(int("0x0C" + content[row+3][7][2:], 16))
            chars.append(int(content[row+7][7] + content[row+6][7][2:], 16))
            chars.append(int(content[row+9][7] + content[row+8][7][2:], 16))
        elif row == 794:
            chars.append(int("0x0C" + content[row+2][7][2:], 16))
            chars.append(int(content[row+6][7] + content[row+5][7][2:], 16))
            chars.append(int(content[row+8][7] + content[row+7][7][2:], 16))
            chars.append(int(content[row+10][7] + content[row+9][7][2:], 16))
        else:
            chars.append(int(content[row+2][7] + content[row+1][7][2:], 16))
            chars.append(int(content[row+4][7] + content[row+3][7][2:], 16))
            chars.append(int(content[row+6][7] + content[row+5][7][2:], 16))
            chars.append(int(content[row+8][7] + content[row+7][7][2:], 16))
        

        pseudo_flag = f"ROW {row}: " + " " * space_cnt
        for c in chars:
            if c in fourteen_seg:
                pseudo_flag += fourteen_seg[c]
            else:
                pseudo_flag += "<?>"
        print(pseudo_flag)

        if space_cnt == 0:
            flag = pseudo_flag[-4:]
        else:
            flag += pseudo_flag[-1]

        space_cnt += 1
        row += 20
        if row == 573:
            row += 1

    print(f"The flag is: {flag}")
```

<img width="759" height="834" alt="Screenshot 2026-04-06 223040" src="https://github.com/user-attachments/assets/932fa64d-76b6-4f47-8afa-588eb588a12e" />

It worked and I got the flag *byuctf{4r3n7_h4rdw4r3_pr070c0l5_c00l?}*
