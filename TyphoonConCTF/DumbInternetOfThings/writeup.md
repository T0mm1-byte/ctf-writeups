
# Dumb Internet Of Things

CTF: TyphoonCon CTF 2023(Jeopardy)

Category: rev

## Description

Some employee from the engineering team at DumbIOT inc. got drunk and left the prototype of some new sensor device around in our bar.

Here's the firmware dump, can you try to get anything from it?

Flag structure: S3D{...}

## Overview

The challenge is composed by a .bin file, the dump of a firmware.

## Solution

The first thing I did was using "binwalk -e --term dump.bin" to extract the squashfs file system. Searching for some custom binaries in /usr/bin I foundrunProcess. I opened it in IDA and started analyzing it. The flow is pretty simple: it uses the mbedtls functions to establish an ssl connection to a server, sends a request to it, attends a response and then ends. To get the flag I tried to do the same. I identified when the device sends the request:

<img width="688" height="568" alt="Screenshot 2026-05-18 215802" src="https://github.com/user-attachments/assets/9a12e81e-35e0-48cb-a4e8-671e6ef5de4f" />

<img width="538" height="445" alt="Screenshot 2026-05-18 215716" src="https://github.com/user-attachments/assets/b0147d38-74f1-4969-923c-91b5d01ddee4" />

and I searched for each element. The request template:

<img width="971" height="360" alt="Screenshot 2026-05-18 215039" src="https://github.com/user-attachments/assets/3a76fd4a-844b-4861-bd5f-c1e842965e36" />

the host:

<img width="963" height="164" alt="Screenshot 2026-05-18 215138" src="https://github.com/user-attachments/assets/feee62e6-c761-404d-a19b-3e3497fcdbc9" />

The token:

<img width="883" height="244" alt="Screenshot 2026-05-18 221206" src="https://github.com/user-attachments/assets/728c39a9-86ee-4ab2-99e5-e964c46ec79a" />

<img width="439" height="307" alt="Screenshot 2026-05-18 220150" src="https://github.com/user-attachments/assets/0f403fff-801e-4660-900d-9250c522a47e" />

The payload and the payload size:

<img width="786" height="349" alt="Screenshot 2026-05-18 220502" src="https://github.com/user-attachments/assets/e2c27ed7-c7ae-4b4e-b44c-79c3a9cd7d4f" />

<img width="858" height="104" alt="Screenshot 2026-05-18 220959" src="https://github.com/user-attachments/assets/3284387f-e6df-4de9-adbe-2e22caa44717" />

Then I did the same request and got the flag *S3D{They_d0nt_mak3_like_th3y_u5ed_to}*
