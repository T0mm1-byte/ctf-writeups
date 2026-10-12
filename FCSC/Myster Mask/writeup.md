# Myster Mask

CTF: FCSC 2022

Category: hardware

Authors: Mélissa and Ange

## Description

Myster Mask has written an implementation that sucks big time!

You will have to analyze the consumption traces of the beginning of an implementation of the AES made by Myster Mask. Will you be able to exploit these traces to make the difference?

The part to be targeted corresponds to the inversion step present in the calculation of the S-box in the first round of the AES. Only this step is implemented, it is not necessary to know the details of the AES since this challenge is specifically focused on this inversion step.

The consumption traces provided in the traces.npz file to be loaded with numpy correspond to the following line in the myster_mask.py code: ``py masked_inversion(L)

## Overview

This challenge is made of two .npz files, one for the traces and one for the inputs, a .txt file, that containt ciphertext and iv, and a .py file that describes the encryption and the leak.

## Solution

I opened the file .py to see what the implementation written by Myster Mask does. Substantially it xors each byte of the key with each byte of the input (that is a random 16 bytes block) to get a state; for each state's byte it does generate four random bytes; it divides the state's byte for each of the four random bytes in GF(256) and creates an array with the division result (that I will call inp) and the four bytes. So at the end there are 16 arrays of 5 elements each. Lastly there is the inversion alorithm that inverts in GF(256) each byte of each array. The power traces given are about the inversion phase. After learning a thing or two about modular arithmetic I understood the problem. Inverting 0 in GF gives always 0 and it's impossible to get 0 in a division if the dividend itself isn't 0. That means that if key[i] == input[i], for a generic i and a generic input, then their xor will be 0 and in the trace there will be the power consume of a 0. There are 5000 traces, that means nearly 20 input for each byte in each position. I decided to retrieve the key by bruteforcing a byte at a time, gathering all the traces which inputs have that byte in that position and observing the values around the point. A nearly perfect match between the traces means a correct byte for the key. But where should I've looked? I made a python script to analyze the traces: the points where there is the inversion must be pretty random through the traces while the others should be pretty standard since they rappresents the same operations.

```python
import sys
import numpy as np

n = 2000
HP_WINDOW = 201  
MIN_DIST = 40     
ZOOM = 400        

traces = np.load("traces.npz")["traces"][:n]

std = traces.std(axis=0)

s = std - std.mean()
ac = np.correlate(s, s, mode="full")[len(s) - 1:]
ac /= ac[0]
start = np.argmax(ac < 0)
period = start + np.argmax(ac[start:len(ac) // 2])

thr = np.median(std) + (std.max() - np.median(std)) / 2
peaks = []
for i in np.argsort(std)[::-1]:
    if std[i] < thr:
        break
    if all(abs(i - p) >= MIN_DIST for p in peaks):
        peaks.append(i)
peaks = np.sort(peaks)

print("positions:", peaks.tolist())
print("distances :", np.diff(peaks).tolist())
```

The results was better than I imagined: starting from time 36, all inversion are 56 times distant from each other. Knowing where to look it wasn't hard to put my plan to practice.

```python
import json
import itertools
import numpy as np
from Crypto.Cipher import AES

FIRST_PEAK = 36
STEP = 56
HALF = STEP // 2   
HP_WINDOW = 201    
TOP = 2           

traces = np.load("traces.npz")["traces"]
inputs = np.load("inputs.npz")["inputs"]


def highpass(t, w):
    kernel = np.ones(w) / w
    padded = np.pad(t, ((0, 0), (w // 2, w // 2)), mode="edge")
    smooth = np.array([np.convolve(row, kernel, mode="valid") for row in padded])
    return t - smooth

end = FIRST_PEAK + STEP * 15 + HALF
traces = highpass(traces[:, :end + HP_WINDOW], HP_WINDOW)[:, :end]

candidates = []
for i in range(16):
    peak = FIRST_PEAK + STEP * i
    window = traces[:, peak - HALF:peak + HALF]
    mean_all = window.mean(axis=0)
    var_all = window.var(axis=0)

    t_score = np.zeros(256)
    v_score = np.full(256, np.inf)
    for b in range(256):
        group = window[inputs[:, i] == b]
        if len(group) < 2:
            continue
        t = (group.mean(axis=0) - mean_all) / np.sqrt(var_all / len(group))
        t_score[b] = (t ** 2).mean()
        v_score[b] = (group.var(axis=0) / var_all).mean()

    order = np.argsort(t_score)[::-1]
    best, second = order[0], order[1]
    v_rank = int(np.sum(v_score < v_score[best]))
    candidates.append([int(b) for b in order[:TOP]])

out = json.load(open("output.txt"))
iv, c = bytes.fromhex(out["iv"]), bytes.fromhex(out["c"])
best_key = bytes(c[0] for c in candidates)

aes = AES.new(best_key, AES.MODE_CBC, iv=iv)
print(aes.decrypt(c).decode())
```

There was some noise so I had to use an approach based on the mean in an arbitrary interval but the script worked perfectly as planned.

The flag is *FCSC{8e29ba7aa273cc1b3ea74defe5972fd7ff4a0180acf790bddb25980289c81d60}*