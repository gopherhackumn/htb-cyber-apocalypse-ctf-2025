from sage.all import *
from pwn import *
import logging

r = remote("94.237.58.86", 40133)

print(r.recvuntil(b"You are given the sacred prime: p = "))
print(line := r.recvline())
p = int(line.strip())
r.sendline(bytes(str(p.bit_length()), "utf-8"))

res = []
for k, v in factor(p - 1):
    res.append(str(k) + "," + str(v))
r.sendline("_".join(res))

print(r.recvuntil(b"[3]"))
print(r.recvline())
for _ in range(17):
    # print(line := r.recvuntil(b"?"))
    print(line := r.recv(4096))
    g = GF(p)(int(line.split(b"?")[0].split()[-1]))
    print("g", g)
    r.sendline(b"1" if g.is_primitive_root() else b"0")

print(r.recvuntil(b"a = "))
print(line := r.recvline())
a = int(line.strip())
print(r.recvuntil(b"b = "))
print(line := r.recvline())
b = int(line.strip())
E = EllipticCurve(GF(p), [a, b])
order = E.cardinality()
r.sendline(bytes(str(order), "utf-8"))

# https://math.stackexchange.com/questions/144106/how-to-find-the-order-of-elliptic-curve-over-finite-field-extension
# Order is p^3 + 3*p
res = [(2, 2), (7, 2), (p, 1), (2296163171090566549378609985715193912396821929882292947886890025295122370435191839352044293887595879123562797851002485690372901374381417938210071827839043175382685244226599901222328480132064138736290361668527861560801378793266019, 1)]
for i in range(len(res)):
    k, v = res[i]
    res[i] = str(k) + "," + str(v)
r.sendline("_".join(res))

print(r.recvuntil(b"The chosen base point G has x-coordinate: "))
print(line := r.recvline())
G = int(line.strip())
print(r.recvuntil(b"The resulting point A has x-coordinate: "))
print(line := r.recvline())
A = int(line.strip())

# https://github.com/jvdsn/crypto-attacks/blob/master/attacks/ecc/smart_attack.py

# Convert a field element to a p-adic number.
def _gf_to_qq(n, qq, x):
    return ZZ(x) if n == 1 else qq(list(map(int, x.polynomial())))


# Lift a point to the p-adic numbers.
def _lift(E, p, Px, Py):
    for P in E.lift_x(Px, all=True):
        if (P.xy()[1] % p) == Py:
            return P


def attack(G, P):
    """
    Solves the discrete logarithm problem using Smart's attack.
    More information: Smart N. P., "The Discrete Logarithm Problem on Elliptic Curves of Trace One"
    More information: Hofman S. J., "The Discrete Logarithm Problem on Anomalous Elliptic Curves" (Section 6)
    :param G: the base point
    :param P: the point multiplication result
    :return: l such that l * G == P
    """
    E = G.curve()
    assert E.trace_of_frobenius() == 1, f"Curve should have trace of Frobenius = 1."

    F = E.base_ring()
    p = F.characteristic()
    q = F.order()
    n = F.degree()
    qq = Qq(q, names="g")

    # Section 6.1: case where n == 1
    logging.info(f"Computing l % {p}...")
    E = EllipticCurve(qq, [_gf_to_qq(n, qq, a) + q * ZZ.random_element(1, q) for a in E.a_invariants()])
    Gx, Gy = _gf_to_qq(n, qq, G.xy()[0]), _gf_to_qq(n, qq, G.xy()[1])
    Gx, Gy = (q * _lift(E, p, Gx, Gy)).xy()
    Px, Py = _gf_to_qq(n, qq, P.xy()[0]), _gf_to_qq(n, qq, P.xy()[1])
    Px, Py = (q * _lift(E, p, Px, Py)).xy()
    l = ZZ(((Px / Py) / (Gx / Gy)) % p)

    if n > 1:
        # Section 6.2: case where n > 1
        G0 = p ** (n - 1) * G
        G0x, G0y = _gf_to_qq(n, qq, G0.xy()[0]), _gf_to_qq(n, qq, G0.xy()[1])
        G0x, G0y = (q * _lift(E, p, G0x, G0y)).xy()
        for i in range(1, n):
            logging.info(f"Computing l % {p ** (i + 1)}...")
            Pi = p ** (n - i - 1) * (P - l * G)
            if Pi.is_zero():
                continue

            Pix, Piy = _gf_to_qq(n, qq, Pi.xy()[0]), _gf_to_qq(n, qq, Pi.xy()[1])
            Pix, Piy = (q * _lift(E, p, Pix, Piy)).xy()
            l += p ** i * ZZ(((Pix / Piy) / (G0x / G0y)) % p)

    return int(l)

res = attack(E.lift_x(Integer(G)), E.lift_x(Integer(A)))
r.sendline(bytes(str(res), "utf-8"))

print(r.recvline())
print(r.recvline())
print(r.recvline())
print(r.recvline())
print(r.recvline())
print(r.recvline())
print(r.recvline())
print(r.recvline())
print(r.recvline())

# Flag: HTB{Welcome_to_CA_2k25!Here_is_your_anomalous_flag_for_this_challenge_and_good_luck_with_the_rest:)_d077a4b85dd9de9a0c1bbcfb618665c6}
