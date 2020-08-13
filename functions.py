import numpy as np


def get_chess(N):
	assert N % 2 == 0

	row_a = np.ones(N)
	row_a[0::2] = -1

	row_b = np.roll(row_a, 1)

	chess = []
	
	for _ in range(int(N / 2)):
		chess.append(row_a)
		chess.append(row_b)

	return np.array(chess).astype(int)