import numpy as np

from lattice import Lattice


N = 16
T = 2.
h = 0.

lattice = Lattice(N, T, h)

for i in range(1000):
	lattice.wolff()

M = []

for i in range(10000):
	lattice.wolff()

	if i % 10 == 0:
		M.append(np.abs(lattice.spins.mean()))

np.savetxt("M.txt", np.array(M))