# SPAnosaurus

CTF: FCSC 2023

Category: hardware

Author: erdnaxe

## Description

The MegaSecure company has just released a security update for their servers. After analyzing the update, you notice that the editor now uses this code for exponentiation:

```C
unsigned long exp_by_squaring(unsigned long x, unsigned long n) {
  // n is the secret exponent
  if (n == 0) {
    return 1;
  } else if (n % 2 == 0) {
    return exp_by_squaring(x * x, n / 2);
  } else {
    return x * exp_by_squaring(x * x, (n - 1) / 2);
  }
}
```

You have access to a server on which you can run as a user exp_by_squaring(2, 2727955623) while measuring its power consumption. The exponent here is therefore n = 2727955623, or 10100010100110010100110010100111 in binary. This consumption trace is saved in user_trace.csv.

You have also managed to measure the energy consumption during exponentiation of an administrator data. This consumption trace is saved in trace_admin.csv. Can you find its secret exponent n?

The flag is in FCSC{1234567890} format with 1234567890 to be replaced by the secret exponent of the administrator written in decimal.

## Overview 

This challenge is made of two .csv file with power consumptions and a .png that shows them visually.

## Solution

First thing first, the exp_by_squaring function is literally the "square and multiply" function used by RSA algorithm and it's the part vulnerable to Simple Power Analysis (SPA, as the title suggests), a known vulnerability that permits to discover the exponent just looking at power traces since it considers one bit at a time and when it's 1 it does a multiplication more than when it's 0 and so it uses more power. From the image I saw that the square and multiply algorithm starts around sample 1500 so what happens before it's irrelevant. The idea is to relevate all the peaks in the last 500 samples and to give 1 to high peaks and 0 to smaller peaks. The problem is, as showed in the .png, that the medium power consumption increases over time so I couldn't use a stable treshold. To find the peaks I decided to detrend each sample by subtracting to him the median of the 25 samples before and after it. Doing this I could clearly see the peaks and I classified the single ones as 0 while multiple peaks in sequence as 1. After some tries I established the treshold for peaks at 0.015 and after verified the script with the user traces I launched it with the admin .csv.

```python
import csv
import statistics

TRACE = 'trace_admin.csv'
CROP = 1475      
W = 25          
THR = 0.015      
PAIR = 7         

with open(TRACE, mode='r') as f:
    content = list(csv.reader(f, delimiter=';'))[CROP:]

vals = []    
for i in range(25, len(content)):
    if i <= (len(content) - 26):
        points = [float(content[i + j][0]) for j in range(-25, 26)]
    else:
        points = [float(content[i + j][0]) for j in range(-25, len(content) - i)]
    delta = statistics.median(points)
    vals.append(float(content[i][0]) - delta) 

peaks = []
i = 1
while i < len(vals) - 1:
    if vals[i] > THR and vals[i] >= vals[i - 1] and vals[i] >= vals[i + 1]:
        peaks.append(i)
        i += 3
    else:
        i += 1

labels = {}  
i = 0
while i < len(peaks):
    if i + 1 < len(peaks) and peaks[i + 1] - peaks[i] <= PAIR:
        labels[peaks[i]] = '1'
        i += 2
    else:
        labels[peaks[i]] = '0'
        i += 1

bits = ''.join(labels[p] for p in peaks if p in labels).rstrip('0')
if bits:
    print('FCSC{' + str(int(bits, 2)) + '}')
```

I got the flag *FCSC{2327373741}*