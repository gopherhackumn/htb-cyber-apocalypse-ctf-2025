import base64
import itertools


def caesar(s, shift):
    res = []
    for c in s:
        # print(ord(c), end=" ")
        if "0" <= c <= "9":
            c = (ord(c) - ord("0") + shift) % 10 + ord("0")
        elif "A" <= c <= "Z":
            c = (ord(c) - ord("A") + shift) % 26 + ord("A")
        elif "a" <= c <= "z":
            c = (ord(c) - ord("a") + shift) % 26 + ord("a")
        else:
            c = ord(c)
        # print(c)
        res.append(chr(c))
    return bytes("".join(res), "utf-8")



def xor(s, key):
    # print("TEST")
    # for c, ck in list(zip(s, itertools.cycle(key)))[:30]:
        # print(c, ck)
    return [c ^ ck for c, ck in zip(s, itertools.cycle(key))]


with open("map.pdf.secured", "rb") as f:
    s = f.read()
    s = base64.b64decode(s)
    # print(len(s))

    k34Vm = "Ki50eHQgKi5kb2MgKi5kb2N4ICoucGRm"
    m78Vo = "LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQpZT1VSIEZJTEVTIEhBVkUgQkVFTiBFTkNSWVBURUQgQlkgQSBSQU5TT01XQVJFCiogV2hhdCBoYXBwZW5lZD8KTW9zdCBvZiB5b3VyIGZpbGVzIGFyZSBubyBsb25nZXIgYWNjZXNzaWJsZSBiZWNhdXNlIHRoZXkgaGF2ZSBiZWVuIGVuY3J5cHRlZC4gRG8gbm90IHdhc3RlIHlvdXIgdGltZSB0cnlpbmcgdG8gZmluZCBhIHdheSB0byBkZWNyeXB0IHRoZW07IGl0IGlzIGltcG9zc2libGUgd2l0aG91dCBvdXIgaGVscC4KKiBIb3cgdG8gcmVjb3ZlciBteSBmaWxlcz8KUmVjb3ZlcmluZyB5b3VyIGZpbGVzIGlzIDEwMCUgZ3VhcmFudGVlZCBpZiB5b3UgZm9sbG93IG91ciBpbnN0cnVjdGlvbnMuCiogSXMgdGhlcmUgYSBkZWFkbGluZT8KT2YgY291cnNlLCB0aGVyZSBpcy4gWW91IGhhdmUgdGVuIGRheXMgbGVmdC4gRG8gbm90IG1pc3MgdGhpcyBkZWFkbGluZS4KLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQo="
    a53Va = "NXhzR09iakhRaVBBR2R6TGdCRWVJOHUwWVNKcTc2RWl5dWY4d0FSUzdxYnRQNG50UVk1MHlIOGR6S1plQ0FzWg=="
    b64Vb = "n2mmXaWy5pL4kpNWr7bcgEKxMeUx50MJ"

    k34Vm = base64.b64decode(k34Vm)
    m78Vo = base64.b64decode(m78Vo)
    c56Ve = base64.b64decode(caesar(a53Va, 1))
    d78Vf = base64.b64decode(caesar(b64Vb, 1))
    # c56Ve = base64.b64decode(a53Va)
    # c56Ve = base64.b64decode(c56Ve)
    # d78Vf = base64.b64decode(b64Vb)

    # print(c56Ve)

    res = bytes("".join(chr(c) for c in xor(xor(s, c56Ve), d78Vf)), "utf-8")
    print(res[:20])
    with open("map.pdf", "wb") as ff:
        ff.write(res)
