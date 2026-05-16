# Firmware

CTF: GreyCTF

Category: ezpz

## Overview

This challenge is composed by a .img file that is the imagine of the firmware.

## Solution

I used "binwalk -e --term firmware.img" to see the sections and extract the squashfs file system. I then searched in it if there was a file with "grey" as string using "grep -rl "grey" ./". I found a file and when I opened it there was the the flag.

<img width="1798" height="233" alt="Screenshot 2026-05-13 151117" src="https://github.com/user-attachments/assets/9e66a13a-9b89-4986-b56c-bab10b7e9484" />

The flag is *grey{inittab_1s_4n_1mp0rt4nt_pl4c3_t0_l00k_4t_wh3n_r3v3rs1ng_f1rmw4r3}*
