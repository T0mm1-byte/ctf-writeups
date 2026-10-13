# SCHaiku

CTF: FCSC 2021

Category: hardware

Author: Guena

## Description

An embedded device, a tablet, that has a secure exchange system with a data server has just been analyzed by one of our interns on side channels.

To authenticate the server, a challenge-response system is implemented as defense-in-depth. More specifically, this step goes as follows. The server sends a challenge P (a random 128-bit plaintext) to the tablet. The tablet computes a ciphertext C from P and a secret key K (shared between the tablet and the server) with:

C = AES128-ECB(K, P)
and then sends C to the server to authenticate itself. (The same steps are performed in the other direction to reach mutual authentication).

In parallel to the encryption, the tablet displays an image on its screen. Our colleague noticed that interference appeared on some part of the image during this computation.

Can you find the key from these potential information leaks?

To do so, he has prepared an animated PNG (SCHaiku.png) showing the reference image and those corresponding to different encryptions. The ordered list of challenges corresponding to each of the parasitized images is also given (challenges.txt).

Additional information: the display is done using elementary blocks of 4 pixels. The synchronization between the display of the elementary blocks and the cryptographic computation is not perfect: the only thing we can be sure of is that the interference only occurs on exactly one pixel among the 4 in a block.

The flag is obtained by finding the challenge corresponding to this ciphertext sent by the server: d048821b99bca6758115e7a403bff427

## Overview

This challenge is made of a .txt file, that contains 50 plaintext fo 16 bytes, and a .png file that contains the leaky screen.

## Description

First thing I did was to check the number of frames of the .png: they are 51. The first one is just black so its useless while the others are the leaks of an encryption. I extracted the frames and put them in a directory named "SCHaiku_frames". The screen is just a small part of each frame. Each square is a 140x140 pixel matrix. As the description suggests, a square should be consider as a 70x70 pixel matrix where each pixel is actually a 2x2 square of pixels. In each 2x2 square there is always only one pixel that isn't black. The 50 plaintext, the 50 leaks and AES-128 ECB made me think about another challenge I solved that I will link here and that I suggest to read before going on with this writeup: https://github.com/T0mm1-byte/ctf-writeups/tree/main/ACSC/PWR_Tr4ce. I thought the vulnerability may be the same, that means a leak of Sbox[input[i]^key[i]] but instead of the power consumption this time I have a pixel matrix. There are 4900 2x2 squares and I thought that 16 of them might be the leaks I was looking for to retrieve the key using a CPA. While in PWR_Tr4ce I had 5000 timestamps this time I had 4900 2x2 pixel squares that I could manage in the same exact way. But what parameter should I use to correlate with the Hamming Weight? The description says that the position of a non-black pixel in its 2x2 matrix is random for a synchronization problem but they should all be the same so I thought it was irrelevant and that I could simply identify a 2x2 matrix with the RGBA values of its non-black pixel. R is 0 for all non-black pixels so it doesn't leak information. I still had G, B and A from which to choose. In my head A was the most likely but I decided to do the CPA for each of them and their sums (G, B, A, G+B, G+A, B+A, G+B+A). I've already explained what a CPA is in the link I put here but I will refresh your memory just in case: I decided to recover one byte at the time of the key trying all its 256 possible values, xoring them with all the plaintext's bytes in the same position, doing the substitution with the Sbox, calculating its hamming weight and then calculating the Pearson's correlation coefficient between the hamming weight and each parameter of a 2x2 pixel square. A very high coefficient means a very strong correlation between the quantities and that the key's byte is probably the right one. At the end I found my idea was correct and that the right parameter is G, the correlation between its value in some squares and the hamming weigth are nearly perfect and the key is fully ascii printable. Here's the script I used:

```python
import ast
import itertools
import sys
from pathlib import Path
from Crypto.Cipher import AES
import numpy as np
from PIL import Image

FRAMES_DIR = Path("SCHaiku_frames")
CHALLENGES = Path("challenges.txt")

X0, Y0, SIZE = 475, 450, 140    # frame's central square 
NB = SIZE // 2                    
BG = np.array([0, 5, 17, 255])  # background RGBA value

SBOX = np.array([
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
], dtype=np.uint8)
assert len(set(SBOX.tolist())) == 256 and SBOX[0x53] == 0xed
HW = np.array([bin(x).count("1") for x in range(256)], dtype=np.float64)


def load_plaintexts():
    pts = ast.literal_eval(CHALLENGES.read_text())
    return np.array([[int(b, 16) for b in pt] for pt in pts], dtype=np.uint8)


def load_traces(n):
    traces = np.empty((n, NB * NB, 4), dtype=np.float64)
    for i in range(n):
        img = np.asarray(Image.open(FRAMES_DIR / f"frame_{i + 1:02d}.png").convert("RGBA"))
        sq = img[Y0:Y0 + SIZE, X0:X0 + SIZE].astype(np.int64)
        # (70, 2, 70, 2, 4) -> (70, 70, 4 sub-pixels, 4 channels)
        blocks = sq.reshape(NB, 2, NB, 2, 4).transpose(0, 2, 1, 3, 4).reshape(NB, NB, 4, 4)
        lit = np.any(blocks != BG, axis=-1)
        traces[i] = blocks[lit].reshape(NB * NB, 4)
    return traces

def standardize(x, axis):
    x = x - x.mean(axis=axis, keepdims=True)
    norm = np.sqrt((x ** 2).sum(axis=axis, keepdims=True))
    norm[norm == 0] = np.inf
    return x / norm

def cpa(pts, trace):
    t = standardize(trace, axis=0)                                  
    keys = np.arange(256, dtype=np.uint8)
    hyp = HW[SBOX[pts[:, :, None] ^ keys[None, None, :]]]          
    hyp = standardize(hyp, axis=0)
    return np.einsum("nbk,np->bkp", hyp, t)

def analyse(name, corr):
    a = np.abs(corr)
    per_key = a.max(axis=2)                     
    key, rows = [], []
    for b in range(16):
        order = np.argsort(per_key[b])[::-1]
        k1, k2 = order[0], order[1]
        poi = int(a[b, k1].argmax())
        r1, r2 = per_key[b, k1], per_key[b, k2]
        rows.append((b, k1, r1, np.sign(corr[b, k1, poi]), k2, r2, r1 / r2, poi))
        key.append(int(k1))
    return bytes(key), rows

def main():
    pts = load_plaintexts()
    n = len(pts)
    raw = load_traces(n)

    chans = {"G": raw[:, :, 1], "B": raw[:, :, 2], "A": raw[:, :, 3]}
    params = {}
    for r in range(1, 4):
        for combo in itertools.combinations("GBA", r):
            params["+".join(combo)] = sum(chans[c] for c in combo)

    noise_max = 5 / np.sqrt(n)      # to filter noise

    def is_strong(row):
        return row[2] > noise_max and row[6] > 1.15

    summary = []
    for name, trace in params.items():
        key, rows = analyse(name, cpa(pts, trace))
        strong = [r for r in rows if is_strong(r)]
        mean_r = np.mean([r[2] for r in rows])
        signs = {r[3] for r in rows}
        summary.append((len(strong), mean_r, name, key))

    summary.sort(key=lambda s: (s[0], s[1]), reverse=True)
    best = summary[0]

    aes = AES.new(best[3], AES.MODE_ECB)
    print(aes.decrypt(bytes.fromhex("d048821b99bca6758115e7a403bff427")).decode())


if __name__ == "__main__":
    main()
```

The flag is *FCSC{mizunooto!}*