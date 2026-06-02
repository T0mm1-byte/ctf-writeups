# Mission Pinpossible

CTF: Hack The Box

category: hardware

author: diogt

## Description

Our field agent cannot access the enemy base due to the password-protected internal gates, but observed that the password seemed to be partially displayed as it was typed into the security keypad. Thanks to an audacious mission, we were able to implant an embedded device into the wiring for the keypad's monitor, and intercepted some data. Your mission is to recover the password from the collected data.

## Overview

This challenge is composed by a .logicdata file and a .jpeg that shows a led display with 2x16 regions of 5x8 pixels and a PCF8574T I2C extender.

## Solution

I started reading the datasheet of both the display and the extender. I found out that the display as a map where each char rapresentation is linked to its ascii encoding (for example, if I want to write an 'A' in the display I have to send a 0x41 to it) but the particular thing is how it takes the bytes. 



The extender has 8 GPIO pins that are used to write the data but the four least significant of them are used as control signals and not to transmit data. That means that to write a byte the extender must send two bytes and in each of them the four most significant bits are the nibble of the real byte. For example, to send "0x41" the extender will send "0x4X" and "0x1X". Actually to transmit a single nibble it's necessary to transmit three byte: "0xX9", "0xXD" and "0xX9". The bit that changes between 0xD and 0x9 is the EN bit and it should go from low to high to low again. The four lower bits are RS = 1 (the extender is sending a data, not a command), RW = 0 (write operation), EN (0 and 1 as explained before) and BL = 1 (4 bit mode, each byte transmitted contains 4 bit of data). This explain why 0x9 and 0xD as lower nibble in each transmitted byte. So what I expected was that, for example, the sequence 0x49 0x4D 0x49 0x19 0x1D 0x19 = "A". I opened the .logicfile with saleae 1.x.y (the old version) and applied its embedded I2C analyzer to see the bytes.



I saw that each block of transmission is "Enter Password" followed by a sequence of "0x2A" and an arbitrary last byte. The first two last bytes were "H" and "T" so I was pretty sure that I should just recover the last bytes of each block and so I did. Honestly I had no idea about how to script it so I just did it by hand.

I got the flag *HTB{84d_d3519n_c4n_134d_70_134k5!d@}*

