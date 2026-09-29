# Sanity

CTF: TORX Finals 2026

Category: hardware

## Description

Sanity check, if everything it is ok on the board you will get the flag. (It requires a hardware modification, talk to the organizers when you are sure you've understood what to do)

## Overview

This was the first of six hardware challenges available in place at TORX finals 2026. They gave us a custom board with a STM32F103C8T6, a FT232H USB and a Saleae clone. The challenges were all stored in the board and could be solved in any order besides the first one, Sanity.




## Solution

The first thing I did was trying to communicate with the board using the ft232 but it just seemed impossible. I sampled each pin using the logic analyzer but they were all either constantly high or constantly low. I saw two sets of four pins each where one of them was constantly high, one was constatntly low and the other two were disconnected from the board. I thought they were UART pins so I asked the hosts to solder a resistor to connect them. It was correct. Unfortunately I didn't take a photo of the board before the modification so here's the final result:




I connected the board to my pc and tried to open a shell with "picocom -b 115200 /dev/ttyUSB0".




It worked. The baudrate was a guess, the most common ones are 115200 and 9600. If they would've failed I would've just sampled the TX pin with the logic analyzer to find the baudrate. Now I had a shell and typing "help" took me to a menu with four commands: list, to list the six available challenges, info n (with n the challenge number), to print the description, load n (with n the challenge number), to prepare a challange, and jump, to start the challenge prepared with the last load.
I typed "load 0" to prepare Sanity and then "jump" to execute it. 




The board printed a bunch of stuff and then gave me the flag *TORX{n0w_th4t_3v3ryt1ng_w0rk5_h4v3_fun}*