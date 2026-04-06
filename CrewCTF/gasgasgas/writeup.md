# Gas Gas Gas

CTF: CrewCTF 2025(Jeopardy)

Category: hardware

Author: Aali

## Description

Someone has been sending messages to the dash of my car, a 2007 Volvo S60. I managed to capture this signal, maybe you can make sense of it?

## Overview

This challenge is composed by a .csv file.

## Solution

I opened the .csv and took a look at the content. There are 5000 rows. Each row contains the row index, the timestamp and the volt measurements of two channels: CH1 and CH2.

<img width="348" height="706" alt="Screenshot 2026-04-06 092247" src="https://github.com/user-attachments/assets/4ab8a5d1-c2fb-45cf-ac5f-ccfc0fafed75" />

I searched for the protocol used by Volvo and found that it's CAN Bus.

<img width="892" height="136" alt="Screenshot 2026-04-06 092336" src="https://github.com/user-attachments/assets/14021560-eadd-4db7-a91c-3eac0db1cd99" />

In particular I saw that the DIM (dash) uses the LS CAN with a frequency of 125Kbps. Since there are the timestamps in the .csv I saw that the difference between two of them is 4 microseconds, that means a sampling frequency of 250Kbps and so 2 sample for each bit transmitted.

<img width="861" height="283" alt="Screenshot 2026-04-06 092354" src="https://github.com/user-attachments/assets/06bc92ab-f406-44d5-a2ae-54553249f208" />

How are the bits encoded? There are two channels: CAN Low and CAN High. When their voltage difference is smaller than a specific treshold the bit is recessive (1), when is bigger the bit is dominant (0).

<img width="851" height="717" alt="Screenshot 2026-04-06 093043" src="https://github.com/user-attachments/assets/f58b08ed-5042-4261-8022-f39d613e16b9" />

The next thing I looked for was the layer 2 protocol to exchange frames. There are 4 types of frames: data, remote, error and overload. After I read the whole datasheet (link in sources.md) I tried to understand which type of frames I was looking at by measure their length. At the end of each data and remote frame there is the End of Frame, that consists in 7 bit set to 1, and then there is a interframe space made of at least 3 bit set to 1. The Start of Frame is always a bit set to 0. This means I could roughly measure the size of each frame using the distance between the first and the last 0 before a long sequence of 1s. I found 13 frames and their length was between 127 and 133 bits. It's important to consider the stuffing: in a frame 6 consecutive identical bits are considered an error so if there are 5 consecutive identical bits the protocol adds a complementary bit. In the decoding phase the stuffing bits must be removed. I thought that the frames I found were of the same type and the length difference was caused by stuffing. So I wrote a script to measure each frame before and after the destuffing.

```python
import csv

ranges = [[4698, 4442], [4322, 4068], [3942, 3682],
          [3578, 3322], [3284, 3018], [2952, 2696],
          [2628, 2374], [2310, 2050], [1980, 1723],
          [1668, 1404], [1346, 1082], [1018, 754],
          [702, 436]]

with open('gas.csv', mode='r', encoding='utf-8') as file:
    content = list(csv.reader(file, delimiter=','))
    
    for spot in ranges:
        message = ""

        for i in range(spot[0]-1, spot[1]-1, -2):
            if float(content[i][3]) - float(content[i][2]) > 1000:
                message += "0"
            else:
                message += "1"

        print(f"SPOT {spot[0]}-{spot[1]}\nmessage: {message}\nlength: {len(message)}")

        i = 0
        while(i < len(message)):
            if message[i:i+5] == "00000" or message[i:i+5] == "11111":
                message = message[:i+5] + message[i+6:]
                i += 5
            else:
                i += 1

        print(f"message destuffed: {message}\nlength: {len(message)}\n\n")
```

The results was exactly what I expected. Each frame was made of 120/121 bits.

<img width="1721" height="936" alt="Screenshot 2026-04-06 095221" src="https://github.com/user-attachments/assets/cf2cc2a1-fde2-4598-8910-04be68654c9d" />

The only frame that could have this size is a Data Frame Extended with 8 bytes of data. The structure is:

