# An4lyz3_1t(warmup)

CTF: Asian Cyber Security Challenge 2024(Jeopardy)

Category: hardware

Author: Chainfire73

## Description

Our surveillance team has managed to tap into a secret serial communication and capture a digital signal using a Salae logic analyzer.
Your objective is is to decode the signal and uncover the hidden message.

## Overview

This challenge is composed by a .sal file.

We have to analyze it.

## Solution

Let's open the .sal file using Logic.
<img width="1832" height="272" alt="Screenshot 2026-03-09 175017" src="https://github.com/user-attachments/assets/7fdca621-30f5-451f-ac8a-3466050a4807" />

There is a single channel signal and the duration of each high and low is a multiple of 17.375 microseconds.

This is a common frequency for UART using 57600 as baudrate.

It's probably UART also because the signal is high in idle and goes to low before sending 8 bits.

In this case we see that the bit sent are 9 beacuse there's also a parity bit.

Let's try to use the Async Serial analyzer to see if the idea is correct.

<img width="897" height="796" alt="Screenshot 2026-03-09 175034" src="https://github.com/user-attachments/assets/00619c8d-45f7-4495-a6d2-d5913aa085cb" />
<img width="383" height="867" alt="Screenshot 2026-03-09 175048" src="https://github.com/user-attachments/assets/8436dbf9-6028-4b53-b14b-6b51dd30cd59" />

We can clearly see the flag: *ACSC{b4by4n4lyz3r_548e8c80e}*
