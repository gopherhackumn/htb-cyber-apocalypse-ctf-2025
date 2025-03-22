# Coppersmith

import itertools

def small_roots(f, bounds, m=1, d=None):
	if not d:
		d = f.degree()

	if isinstance(f, Polynomial):
		x, = polygens(f.base_ring(), f.variable_name(), 1)
		f = f(x)

	R = f.base_ring()
	N = R.cardinality()

	f /= f.coefficients().pop(0)
	f = f.change_ring(ZZ)

	G = Sequence([], f.parent())
	for i in range(m+1):
		base = N^(m-i) * f^i
		for shifts in itertools.product(range(d), repeat=f.nvariables()):
			g = base * prod(map(power, f.variables(), shifts))
			G.append(g)

	B, monomials = G.coefficient_matrix()
	monomials = vector(monomials)

	factors = [monomial(*bounds) for monomial in monomials]
	for i, factor in enumerate(factors):
		B.rescale_col(i, factor)

	B = B.dense_matrix().LLL()

	B = B.change_ring(QQ)
	for i, factor in enumerate(factors):
		B.rescale_col(i, 1/factor)

	H = Sequence([], f.parent().change_ring(QQ))
	for h in filter(None, B*monomials):
		H.append(h)
		I = H.ideal()
		if I.dimension() == -1:
			H.pop()
		elif I.dimension() == 0:
			roots = []
			for root in I.variety(ring=ZZ):
				root = tuple(R(root[var]) for var in f.variables())
				roots.append(root)
			return roots

	return []


# Main

p = 0x31337313373133731337313373133731337313373133731337313373133732ad
Zp = Integers(p)
a = 0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef
b = 0xdeadc0dedeadc0dedeadc0dedeadc0dedeadc0dedeadc0dedeadc0dedeadc0de

h1 = 77759147870011250959067600299812670660963056658309113392093130
h2 = 50608194198883881938583003429122755064581079722494357415324546

P.<x, y> = PolynomialRing(Zp)

w1 = (h1 << 48) + x
w2 = (h2 << 48) + y
bounds = (1 << 48, 1 << 48)
print("Poly", w2*(1 - a*w1) - a*(1 - a*w2) - (1 - a*w1)*(1 - a*w2))
print(small_roots(w2*(1 - a*w1) - a*(1 - a*w2) - (1 - a*w1)*(1 - a*w2), bounds))

x = 53006259096585
y = 248699398699637
c = (h1 << 48) + x
f = c*b * pow(1 - a*c, -1, p) % p
print(hex((f - b) * pow(a, -1, p) % p))
