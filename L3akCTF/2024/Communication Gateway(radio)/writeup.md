# Communication Gateway(radio)

CTF: L3akCTF 2024(Jeopardy)

Category: hardware

Authors: 0x157

## Description
Something is in-front of you, and you don't even know it

## Overview
This challenge is composed by a .wav file. We have to analyze it

## Solution
Let's start opening the file with Audacity and have a look at its spectrum:

<img width="736" height="694" alt="Screenshot 2025-11-17 155427" src="https://github.com/user-attachments/assets/0c18579e-4b62-4247-b670-de59b0447f2e" />

We can see it has only two peaks: one at 1415Hz and another at 1583Hz

The difference bitween them is 168Hz that's very close to 170Hz, the standard difference used by RTTY standard

We are probably looking at BFSK where 1583Hz is 1 and 1415Hz is 0

We can retrieve the message using minimodem but we don't know the baudrate

We can try all the common baudrate for RTTY like 45 and 50 but we see only garbage

Then we remember the decription and see that the .wav file is named file10.wav

Let's try with 10 as baudrate:

<img width="1572" height="114" alt="Screenshot 2025-11-17 172601" src="https://github.com/user-attachments/assets/ac38d512-f169-4705-a1a3-6cf7f4ff43f3" />

We see the flag *L3AK{s1gn4ls_0f_h0p3}*


