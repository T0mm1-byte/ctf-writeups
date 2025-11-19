# Cube Sounds

CTF: CTFZone 2024 Quals(Jeopardy)

Category: Hardware

Author: Unknown

## Description

A strange signal was intercepted from the far side of the Moon by our Robot36 system. Perhaps this signal is the television of the future…

Who knows what is being transmitted. Maybe this is how extraterrestrial forces want to share their secrets with us?

## Overview

This challenge is composed by 10 .wav files. We have to analyze them

## Solution

Let's start opening all the files and looking at their spectrum

We can see that all of them have very similar spectrum with 4 peaks around 1200Hz, 1530Hz, 1900Hz and 2290Hz

<img width="732" height="695" alt="Screenshot 2025-11-19 101212" src="https://github.com/user-attachments/assets/4b0fed97-6436-4c10-9384-e1e8227d1ae8" />

The 4 peaks and the description suggest us that we are looking at sstv so let's try open them with qsstv

We see that every file produce a piece of an image and we have to arrange them to see the complete picture

But we can also see that the flag is mainly written in file 5.wav so we just need to find what file goes before and after that

Looking at all the images we find that the correct order is 7.wav -> 5.wav -> 3.wav

Let's concatenate them in a new file usin "sox 7.wav 5.wav 3.wav flag.wav" from terminal and have a look at flag.wav with qsstv

<img width="1478" height="953" alt="Screenshot 2025-11-19 100611" src="https://github.com/user-attachments/assets/715af328-6912-4d3f-adab-f219d1c275ff" />

We can clearly see the flag *CTFZone{s1gn@l_dEtected!}*

