# Strange Transmission(beginner)

CTF: L3akCTF 2025(Jeopardy)

Category: hardware

Authors: Suvoni

## Description

I received this strange transmission and I'm not sure what to make of it! Weird beeps, static noise, then silence. Can you help me figure out what it all means?

## Overview

This challenge is composed by a .wav file. We have to analyze it.

## Solution

Let's start analyzing the spectrum with Audacity

We can see one peak at 1003Hz. Using just one frequence it may be morse code

<img width="751" height="705" alt="Screenshot 2025-11-17 173659" src="https://github.com/user-attachments/assets/f4708fd9-9d9e-4dce-aae3-029e27f5fffc" />

Now let's look at the spectrogram

We can see two regions: the first one is just a repeated peak while the second, at the end of the file, looks a little weird

<img width="1900" height="571" alt="Screenshot 2025-11-17 173729" src="https://github.com/user-attachments/assets/9347f4a2-aff9-4084-98e8-22b2610544b5" />

If we expand that area we can see that it's the final part of the flag

<img width="1202" height="255" alt="Screenshot 2025-11-17 173425" src="https://github.com/user-attachments/assets/4d0ebc95-4441-4f2d-9fe3-5fff4c73a502" />

Now let's see if the first part is really morse code using https://morsecode.world/international/decoder/audio-decoder-adaptive.html

<img width="1273" height="762" alt="Screenshot 2025-11-17 174843" src="https://github.com/user-attachments/assets/c5726337-42e1-4558-b24a-fb950c852413" />

We can see it was really morse code and the message is "oh wow you found our secret morse code audio, well done, here is the first half of the flag: L3AK{welc0m3_t0_th3_h4rdw4r3_rf_"

Now we just have to concatenate the two flag pieces

The flag is *L3AK{welc0m3_t0_th3_h4rdw4r3_rf_c4teg0ry_w3_h0p3_you_h4ve_fun!}*





