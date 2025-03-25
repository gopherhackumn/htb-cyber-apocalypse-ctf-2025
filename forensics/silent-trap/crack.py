from collections import defaultdict
from tqdm import tqdm
key = [168, 115, 174, 213, 168, 222, 72, 36, 91, 209, 242, 128, 69, 99, 195, 164, 238, 182, 67, 92, 7, 121, 164, 86, 121, 10, 93, 4, 140, 111, 248, 44, 30, 94, 48, 54, 45, 100, 184, 54, 28, 82, 201, 188, 203, 150, 123, 163, 229, 138, 177, 51, 164, 232, 86, 154, 179, 143, 144, 22, 134, 12, 40, 243, 55, 2, 73, 103, 99, 243, 236, 119, 9, 120, 247, 25, 132, 137, 67, 66, 111, 240, 108, 86, 85, 63, 44, 49, 241, 6, 3, 170, 131, 150, 53, 49, 126, 72, 60, 36, 144, 248, 55, 10, 241, 208, 163, 217, 49, 154, 206, 227, 25, 99, 18, 144, 134, 169, 237, 100, 117, 22, 11, 150, 157, 230, 173, 38, 72, 99, 129, 30, 220, 112, 226, 56, 16, 114, 133, 22, 96, 1, 90, 72, 162, 38, 143, 186, 35, 142, 128, 234, 196, 239, 134, 178, 205, 229, 121, 225, 246, 232, 205, 236, 254, 152, 145, 98, 126, 29, 217, 74, 177, 142, 19, 190, 182, 151, 233, 157, 76, 74, 104, 155, 79, 115, 5, 18, 204, 65, 254, 204, 118, 71, 92, 33, 58, 112, 206, 151, 103, 179, 24, 164, 219, 98, 81, 6, 241, 100, 228, 190, 96, 140, 128, 1, 161, 246, 236, 25, 62, 100, 87, 145, 185, 45, 61, 143, 52, 8, 227, 32, 233, 37, 183, 101, 89, 24, 125, 203, 227, 9, 146, 156, 208, 206, 194, 134, 194, 23, 233, 100, 38, 158, 58, 159]

def decrypt(data:bytes)->bytes:
    a1 = [0] * 256
    a2 = [0] * 256
    for i in range(256):
        a1[i] = key[i % len(key)]
        a2[i] = i
    num = 0
    for i in range(256):
        num = (num + a2[i] + a1[i]) % 256
        num2 = a2[i]
        a2[i] = a2[num]
        a2[num] = num2
    num = 0
    num3 = 0
    a3=[]
    for i in range(len(data)):
        num3 += 1
        num3 %= 256
        num += a2[num3]
        num %= 256
        num2 = a2[num3]
        a2[num3] = a2[num]
        a2[num] = num2
        num4 = a2[(a2[num3] + a2[num]) % 256]
        a3.append( data[i] ^ num4)
    return bytes(a3 )

import pickle
import base64
import pyshark

capture = pyshark.FileCapture('capture.pcapng')

# for packet in capture:
#     try:
#         if "FETCH" in packet.imap.line:
#             print("SHIET")
#             print(packet.text)
#             print(decrypt(base64.b64decode(packet.text)))

#     except: pass

# packet_info = dict()

# for packet in capture:
#     if hasattr(packet, 'imap') and hasattr(packet.imap, 'request_command') and packet.imap.request_command == "APPEND":
#         packet_info[packet.tcp.stream] = dict(
#             imap_number=packet.number,
#             stream=packet.tcp.stream,
#         )

# print(packet_info)

# # packet_info = {744: {'stream': 16}, 749: {'stream': 16}, 912: {'stream': 22}, 980: {'stream': 25}, 1103: {'stream': 28}, 1331: {'stream': 35}, 2025: {'stream': 54}, 2122: {'stream': 57}, 2229: {'stream': 61}, 2361: {'stream': 64}, 2580: {'stream': 69}, 2691: {'stream': 74}, 2974: {'stream': 85}, 3621: {'stream': 97}}
# all_data = defaultdict(list)

# for packet in capture:
#     try:
#         if packet.tcp.stream in packet_info:
#             all_data[packet.tcp.stream].append(packet.tcp.segment_data)
#     except: pass

# all_data2 = dict()

# for number, data in all_data.items():
#     data = "".join(c.replace(":", "") for c in data)
#     data = bytes.fromhex(data)
#     all_data2[number] = data

# with open("data2.pkl", "wb") as f:
#     pickle.dump(all_data2, f)


def print_output():
    with open("data2.pkl", "rb") as f:
        all_data2 = pickle.load(f)

    for number, data in all_data2.items():
        data2 = base64.b64decode(data)
        print(decrypt(data2).decode())

# while True:
#     line = input("> ")
#     print(decrypt(base64.b64decode(line)).decode())

# s= s.split("\n")
# s = filter(lambda c: "," in c, s)
# s = map(lambda c: c.split(",")[1],s )
# s = filter(lambda c: "["not in c, s)
# s= map(lambda c: decrypt(base64.b64decode(c)),s)
# s= list(s)
# # print(b"\n".join(s).decode())

for packet in tqdm(capture):
    try:
        if hasattr(packet, 'imap'):
            print(decrypt(base64.b64decode(packet.text)))
    except: pass
