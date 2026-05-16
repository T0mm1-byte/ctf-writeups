# The Needle

CTF: Hack The Box

Category: Hardware

Author: MrR3boot

## Description

As a part of our SDLC process, we've got our firmware ready for security testing. Can you help us by performing a security assessment?

## Overview

This challenge is composed by a .bin file that is the dump of a firmware

## Solution

The first thing I did was to try to connect with netcat at the endpoint given by the challenge. I saw a login similar to telnet and so I tried to connect with telnet to test my idea. Then I used "binwalk --term firmware.bin" and found that it has a squashfs that I extracted using "binwalk -e firmware.bin". Once in the filesystem I searched for the files that contains the string "telnet" with the command "grep -rl "telenet" ./" and found three of them. One in particular, ./etc/scripts/telnetd.sh, seemed the file I was looking for so I opened it and saw that it was in fact the script that initialize the telenet connection. The name is "Device_Admin", the password is loaded in the variable sign from /etc/config/sign so I opened that file to retrieve the sign. At this point I reused nc to connect and got access to a remote shell where I just got the flag that was stored in the file flag.txt.



The flag is *HTB{4_hug3_blund3r_d289a1_!!}*
