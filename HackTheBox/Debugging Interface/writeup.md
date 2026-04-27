# Debugging Interface

CTF: Hack The Box

Category: hardware

Author: diogt

## Description

We accessed the embedded device's asynchronous serial debugging interface while it was operational and captured some messages that were being transmitted over it. Can you decode them?

## Overview

This challenge is composed by a .sal file.

## Solution

To start I opened the file with saleae logic. I saw that the only channel is at "1" in idle and that could be UART. The duration of a sample is 32 microseconds so the frequency is 31250 Hz. I used the saleae UART analyzer and got the flag.




The flag is *HTB{d38u991n9_1n732f4c35_c4n_83_f0und_1n_41m057_3v32y_3m83dd3d_d3v1c3!!52}*