- Start of Frame: 1 bit (always 0)
- Base Identifier: 11 bit (the first 7 bit can't be all 1s)
- SRR: 1 bit (always 1)
- IDE: 1 bit (always 1)
- Extended Identifier: 18 bit
- RTR: 1 bit (always 0)
- r1 and r0: 2 bits (always 00)
- Data Length: 4 bit (can't be bigger than 1000)
- Data: 8 bit * n, where n is the value of Data Length
- CRC Sequence: 15 bit
- CRC Delimeter: 1 bit (always 1)
- ACK Slot: 1 bit (always 0)
- ACK Delimeter: 1 bit (always 1)
- End of Frame: 7 bits (always 1s)

Without the last 3 fields and considering 64 bits of Data (Data Length = 1000) the frame size is 120 bits (excluding the series of 1s at the end of the frame). At this point I was sure I was looking at data frames and that probably the flag was in the Data field so I wrote a script to show each field of the ustuffed frames. Unfortunately, the results were completely off with almost every field containing wrong bits. I tried to reverse the order of frames and bits and somehow it worked.

```python
import csv

ranges = [[4698, 4442], [4322, 4068], [3942, 3682],
          [3578, 3322], [3284, 3018], [2952, 2696],
          [2628, 2374], [2310, 2050], [1980, 1723],
          [1668, 1404], [1346, 1082], [1018, 754],
          [702, 436]]

ranges = ranges[::-1]

with open('gas.csv', mode='r', encoding='utf-8') as file:
    content = list(csv.reader(file, delimiter=','))
    
    for spot in ranges:
        message = ""

        for i in range(spot[1]+1, spot[0]+1, 2):
            if float(content[i][3]) - float(content[i][2]) > 1000:
                message += "0"
            else:
                message += "1"

        i = 0
        while(i < len(message)):
            if message[i:i+5] == "00000" or message[i:i+5] == "11111":
                message = message[:i+5] + message[i+6:]
                i += 5
            else:
                i += 1

        print(f"SPOT {spot[0]}-{spot[1]}\nmessage: {message}\nlength: {len(message)}\n")
        print(f"start bit: {message[0]}")
        print(f"base id: {message[1:12]}")
        print(f"srr: {message[12]}")
        print(f"ide: {message[13]}")
        print(f"extended id: {message[12:32]}")
        print(f"rtr: {message[32]}")
        print(f"r1 and r0: {message[33:35]}")
        print(f"data length: {message[35:39]}")
        print(f"data: {message[39:47]} {message[47:55]} {message[55:63]} {message[63:71]} {message[71:79]} {message[79:87]} {message[87:95]} {message[95:103]}")
        print("\n\n")
```

<img width="1624" height="702" alt="Screenshot 2026-04-06 101854" src="https://github.com/user-attachments/assets/740d329a-48db-49ac-818c-dfc19631ac54" />

I really don't know why it works. The timestamps show that the samples are arranged in the .csv from most recent to least recent so the first bits of each frame should be those with the biggest row index (for each range) and not viceversa. Maybe the timestamps are a decoy? Who knows. Still, at this point I had 13 correct data frames and I tried to print them.

```python
data = [
    [0b11000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00110101],
    [0b11000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00110001],
    [0b11100001, 0b11111110, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000],
    [0b10100111, 0b00000000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b01000100],
    [0b00100001, 0b01100101, 0b01100011, 0b01101111, 0b01100100, 0b01100101, 0b00100000, 0b00100000],
    [0b00100010, 0b00100000, 0b00100000, 0b00100000, 0b01011001, 0b00110011, 0b01001010, 0b01101100],
    [0b00100011, 0b01100100, 0b00110011, 0b01110100, 0b01111010, 0b01100100, 0b01000100, 0b01001110],
    [0b01100101, 0b01110111, 0b01011000, 0b01111010, 0b01000010, 0b01001111, 0b00000000, 0b00000000],
    [0b10100111, 0b00000000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b00100000, 0b01000010],
    [0b00100001, 0b01100001, 0b01110011, 0b01100101, 0b00110110, 0b00110100, 0b00100000, 0b00100000],
    [0b00100010, 0b00100000, 0b00100000, 0b00100000, 0b01011000, 0b00110011, 0b01010010, 0b01001001],
    [0b00100011, 0b01011010, 0b01010110, 0b00111001, 0b01101110, 0b01001110, 0b01001000, 0b01001101],
    [0b01100101, 0b01101000, 0b01100110, 0b01010001, 0b00111101, 0b00111101, 0b00000000, 0b00000000],
]

s = ""
for block in data:
    for c in block:
        s += chr(c)

print(s)
```

The result was:

<img width="972" height="27" alt="Screenshot 2026-04-06 090019" src="https://github.com/user-attachments/assets/75051fc9-a978-49ee-9f45-abf4d27fc294" />

I thought there were some wrong chars so I looked for "D!ecode" in the data matrix I did and excluded the column with that "!" from the printing. the result was:

<img width="815" height="24" alt="Screenshot 2026-04-06 102838" src="https://github.com/user-attachments/assets/74ee99bb-8aa1-4680-8cb2-360684bfb61e" />

Then I concatenated the two base64 parts and decode it

<img width="706" height="70" alt="Screenshot 2026-04-06 102854" src="https://github.com/user-attachments/assets/703ca7c1-0102-421b-824a-ae2b4398e2af" />

I got the flag *crew{st3p_0N_tHe_g4s!}*








