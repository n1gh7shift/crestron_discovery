#!/usr/bin/env python3

import socket
import time
import re

PORT = 41794
BROADCAST_IP = "255.255.255.255"
REPEATS = 3
TIMEOUT = 5
PACKET_LEN = 266

hostname = socket.gethostname().encode()

# Build discovery packet
packet = (
    b"\x14\x00\x00\x00\x01\x04\x00\x03\x00\x00"
    + hostname
    + b"\x00\x00"
)
packet += b"\x00" * (PACKET_LEN - len(packet))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", PORT))
sock.settimeout(TIMEOUT)

print(
    "IP_ADDRESS        HOSTNAME               DEVICE_TYPE   FW_VERSION       MAC_ADDRESS"
)
print(
    "----------------------------------------------------------------------------------"
)

seen = set()

# Send discovery packets
for _ in range(REPEATS):
    sock.sendto(packet, (BROADCAST_IP, PORT))
    time.sleep(0.2)

start = time.time()

while time.time() - start < TIMEOUT:
    try:
        data, (ip, _) = sock.recvfrom(2048)
    except socket.timeout:
        break

    # Only responses start with 0x15 00
    if not data.startswith(b"\x15\x00"):
        continue

    text = data.decode("ascii", errors="ignore")

    # Hostname
    host = None
    for part in data.split(b"\x00"):
        if re.fullmatch(rb"[A-Z0-9_-]{4,}", part):
            host = part.decode()
            break

    if not host:
        continue

    # Device type (e.g. TSW-1060, RMC4)
    dev_match = re.search(r"([A-Z0-9-]+) \[v", text)
    if not dev_match:
        continue
    device_type = dev_match.group(1)

    # Firmware version
    fw_match = re.search(r"\[v([0-9.]+)", text)
    if not fw_match:
        continue
    fw_version = fw_match.group(1)

    # MAC address
    mac_match = re.search(r"@E-([0-9a-f]{12})", text)
    if not mac_match:
        continue

    mac_raw = mac_match.group(1)
    mac = ":".join(mac_raw[i:i + 2] for i in range(0, 12, 2))

    key = (ip, mac)
    if key in seen:
        continue
    seen.add(key)

    print(
        f"{ip:<17} {host:<21} {device_type:<13} {fw_version:<16} {mac}"
    )

sock.close()