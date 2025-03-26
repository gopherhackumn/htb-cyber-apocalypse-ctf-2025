import base64


def xor_decrypt(encrypted_data, key1, key2):
    # Decrypt data using double XOR with two keys.
    decrypted = bytearray(len(encrypted_data))
    for i in range(len(encrypted_data)):
        decrypted[i] = encrypted_data[i] ^ key1[i % len(key1)] ^ key2[i % len(key2)]
    return bytes(decrypted)


def get_flawed_key(encoded_key):
    # Replicate PowerShell's flawed key derivation: Base64 -> UTF-8 string (with replacement) -> UTF-8 bytes.
    decoded_bytes = base64.b64decode(encoded_key)
    decoded_str = decoded_bytes.decode(
        "utf-8", errors="replace"
    )
    return decoded_str.encode("utf-8")


def main():
    # Read encrypted file (Base64 encoded)
    with open("map.pdf.secured", "rb") as f:
        encrypted_b64 = f.read()

    # Base64 decode to get raw encrypted bytes
    encrypted_bytes = base64.b64decode(encrypted_b64)

    # Replicate PowerShell's key processing
    key1 = get_flawed_key(
        "NXhzR09iakhRaVBBR2R6TGdCRWVJOHUwWVNKcTc2RWl5dWY4d0FSUzdxYnRQNG50UVk1MHlIOGR6S1plQ0FzWg=="
    )
    key2 = get_flawed_key("n2mmXaWy5pL4kpNWr7bcgEKxMeUx50MJ")

    # Decrypt using XOR
    decrypted_data = xor_decrypt(encrypted_bytes, key1, key2)

    # Save decrypted file
    with open("map_decrypted.pdf", "wb") as f:
        f.write(decrypted_data)

    print("Decryption complete.")


if __name__ == "__main__":
    main()
