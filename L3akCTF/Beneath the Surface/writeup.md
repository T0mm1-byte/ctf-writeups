# Beneath the Surface

CTF: L3akCTF 2025(jeopardy)

Category: hardware

Author: Suvoni

## Description

On the surface, this signal is nothing but meaningless noise — a mere whisper of the wind. But dive deeper into this transmission, and a storm begins to take shape, with gray skies gathering on the horizon. Can you navigate through the static and uncover what lurks beneath the surface of the wav — before it’s too late?

## Overview

This challenge is composed by a .wav file.

## Solution

I started by opening the file with Audacity to look at the spectrum.

<img width="729" height="666" alt="Screenshot 2025-11-20 115407" src="https://github.com/user-attachments/assets/2360ba74-23de-49df-a0f2-7a6b0535215a" />

There are 4 peaks at 299Hz, 449Hz, 1449Hz and 2279Hz.
Looking at the spectrogram I sea that only 1449Hz and 2279Hz are really part of the signal

<img width="1905" height="426" alt="Screenshot 2025-11-20 115433" src="https://github.com/user-attachments/assets/15958e55-ad37-411b-80cd-8824bb8c4149" />

I used "strings beneath_the_surface.wav > metadata.txt" to see the metadata.

<img width="368" height="225" alt="Screenshot 2025-11-20 181357" src="https://github.com/user-attachments/assets/c015f354-1067-48f1-9b35-14145305a527" />

It's wefax. It makes sense because the peaks are very close to the usual frequencies used by wefax (1500Hz and 2300Hz). I used fldigi to recover the image.

<img width="1049" height="637" alt="Screenshot 2025-11-20 183827" src="https://github.com/user-attachments/assets/91f89c5c-f5e4-44bf-a346-17750c1670d6" />

I could clearly see the flag *L3AK{R4diOF4X_1S_G00d_4_ImAG3_Tr4nsM1sSiON}*
