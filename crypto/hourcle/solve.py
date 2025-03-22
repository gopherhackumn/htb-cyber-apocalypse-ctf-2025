from pwn import *
import string

# p = process("python server.py", shell=True)
p = remote("94.237.57.114", 55099)

print(p.recvline())
p.recvuntil(b" :: ")

ALPHABET = string.ascii_letters + string.digits

def encrypt(s):
    p.sendline(b"1")
    p.recvuntil(b" :: ")
    p.sendline(s.encode())
    # print(p.recvline())
    # print(p.recvline())
    # print()
    res = p.recvuntil(b" :: ")
    return bytes.fromhex(res.split(b"scrolls: ")[1].split(b"\n")[0].decode())

def block(s, n): return s[n * 16 : (n + 1) * 16]

def format(b, k=32):
    s = b.hex()
    return " ".join(s[i:i+k] for i in range(0, len(s), k))

known = ""
for i in range(20):
    prefix = "A" * (3 * 16 - 1 - len(known))
    # print(len(prefix))
    reference = encrypt(prefix)
    print("REFER", "=", "=", format(reference))

    for c in ALPHABET:
        modded = encrypt(prefix + known + c)
        block_looking = 2 - len(known) // 16
        found = block(modded, 2) == block(reference, 2)
        if found:
            print("FOUND", "*" if found else " ", c, format(modded))
            known += c
            break

print("known", len(known), known, format(known.encode()))

p.sendline(b"2")
print(p.recvuntil(b" :: "))
p.sendline(known.encode())
print(p.recvall())
