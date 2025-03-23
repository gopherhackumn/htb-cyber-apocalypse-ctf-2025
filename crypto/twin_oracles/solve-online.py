from pwn import *

r = remote("94.237.55.61", 50411)
# r = process(["python3", "server.py"])

print(r.recvuntil(b"M = "))
print(line := r.recvline())
m = int(line.strip())

len_seq = 40
seq = []
for _ in range(len_seq):
    print(r.recvuntil(b"> "))
    r.sendline(b"2")

    print(r.recvuntil(b"Submit your encrypted scripture for the Seers' judgement: "))
    r.sendline(b"1")

    print(r.recvuntil(b"The Seers whisper their answer:"))
    print(line := r.recvline())
    seq.append(int(line.strip()))

seed = 0
for x0 in range(m):
    x = x0

    valid = True
    for actual in seq:
        x = pow(x, 2, m)
        if 1 - (x % 2) != actual:
            valid = False
            break

    if valid:
        print("Seed found", x0)
        seed = x0
        break

state = seed
for _ in range(len_seq):
    state = pow(state, 2, m)

# RSA
print(r.recvuntil(b"> "))
r.sendline(b"1")

print(r.recvuntil(b"n = "))
print(line := r.recvline())
n = int(line.strip())
e = 65537

print(r.recvuntil(b"The ancient script has been sealed: "))
print(line := r.recvline())
c = int(line.strip())

res_msb = []
res_lsb = []
i = 100
j = 0
while True:
    state = pow(state, 2, m)

    # print(r.recvuntil(b"> "))
    r.sendline(b"2")

    print(r.recvuntil(b"Submit your encrypted scripture for the Seers' judgement: "))
    if state % 2 == 0:
        cc = bytes(hex(c * pow(2, e * i, n) % n)[2:], "utf-8")
        i += 1
    else:
        cc = bytes(hex(c * pow(2, -e * j, n) % n)[2:], "utf-8")
        j += 1
    r.sendline(cc)  # ciphertext for 2P, 4P, etc
    print("SENT", cc)

    print(r.recvuntil(b"The Seers whisper their answer: "))
    print(line := r.recvline())
    b = int(line.strip())

    if state % 2 == 0:
        res_msb.append(b)
        print("MSB:", "".join(map(str, res_msb)))
    else:
        res_lsb.append(b)
        print("LSB:", "".join(map(str, res_lsb))[::-1])
