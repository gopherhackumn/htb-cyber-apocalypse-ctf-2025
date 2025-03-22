from Crypto.Cipher import AES

k = "5UUfizsRsP7oOCAq".encode()
c = AES.new(k , AES.MODE_CBC, k)

with open("extracted-file", "rb") as f:
    data = f.read()

result = c.decrypt(data)

with open("decrypted-file", "wb") as f:
    f.write(result)
