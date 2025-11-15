# Celestial(radio)

CTF: L3akCTF 2024(Jeopardy)
Category: hardware
Authors: 0x157

## Description
We've received this file over the cosmic network at our headquarters. No idea what they tried to tell us, can you help ?

## Overview
This challenge is composed by a .wav file. We have to analyze it.

## Solution
First thing we have to do is open the file with Audacity and see the spectrum.
<img width="773" height="720" alt="Screenshot 2025-11-15 194922" src="https://github.com/user-attachments/assets/0d9da82a-0e0f-4e2d-92a5-fec16e5de4bd" />
We can see that there are 4 peaks at frequences 1199Hz, 1721Hz, 1907Hz and 2256Hz. They are very close to some typical frequences used by sstv (1200Hz, 1700Hz, 1900Hz and 2300Hz).
The description also suggests us that we are looking at sstv because it's used by the ISS to send images. 
We can see the spectrogram to confirm if it's sstv.
<img width="1905" height="652" alt="Screenshot 2025-11-15 200251" src="https://github.com/user-attachments/assets/a1519465-9cc0-4873-9309-6ab3cd0250bd" />
We can see bright horizontal bands between 1400Hz and 2600Hz and a regular vertical pattern. We are fairly sure it's sstv now. 
Let's try to open the .wav file with qsstv to decode it and see the image.
<img width="1914" height="1015" alt="Screenshot 2025-11-15 201421" src="https://github.com/user-attachments/assets/b67aee82-0194-433d-b4f7-2d8d34db1da0" />
We can clearly see the flag *L3AK{SsTV_k1nd4_c00l!}*
