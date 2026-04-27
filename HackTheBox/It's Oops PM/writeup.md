# It's Oops PM

CTF: Hack The Box

Category: hardware

Author: Unknown

## Description

With the location of the underground bunker secured, the crew embarks on the next phase of their plan: assessing the feasibility of creating an underground tunnel to bypass the super mutant camp. They secure samples of water, soil, and air near the area. Scouring the wasteland for salvageable equipment, they stumble upon a dilapidated research facility where they find a cache of environmental sensors. Examining these sensors, the crew discovers they communicate with a satellite and contain a crypto-processor that encrypts their transmissions. After hand-drawing the diagrams and emulating the silicon chip's logic with VHDL, they uncover what appears to be a backdoor in the embedded logic that only triggers when a specific input is given to the system. Determined to exploit this, they turn to their tech specialist. Can you connect to the satellite and activate it?

## Overview

This challenge is composed by four .vhdl files and one .png file.

## Solution

The .png file shows a schematic of the device. The key.vhdl module simply gives a constant 16 bit value (KEY) as output. The encryption.vhdl module takes as input KEY and the user's input (INPUT), does some simple operations and gives a 16 bit value (ENCRYPTED) as output. The backdoor.vhdl module takes INPUT as input and checks if it's equal to a constant 16 bit value (BACKDOOR). If INPUT == BACKDOOR the module gives '1' as input, else '0'. The tpm.vhdl module implements the logic of the whole device. It checks the backdoor module's: if it's '0' the output is ENCRYPTED, if it's '1' the output is KEY. So the way to activate the backdoor is simply to send BACKDOOR as INPUT. I opened the connection and did that.





I got the flag *HTP{4_7yp1c41_53cu23_TPM_ch1p}*
