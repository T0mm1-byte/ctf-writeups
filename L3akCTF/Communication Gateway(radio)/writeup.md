# Communication Gateway(radio)

CTF: L3akCTF 2024(Jeopardy)

Category: hardware

Authors: 0x157

## Description
Something is in-front of you, and you don't even know it

## Overview
This challenge is composed by a .wav file. We have to analyze it

## Solution

I started by opening the file with Audacity and took a look at its spectrum:

<img width="736" height="694" alt="Screenshot 2025-11-17 155427" src="https://github.com/user-attachments/assets/0c18579e-4b62-4247-b670-de59b0447f2e" />

It has only two peaks: one at 1415Hz and another at 1583Hz. The difference bitween them is 168Hz that's very close to 170Hz, the standard difference used by RTTY standard. It's probably BFSK where 1583Hz is 1 and 1415Hz is 0. I could retrieve the message using minimodem but I didn't know the baudrate.
I tried all the common baudrate for RTTY like 45 and 50 but I got only garbage.
Then I remembered the description and saw that the .wav file is named "file10.wav".
What does that 10 means? Could it be the baudrate?
I tried with 10 as baudrate with "minimodem --rx -f file10.wav 10":

<img width="1572" height="114" alt="Screenshot 2025-11-17 172601" src="https://github.com/user-attachments/assets/ac38d512-f169-4705-a1a3-6cf7f4ff43f3" />

I got the flag *L3AK{s1gn4ls_0f_h0p3}*


