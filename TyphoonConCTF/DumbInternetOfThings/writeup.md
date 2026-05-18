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



and I searched for each element. The request template:



the host:



The token:



The payload:



And the payload size:



Then I did the same request and got the flag *S3D{They_d0nt_mak3_like_th3y_u5ed_to}*
