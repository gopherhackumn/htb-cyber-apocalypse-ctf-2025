the first half constructs some code at runtime, then calls it

- gdb challenge
- breakpoint at mmap
- finish
- now ur in main
- x/50i $rip until u find the call rax instruction, break on it

i checkpointed here to make it easy to come back to

- enter the constructed code, and do a x/50i $rip again
- look at the code. seems like it's xor'ing 0xbeefcafe against ur input and comparing to some specified memory
- i dug that memory out using x/32x

```
0x7ffff7fc0084: 0xb6    0x9e    0xad    0xc5    0x92    0xfa    0xdf    0xd5
0x7ffff7fc008c: 0xa1    0xa8    0xdc    0xc7    0xce    0xa4    0x8b    0xe1
0x7ffff7fc0094: 0x8a    0xa2    0xdc    0xe1    0x89    0xfa    0x9d    0xd2
0x7ffff7fc009c: 0x9a    0xb7    0x00    0x00    0x00    0x00
```

just write a simple python script to reverse

```
>>> desired = b'\xb6\x9e\xad\xc5\x92\xfa\xdf\xd5\xa1\xa8\xdc\xc7\xce\xa4\x8b\xe1\x8a\xa2\xdc\xe1\x89\xfa\x9d\xd2\x9a\xb7'
>>> t = []
>>> for i in range(0, 26, 4):
...  for j in range(4):
...   if i + j >= 26: break
...   t.append(b"\xfe\xca\xef\xbe"[j] ^ desired[i + j])
...
>>> t
[72, 84, 66, 123, 108, 48, 48, 107, 95, 98, 51, 121, 48, 110, 100, 95, 116, 104, 51, 95, 119, 48, 114, 108, 100, 125]
>>> bytes(t)
b'HTB{l00k_b3y0nd_th3_w0rld}'
```
