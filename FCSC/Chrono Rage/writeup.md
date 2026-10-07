# Chrono Rage

CTF: FCSC 2024

Category: hardware

Author: rbe

## Description

Your friend has developed a small local daemon on his server which opens a listening socket on localhost and performs privileged actions when clients connect and authenticate with a PIN. Unfortunately, he recently had his server attacked, despite all the efforts he put into securing his daemon.

He provides you with the source code of this Python daemon: as you’ll see, to secure the communication of the PIN on the socket, he uses rotating AES session keys. It also provides you with a pcap capture corresponding to suspicious activity on the part of a local client detected by its constant monitoring. Unfortunately, he has lost the AES key used at the time of this capture, so he can’t provide it to you. Finally, he has obviously redacted the PIN in the source code: you don’t need to know this sensitive secret!

Can you help him out by explaining how the attacker did it, and that he needs to change his PIN and correct his code as quickly as possible?

## Overview 

This challenge is made of a .py file that show us how the server works and a .pcap file that conatins the interaction between the attacker and the server.

## Solution

The server takes max 16 bytes as input and uses AES CTR with a global counter to decrypt (or encrypt, is the same in CTR) the input and then calls a function to verify it. This function, check_password(), verifies one byte at the time doing a pretty long hash function on the byte of the encrypted input and the byte of the pin before comparing them. This is a clear vulnerability to a side channel attack based on time. Initially the attacker has to guess the pin length. check_password() does a check on length before starting the comparison so if the attacker's input has the right length it would take more time to get a response from the server since it would pass the length check and it's first byte will be processed. Following the TCP stream I saw that the attacker sent an input of different length until 12 bytes and from then he only sent inputs of 12 bytes so 12 is the right length. 



In the .pcap file the attacker packets have in info 55986 -> 5000 [PSH, ACK] and the response from the server is 5000 -> 55986 [PSH, ACK]. After discovering the length I didn't really know what the attacker was sending. The pin has 12 digits so he had to bruteforce 10 values for 12 times. I have to admit that initially I was lost because to do the bruteforce the attacker had to leak the keystream but I had no idea about how he does it and I spent much time trying to figure it out. Then I just supposed he already leaked it in some way and that all the inputs he sent after he discovered the length were bruteforce attempts. So I did a script to join all the exchange after the first 12 and measure the time interval between the attacker's message and the server's response.

```python
import struct
import sys

CLIENT_PORT = 55986
SERVER_PORT = 5000
PSH, ACK = 0x08, 0x10


def read_pcap(path):
    with open(path, "rb") as f:
        data = f.read()
    magic = data[:4]
    if magic in (b"\xd4\xc3\xb2\xa1", b"\x4d\x3c\xb2\xa1"):
        endian = "<"
    elif magic in (b"\xa1\xb2\xc3\xd4", b"\xa1\xb2\x3c\x4d"):
        endian = ">"
    nano = magic in (b"\x4d\x3c\xb2\xa1", b"\xa1\xb2\x3c\x4d")
    div = 1e9 if nano else 1e6

    off = 24
    while off + 16 <= len(data):
        ts_sec, ts_frac, incl_len, _ = struct.unpack(endian + "IIII", data[off:off + 16])
        off += 16
        yield ts_sec + ts_frac / div, data[off:off + incl_len]
        off += incl_len


def parse_tcp(frame):
    if len(frame) < 14:
        return None
    eth_type = struct.unpack("!H", frame[12:14])[0]
    ip_off = 14
    if eth_type == 0x8100:  
        eth_type = struct.unpack("!H", frame[16:18])[0]
        ip_off = 18
    if eth_type != 0x0800:
        return None
    ip = frame[ip_off:]
    ihl = (ip[0] & 0x0F) * 4
    total_len = struct.unpack("!H", ip[2:4])[0]
    if ip[9] != 6: 
        return None
    tcp = ip[ihl:]
    sport, dport = struct.unpack("!HH", tcp[:4])
    data_off = (tcp[12] >> 4) * 4
    flags = tcp[13]
    payload_len = total_len - ihl - data_off
    return sport, dport, flags, payload_len


def main(path="chrono-rage.pcap"):
    pairs = []     
    pending = None  

    for ts, frame in read_pcap(path):
        tcp = parse_tcp(frame)
        if tcp is None:
            continue
        sport, dport, flags, _ = tcp
        if flags != (PSH | ACK):  
            continue

        if sport == CLIENT_PORT and dport == SERVER_PORT:
            pending = ts
        elif sport == SERVER_PORT and dport == CLIENT_PORT:
            if pending is not None:
                pairs.append((pending, ts))
                pending = None

    deltas = [t_resp - t_req for t_req, t_resp in pairs]
    deltas = [round(d, 6) for d in deltas]
    print(deltas[:12])
    for i in range(12, len(deltas), 10):
        print(deltas[i:i + 10])

if __name__ == "__main__":
    main(*sys.argv[1:])
```

The result was pretty clear:



The first row shows how the time spent for a 12 byte input is much higher than the one for any other length. Then there are 12 rows of 10 time measurements (except for the last one that has only four). Each row has a clear spike that is the correct byte. I supposed that the bruteforce was done from "0" to "9" at each level so the index of the spike in each row is a digit of the pin and the index of the row is the index of that digit in the pin. I slightly modify the last code to use these information to print the flag. The only strange case was the last row since it has only 4 values and there wasn't a clear spike. I tried the highest value but the flag was wrong. Then I thought that the attacker stopped after 4 values because at the last interaction verified the last digit of the pin and so it should be 3. Although it makes sense I don't know how the attcker should have understood that since it's measurement isn't a spike. Maybe there is a problem in my script? I guess it will remain a mystery for me. Still, I got the flag so it doesn't really matter.

```python
    deltas = [t_resp - t_req for t_req, t_resp in pairs]
    deltas = [round(d, 6) for d in deltas]
    digits = list()
    for i in range(12, len(deltas), 10):
        guess = deltas[i:i + 10]
        if len(guess) < 10:
            digits.append(len(guess) - 1)
        else:
            digits.append(guess.index(max(guess)))
    print("FCSC{" + "".join(str(d) for d in digits) + "}")
```

The flag is *FCSC{825917304623}*