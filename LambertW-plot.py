import numpy as np
import matplotlib.pyplot as plt
from scipy.special import lambertw

def LambertW_plot():

    x = []
    y = []
    for r in np.arange(0,100,0.05):
        y.append(lambertw(r))
        x.append(r)

    plt.plot(y, c="green")
    plt.title("Lambert W function")
    plt.xlabel("X-input")
    plt.ylabel("Y-output")
    plt.xlim(0,2000)
    plt.ylim(0,3.5)
    plt.grid(ls=":",c='grey')
    plt.savefig("lambertW.png", dpi=227)




def stable_states():
    N = 1
    s0 = N - 0.00001
    R0 = []
    Sw = []

    for r in np.arange(1,3.5,0.05):
        Wsub = -(r/N)*s0*np.exp(-r)
        Wmul = -(N/r)
        Sw.append(Wmul*lambertw(Wsub))
        R0.append(r)
        

    plt.plot(R0, np.array(Sw)*100, c="steelblue", label="Susceptible")
    plt.plot(R0, (N - np.array(Sw))*100, c="#969696", label="Recovered")
    plt.title("SIR Stable States")
    plt.xlabel("R\u2080 value")
    plt.ylabel("Percentage of Population")
    plt.xlim(1,3)
    plt.ylim(0,100)
    plt.grid(ls=":",c='grey')
    plt.legend()
    plt.savefig("Stable-States.png",dpi=227)


LambertW_plot()