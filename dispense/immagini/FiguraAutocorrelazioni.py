import numpy as np
import matplotlib.pyplot as plt

tmin=0
tmax=6
tau = np.linspace(tmin, tmax, 600)
var=3
mean = 1.4
noise = 0.03 * (np.random.randn(len(tau))-0.5)

R = mean**2 + var*(np.exp(-tau)+noise)
C = R - mean**2
C_hat = C / C[0]

fig, axs = plt.subplots(3, 1, sharex=True)

# R
axs[0].plot(tau, R)
axs[0].axhline(mean**2, color='red', linestyle='--', label=r'$\bar f^{\,2}$')
axs[0].set_ylabel("R(τ)")
axs[0].set_xlim(tmin, tmax)
axs[0].set_ylim(0, var+mean**2)
axs[0].legend(loc='upper right', frameon=False)


# C
axs[1].plot(tau, C)
axs[1].axhline(0, color='black', linestyle='-', linewidth=0.5)
axs[1].set_ylabel("C(τ)")

# C_hat
axs[2].plot(tau, C_hat)
axs[2].axhline(0, color='black', linestyle='-', linewidth=0.5)
axs[2].set_ylabel("Ĉ(τ)")
axs[2].set_xlabel("τ")

plt.show()