# RFID_Demod

CTF: Asian Cyber Security Challenge 2024(Jeopardy)

Category: hardware

Author: Chainfire73

## Description

We have obtained analog trace captureb by sniffing a rfid writer when it was writing on a T5577 tag.
Can you help us find what DATA is being written to it?
Flag Format : ACSC{UPPERCASE_HEX}

## Overview

This challenge is composed by a .wav file that contains the message written to the tag.

## Solution

The first thing to do is to look at the tag's datasheet to see how it works and how it receives information.

<img width="1403" height="866" alt="Image" src="https://github.com/user-attachments/assets/0c077ef3-52e1-4623-9c1d-86a472c948e6" />
<img width="1427" height="791" alt="Image" src="https://github.com/user-attachments/assets/51323afb-ae57-4fad-9539-f28edd7450c0" />

The bits are encoded as gap in the signal.
The short ones (24 field clocks) are '0' and the long ones (56 field clocks) are '1'.
When there is a gap bigger than 64 field clocks the tag will assume the comunication terminated.

I opened trace.wav with audacity and zoomed in the gap area to see the consecutive gaps.
There are 38 gaps (excluding the start and ending gaps) so is likely standard downlink mode.
Since the duration difference between '0' and '1' is big I could easily identify each bit of the sequence.

<img width="1898" height="207" alt="Image" src="https://github.com/user-attachments/assets/8c79f85a-9f30-4b28-ab23-bce13897e9fd" />

The bits are:
- '10', this is the opcode to write on a page 0's register
- '0', this is the lock bit (off)
- '10110001011000110101110010101101', this is the 32bit message 
- '011', this is the register's address

Since the flag is the message in hex it is *ACSC{B1635CAD}*

