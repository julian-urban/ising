import numpy as np

from functions import *


class Lattice:
    def __init__(self, N, T, h):
        assert N % 2 == 0
        assert T > 0

        self.N = N
        self.b = 1 / T
        self.h = h
        
        # warm start
        self.spins = (2 * (np.random.randint(0, 2, (N, N)) - 0.5)).astype(np.int)

        # cold start
        # self.spins = np.ones((N, N))

        self.black_pm = get_chess(N)
        self.white_pm = np.roll(self.black_pm, 1, 0)

        self.black_01 = ((self.black_pm + 1) / 2).astype(int)
        self.white_01 = np.roll(self.black_01, 1, 0)
    
    def get_energy(self):
        return np.sum(-self.b * self.spins
            * (np.roll(self.spins, 1, 0) + np.roll(self.spins, 1, 1))
            - self.h * self.spins)

    def get_local_energy(self, x, y):
        return (-self.b * self.spins[x,y] * 
            (self.spins[(x+1)%self.N,y] + self.spins[x-1,y]
             + self.spins[x,(y+1)%self.N] + self.spins[x,y-1])
            - self.h * self.spins[x,y])

    def get_energy_density(self):
        return (-self.b * self.spins
            * (np.roll(self.spins, 1, 0) + np.roll(self.spins, 1, 1)
               + np.roll(self.spins, -1, 0) + np.roll(self.spins, -1, 1))
            - self.h * self.spins)

    def local_metropolis(self, x, y):
        H0 = self.get_local_energy(x, y)
        self.spins[x,y] *= -1
        dH = self.get_local_energy(x, y) - H0

        if dH > 0:
            if np.random.rand() > np.exp(-dH):
                self.spins[x,y] *= -1

    def parallel_metropolis(self):
        H0 = self.get_energy_density()
        self.spins *= self.black_pm
        dH = self.get_energy_density() - H0
        self.spins *= self.white_01 - self.black_01 * (2 * (np.random.rand(self.N, self.N) > np.exp(-dH)).astype(int) - 1)

        H0 = self.get_energy_density()
        self.spins *= self.white_pm
        dH = self.get_energy_density() - H0
        self.spins *= self.black_01 - self.white_01 * (2 * (np.random.rand(self.N, self.N) > np.exp(-dH)).astype(int) - 1)
        
    def wolff(self):
        i, j = np.random.randint(0, self.N), np.random.randint(0, self.N)
        S = self.spins[i,j]
        C = [[i,j]]
        F_old = [[i,j]]
        p = 1. - np.exp(-2 * self.b)

        while len(F_old) > 0:
            F_new = []

            for i,j in F_old:
                neighbours = [[(i+1) % self.N,j], [(i-1+self.N) % self.N,j], [i,(j+1) % self.N], [i,(j-1+self.N) % self.N]]

                for neighbour in neighbours:
                    if self.spins[neighbour[0],neighbour[1]] == S and neighbour not in C:
                        if np.random.rand() < p:
                            F_new.append(neighbour)
                            C.append(neighbour)

            F_old = F_new

        for i,j in C:
            self.spins[i,j] *= -1
