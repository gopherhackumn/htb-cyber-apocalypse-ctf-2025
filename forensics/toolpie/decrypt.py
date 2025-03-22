from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

k = "5UUfizsRsP7oOCAq".encode()
c = AES.new(k , AES.MODE_CBC, k)

with open("extracted-file", "rb") as f:
    data = f.read()

result = c.decrypt(data)
result = unpad(result, 16)

with open("decrypted-file", "wb") as f:
    f.write(result)
