# CryptoBro En Detresse

CTF: FCSC 2025

Category: hardware

Author: Danhia

## Description

To recover the PIN of my super-secure cryptocurrency wallet, which contains 0.00000001 BTC, I bought a top-tier oscilloscope for 10,000 euros. But I don’t really know what to do with all these traces. Maybe you could give me a hand?

I’ve acquire one trace for each possible PIN, but to avoid triggering a security mechanism and thus erasing the wallet, I turn off the power after a few microseconds after each attempt.

Note: The cryptobro.tar.xz archive contains files named trace_XXXX.npy, where XXXX corresponds to the PIN used to generate the trace. Once you have recovered the PIN, wrap it between FCSC{} to get the flag. For example, if the PIN were 1234, the flag would be FCSC{1234}

## Overview

As said in the description, the challenge is made of 10000 .npy files and each of them represents the voltage used for a specific pin.

## Solution

Since it was very likely that the wallet checks a digit at the time my idea was to visualize a trace for each first digit and see if there were some differences between a trace and the other nine. To do so I wrote a python script.

```python
import numpy as np
import matplotlib.pyplot as plt

idx = "1001"

path = f"traces/trace_{idx}.npy"
data = np.load(path)

plt.figure(figsize=(12, 5))
plt.plot(data, linewidth=0.7)
plt.title(f"trace_{idx}")
plt.xlabel("tempo")
plt.ylabel("ampiezza")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

There was a pretty clear difference between 9001 and the other x001 and that made me understand the meaning of some sequences. I circled in blue the spike that indicates the start of the checking algorithm, in green the pattern that indicates a correct digit and in red the pattern that indicates an incorrect digit.



In any other x001 there is only the incorrect sequence while in 9001 there is a correct pattern followed by an incorrect pattern, that means that 9 is the first digit. I followed this method bruteforcing by hand a digit at a time, knowing that I would have got the flag in max 40 tries, until I got the right combination with four correct patterns.



To generalize the method to N digits I wrote a script that bruteforce a digit at a time and recognize the different one by the position on the time axis of the peaks over 0.4 since a correct pattern pushes the peaks on the right.

```python
import numpy as np

THRESHOLD = 0.4


def peak_positions(idx):
    data = np.load(f"traces/trace_{idx}.npy")
    return set(np.where(data > THRESHOLD)[0].tolist())


def build_index(found, pos, x):
    digits = list(found)
    digits[pos] = str(x)
    for p in range(pos + 1, 4):
        digits[p] = "1" if p == 3 else "0"
    return "".join(digits)


def odd_one_out(indices):
    peaks = {idx: peak_positions(idx) for idx in indices}
    scores = {}
    for idx in indices:
        scores[idx] = sum(len(peaks[idx] & peaks[other])
                          for other in indices if other != idx)
    return min(scores, key=scores.get)


def main():
    found = ["0", "0", "0", "1"]  
    for pos in range(4):
        candidates = [build_index(found, pos, x) for x in range(10)]
        anomala = odd_one_out(candidates)
        found[pos] = anomala[pos]
    print("FCSC{" + "".join(found) + "}")


if __name__ == "__main__":
    main()
```

The flag is *FCSC{9466}*