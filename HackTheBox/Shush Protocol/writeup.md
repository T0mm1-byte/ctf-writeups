# Shush Protocol

CTF: Hack The Box

Category: ICS

Author: unknown

## Description

The crew sets their sights on an abandoned fertilizer plant, a desolate structure rumored to hold a cache of ammonium nitrate—crucial for their makeshift explosives. Navigating through the plant’s crumbling corridors, they reach the main control room where a dusty, outdated PLC still hums faintly with power. The crew's hackers spring into action, connecting their equipment to the network of the PLC and starting the process of extracting data. They know that finding the password the control device uses to connect to the PLC is key to gaining full access to it. The hackers deploy network enumeration tools to scan for active devices on the plant's internal network. They meticulously sift through IP addresses, looking for clues that might reveal the password. After several tense hours, they pinpoint the device—a ruggedized industrial computer buried under layers of dust, still linked to the PLC that performs certain diagnostic operations under a custom protocol on a specific interval. Having captured the traffic from that connection the only thing that remains is to locate the packet that contains the secret information.

## Overview

This challenge is composed by a .pcapng file.

## Solution

I opened the .pcapng using wireshark and saw it's a modbus communication, a protocol used by PLCs. There are three types of messages: the "reading registers" with func code 3, the "reading coils" with func code 1 and some unkown type with func code 102. I filtered the traffic for types (frame[0x49] == 0x01/0x03/0x66) and watched the results. All the packets with func code 1 and 3 are equal and they read only 0s. There is one packet with func code 102 with a different size from the other 102s.




The flag is *HTB{50m371m35_cu570m_p2070c01_423_n07_3n0u9h7}*
