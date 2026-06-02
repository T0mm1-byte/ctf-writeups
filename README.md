This repo is made to store the hardware challenges I solved. In each challenge's directory there are:
- writeup.md: the file that explains my solution
- sources.md: the links to the web pages I think may be useful to learn everything needed to solve the challenge (no AI slop). It may be absent for particularly easy challenges.
- everything else is the attachments of the challenge. It may be a zip file or the content of a zip file I exctracted, it depends. Still, there is everything needed to try to solve the challenge. If the challenge is not freely accessible (es. HackTheBox VIP challs) there would be writeup.md and eventually sources.md but not the attachments.

I post a challenge only if I have the solution. About remote challenges there are three cases:
- I've played the ctf so I could access the remote resources.
- I haven't played the ctf but the remote resources are needed only to get the flag, that means I have to understand the vuln and how to exploit it from the attachments and then do it on the remote source to get the flag.
- I haven't played the ctf and the remote resources are needed to understand vuln and or exploit.
  
In the third case I don't even bother to try it, there's no fun if I can't solve it. In the second case two things may happen:
- There is a public writeup with the flag made by someone that played the ctf. In this case I confront the writeup with my solution and pretend to have found the flag by myself if I found the right solution.
- There isn't a public writeup. In this case my writeup has the solution I found but without a flag and without the chance to know if my idea is right or wrong.

To better organize this repo I made a list of the challenges that can be found here. They are sorted by type and difficulty.

The types are:
- Side Channel Attack:retrieve the flag or a crypto key from a set of measurments.
- Digital signals/Protocols: analyzing digital signals and protocols.
- Firmware Reversing: reversing firmware.
- RF: analyzing analogical/RF signals.
- HDL/PLC/PCB Reversing: reversing HDL/PLC languages, PCBs and electronic circuits.

Note that one challenge may have attributes of more types. In that case I will decide where to put it based on what I think is the dominant type.

The difficulty levels are:
- very easy: no skills needed, anyone could solve these
- easy: pretty straightforward application of a well-known concept
- medium: more elaborated challs, they requires more steps to being solved and treats more advanced/niche concepts 
- hard: elaborated challs, they requires true skills and a deep understanding of the argument
- nightmare: the name is self-explainatory

Note that the difficulty level is chosen only by myself so it may differ from the difficulty level chosen by the chall's author.

