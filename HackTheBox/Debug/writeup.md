# Debug

CTF: Hack The Box

Category: hardware

Author: unknown

## Description

Your team has recovered a satellite dish that was used for transmitting the location of the relic, but it seems to be malfunctioning. There seems to be some interference affecting its connection to the satellite system, but there are no indications of what it could be. Perhaps the debugging interface could provide some insight, but they are unable to decode the serial signal captured during the device's booting sequence. Can you help to decode the signal and find the source of the interference?

## Overview

This challenge is composed by a .sal file

## Solution

I opened the file using saleae logic and recognized it is UART at a 115200 baudrate. I used the saleae UART analyzer and got the flag.




The flag is *HTB{547311173_n37w02k_c0mp30m153d}*
