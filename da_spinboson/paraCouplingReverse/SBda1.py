import numpy as np
from scipy.optimize import curve_fit
# from fishbonett.starSpinBoson import SpinBoson, SpinBoson1D
from fishbonett.backwardSpinBoson import SpinBoson, SpinBoson1D, calc_U
from fishbonett.stuff import sigma_x, sigma_z, temp_factor, sd_zero_temp, drude1, lemmer, drude, _num, sigma_1
from scipy.linalg import expm
from time import time
import sys

bath_length = 200*5*2
phys_dim = 20
bond_dim = 1000
a = [np.ceil(phys_dim - N*(phys_dim -2)/ bath_length) for N in range(bath_length)]
a = [int(x) for x in a]
ene = int(sys.argv[1])

a = [phys_dim]*bath_length
print(a)

pd = a[::-1] + [2]
eth = SpinBoson(pd)
etn = SpinBoson1D(pd)
# set the initial state of the system. It's in the high-energy state |0>:

etn.B[-1][0, 1, 0] = 0.
etn.B[-1][0, 0, 0] = 1.


# spectral density parameters
g = 3500
eth.domain = [-g, g]
temp = int(sys.argv[2])
gam=int(sys.argv[3])
j = lambda w: drude(w, lam=3952, gam=gam)* temp_factor(temp,w)
eth.sd = j

eth.he_dy = np.diag([2, 1])
#eth.he_dy = np.diag([-.393073/2, .393073/2])
#eth.h1e =  np.diag([0-2700,  3040.58271-2700*1.9321]) + 119.95105179*sigma_x #+ 0.03862659583*np.diag([2700,2700])
eth.h1e =  np.diag([0,  ene]) + 119.95105179*sigma_x
#eth.h1e =  (9678.65315 - 3968.24779) * (sigma_z - sigma_1)/2 + 120.02659*sigma_x

eth.build(g=1., ncap=50000)

print(eth.w_list)
print(eth.k_list)

# ~ 0.5 ps ~ 0.1T
p = []


threshold = 1e-4
dt = 0.001/8
num_steps = 50*16

t = 0.
tt0=time()
for tn in range(num_steps):
    U1, U2 = eth.get_u(2*tn*dt, 2*dt, factor=2)

    t0 = time()
    etn.U = U1
    for j in range(bath_length-1,0,-1):
        print("j==", j, tn)
        etn.update_bond(j, bond_dim, threshold, swap=1)

    etn.update_bond(0, bond_dim, threshold, swap=0)
    etn.update_bond(0, bond_dim, threshold, swap=0)
    t1 = time()
    t = t + t1 - t0

    t0 = time()
    etn.U = U2
    for j in range(1, bath_length):
        print("j==", j, tn)
        etn.update_bond(j, bond_dim, threshold,swap=1)

    dim = [len(s) for s in etn.S]
    theta = etn.get_theta1(bath_length) # c.shape vL i vR
    rho = np.einsum('LiR,LjR->ij',  theta, theta.conj())
    pop = np.abs(rho[0,0])
    p = p + [pop]
    t1 = time()
    t = t + t1 - t0
tt1 = time()
print(tt1-tt0)
pop = [x.real for x in p]
print("population", pop)
pop = np.array(pop)
pop.astype('float32').tofile(f'./output/pop_da1_{temp}_{ene}_{gam}.dat')