# Spy PLC(Forensics)

CTF: Iran Tech Olympics 2025(Jeopardy)

Category: hardware

Author: Unknown

## Description

PLC operators have detected that the test mode has been activated and intruders have sent a message through it. What message is this [PLC](https://ctf.olympics.tech/tasks/Spy_PLC_50028d5ee1eb7164c1f0df6475f927d0aa6bb5d1.txz) transmitting?

Note: Find the spy PLC message and wrap with ASIS{}!

## Overview

This challenge is composed by a .st file. In this context that means a structured text file, a format used for PLC.

## Solution

I opened the file with a text editor and analysed the code. There are 32 cases for 4 different parameters: temperature, humidity, pressure and gas. At each step a new case for each parameter is taken and used to create new variables (Tz, Hz, Pz and Gz). This new variables are used to determined the boolean values of other 8 variables. Since these last 8 variables are boolean, exactly 8 and the last point of each iteration (they aren't used in any other part of the program) I deduced they are bits: each iteration produces a byte of the flag. I wrote a script in python to emulate the .st process and I discovered that they are in fact bits in little endian. So I slightly modified the script to get the flag.

```python
temp_cases = [180, 180, 1300, 1300, 1300, 180, 900, 1300,
              1300, 180, 180, 400, 1300, 180, 400, 400,
              900, 180, 1300, 180, 900, 1300, 400, 900,
              180, 400, 1300, 180, 900, 400, 1300, 400]
temp_min = 200
temp_max = 1200
temp_mid = (temp_max+temp_min)/2

hum_cases = [150, 1000, 150, 150, 1000, 400, 150, 150,
             1000, 400, 800, 400, 1000, 800, 400, 150,
             150, 400, 1000, 150, 400, 1000, 150, 1000,
             400, 400, 150, 400, 150, 800, 150, 400]
hum_min = 200
hum_max = 900
hum_mid = (hum_min+hum_max)/2

press_cases = [1000, 400, 400, 3500, 1000, 3500, 3500, 3500,
               1000, 3500, 400, 2000, 1000, 2000, 2000, 2000,
               1000, 1000, 1000, 3500, 2000, 1000, 3500, 2000,
               2000, 1000, 3500, 3500, 3500, 2000, 3500, 3500]
press_min = 500
press_max = 3000
press_mid = (press_min+press_max)/2

gas_cases = [300, 300, 300, 300, 300, 50, 300, 50,
             300, 300, 300, 300, 300, 300, 300, 300,
             300, 300, 300, 50, 300, 300, 50, 300,
             300, 300, 300, 300, 300, 300, 50, 50]
gas_min = 100
gas_max = 1000
gas_mid = (gas_min+gas_max)/2

flag = ""

for i in range(32):

    if temp_cases[i] <= temp_min:
        Tz = 0
    elif temp_cases[i] <= temp_mid:
        Tz = 1
    elif temp_cases[i] < temp_max:
        Tz = 2
    else:
        Tz = 3

    if hum_cases[i] <= hum_min:
        Hz = 0
    elif hum_cases[i] <= hum_mid:
        Hz = 1
    elif hum_cases[i] < hum_max:
        Hz = 2
    else:
        Hz = 3

    if press_cases[i] <= press_min:
        Pz = 0
    elif press_cases[i] <= press_mid:
        Pz = 1
    elif press_cases[i] < press_max:
        Pz = 2
    else:
        Pz = 3

    if gas_cases[i] <= gas_min:
        Gz = 0
    elif gas_cases[i] <= gas_mid:
        Gz = 1
    elif gas_cases[i] < gas_max:
        Gz = 2
    else:
        Gz = 3

    response = 0

    if Tz == 1 or Tz == 3:
        response += 1

    if Tz >= 2:
        response += 2

    if Hz == 1 or Hz == 3:
        response += 4

    if Hz >= 2:
        response += 8

    if Pz == 1 or Pz == 3:
        response += 16

    if Pz >= 2:
        response += 32

    if Gz == 1 or Gz == 3:
        response += 64

    if Gz >= 2:
        response += 128

    flag += chr(response)

print(flag)
```

I got the flag *ASIS{PLCs_4r3_tHe_heaRT_0f_1ndUstri35}*