| Challenge | Type | Difficulty |
|-----------|------|------------|
| [PWR_Tr4ce](https://github.com/T0mm1-byte/ctf-writeups/tree/main/ACSC/PWR_Tr4ce) | Side Channel Attack | Medium |
| [An4lyz3_1t](https://github.com/T0mm1-byte/ctf-writeups/tree/main/ACSC/An4lyz3_1t) | Logic Signals/Protocols | Very Easy |
| [Debug](https://github.com/T0mm1-byte/ctf-writeups/tree/main/HackTheBox/Debug) | Logic Signals/Protocols | Very Easy |
| [Debugging Interface](https://github.com/T0mm1-byte/ctf-writeups/tree/main/HackTheBox/Debugging%20Interface) | Logic Signals/Protocols | Very Easy |
| [Shush Protocol](https://github.com/T0mm1-byte/ctf-writeups/tree/main/HackTheBox/Shush%20Protocol) | Logic Signals/Protocols | Very Easy |
| [Brick By Brick](https://github.com/T0mm1-byte/ctf-writeups/tree/main/UMassCTF/BrickByBrick) | Logic Signals/Protocols | Easy |
| [Alpha](https://github.com/T0mm1-byte/ctf-writeups/tree/main/BYUCTF/Alpha) | Logic Signals/Protocols | Medium |
| [gasgasgas](https://github.com/T0mm1-byte/ctf-writeups/tree/main/CrewCTF/gasgasgas) | Logic Signals/Protocols | Medium |
| [Mission Pinpossible](https://github.com/T0mm1-byte/ctf-writeups/tree/main/HackTheBox/Mission%20Pinpossible) | Logic Signals/Protocols | Medium |
| [Sal](https://github.com/T0mm1-byte/ctf-writeups/tree/main/BYUCTF/Sal) | Logic Signals/Protocols | Medium |
| [Smart Coffee](https://github.com/T0mm1-byte/ctf-writeups/tree/main/QnQSecCTF/SmartCoffee) | Firmware Reversing | Very Easy |
| [Firmware](https://github.com/T0mm1-byte/ctf-writeups/tree/main/GreyCTF/Firmware) | Firmware Reversing | Very Easy |
| [The Needle](https://github.com/T0mm1-byte/ctf-writeups/tree/main/HackTheBox/The%20Needle) | Firmware Reversing | Easy |
| [picopico](https://github.com/T0mm1-byte/ctf-writeups/tree/main/ACSC/picopico) | Firmware Reversing | Easy |
| [Dumb Internet Of Things](https://github.com/T0mm1-byte/ctf-writeups/tree/main/TyphoonConCTF/DumbInternetOfThings) | Firmware Reversing | Medium |
| [Crash Landing](https://github.com/T0mm1-byte/ctf-writeups/tree/main/DownUnderCTF/Crash-Landing) | Firmware Reversing | Medium |
| [Celestial](https://github.com/T0mm1-byte/ctf-writeups/tree/main/L3akCTF/Celestial(radio)) | RF | Easy |
| [Communication Gateway](https://github.com/T0mm1-byte/ctf-writeups/tree/main/L3akCTF/Communication%20Gateway(radio)) | RF | Easy |
| [CubeSounds](https://github.com/T0mm1-byte/ctf-writeups/tree/main/CTFZone/Cube%20Sounds) | RF | Easy |
| [Strange Transmission](https://github.com/T0mm1-byte/ctf-writeups/tree/main/L3akCTF/Strange%20Transmission(beginner)) | RF | Easy |
| [Beneath the Surface](https://github.com/T0mm1-byte/ctf-writeups/tree/main/L3akCTF/Beneath%20the%20Surface) | RF | Medium |
| [RFID_demod](https://github.com/T0mm1-byte/ctf-writeups/tree/main/ACSC/RFID_demod) | RF | Medium |
| [Layout](https://github.com/T0mm1-byte/ctf-writeups/tree/main/L3akCTF/Layout(baby)) | HDL/PLC/PCB Reversing | Very Easy |
| [Critical Flight](https://github.com/T0mm1-byte/ctf-writeups/tree/main/HackTheBox/Critical%20Flight) | HDL/PLC/PCB Reversing | Very Easy |
| [Not Your Karnaugh Diagram](https://github.com/T0mm1-byte/ctf-writeups/tree/main/QnQSecCTF/NotYourKarnaughDiagram) | HDL/PLC/PCB Reversing | Very Easy |
| [Low Logic](https://github.com/T0mm1-byte/ctf-writeups/tree/main/HackTheBox/Low%20Logic) | HDL/PLC/PCB Reversing | Easy |
| [It's Oops PM](https://github.com/T0mm1-byte/ctf-writeups/tree/main/HackTheBox/It's%20Oops%20PM) | HDL/PLC/PCB Reversing | Easy |
| [Spy PLC](https://github.com/T0mm1-byte/ctf-writeups/tree/main/IranTechOlympicsCTF/Spy_PLC) | HDL/PLC/PCB Reversing | Easy |
| [eXORbitant](https://github.com/T0mm1-byte/ctf-writeups/tree/main/L3akCTF/eXORbitant) | HDL/PLC/PCB Reversing | Medium |
| [VHDLCG](https://github.com/T0mm1-byte/ctf-writeups/tree/main/L3akCTF/VHDLCG(crypto)) | HDL/PLC/PCB Reversing | Medium |
