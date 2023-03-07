from random import random, randint
import numpy as np
import pandas as pd
from matplotlib import colors
import matplotlib.pyplot as plt

def setup_grid_centre(gridsize=10):
        #concatinates rows and edges based on gridsize and max_radius
        sim = np.array([[1]*gridsize]*gridsize)
        #places a single infected individual in the middle of the grid
        centre = int(gridsize/2)
        sim[centre, centre] = 3
        return sim

def setup_grid_random(gridsize=10):
    sim = np.array([[1]*gridsize]*gridsize)
    for x in range(gridsize):
        for y in range(gridsize):
            if random() < 0.2:
                sim[x,y] = 3
    return sim

def grid_frame_update(sim):
        
        size = len(sim[0])
        newsim = sim.copy()
        
        for x in range(size):
            for y in range(size):

                n = random()
                
                if sim[x,y] == 1:

                    if (sim[y,(x+1)%size] == 3 or sim[y,(x-1)%size] == 3 \
                    or sim[(y+1)%size,x] == 3 or sim[(y-1)%size,x] == 3 \
                    or sim[(y-1)%size,(x+1)%size] == 3 or sim[(y+1)%size,(x-1)%size] == 3 \
                    or sim[(y-1)%size,(x-1)%size] == 3 or sim[(y+1)%size,(x+1)%size] == 3):

                        nearsq = [sim[y,(x+1)%size], sim[y,(x-1)%size], 
                                  sim[(y+1)%size,x], sim[(y-1)%size,x],
                                  sim[(y-1)%size,(x+1)%size], sim[(y+1)%size,(x-1)%size],
                                  sim[(y-1)%size,(x-1)%size], sim[(y+1)%size,(x+1)%size]]

                        infecProb = (nearsq.count(3))/5

                        if n < infecProb:
                            newsim[x,y] = 3

                elif sim[x,y] == 3:
                    if n < 0.1:
                        newsim[x,y] = 5
                elif sim[x,y] == 5:
                    if n < 0:
                        newsim[x,y] = 1
        
        return newsim

def grid_sim(simtime=1000, gridsize=8000):
        sim = setup_grid_centre(gridsize)
        cmap = colors.ListedColormap(['steelblue','crimson','silver'])
        bounds = [0,2,4,6]
        #plt.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
        
        S = [gridsize**2 - 1]
        I = [1]
        R = [0]

        for j in range(0,simtime):
            sim = grid_frame_update(sim)
            S.append(list((sim.flatten())).count(1))
            I.append(list((sim.flatten())).count(3))
            R.append(list((sim.flatten())).count(5))
            #plt.cla()
            #plt.imshow(sim, cmap=cmap)
            #plt.draw()
            #plt.pause(0.00001)
        
        dict = {"S":S,"I":I,"R":R}
        df = pd.DataFrame(dict) 
        df.to_csv('SIR5.csv') 



        #plt.close()
        #plt.stackplot(range(0,simtime+1), 100*np.array(I)/(gridsize**2), 100*np.array(S)/(gridsize**2), 100*np.array(R)/(gridsize**2), colors=['crimson','steelblue','silver'], labels=["Infected","Susceptible","Recovered"])        
        #plt.xlabel("Time (days)")
        #plt.ylabel("Percentage of Population")
        #plt.title("SIR Grid Simulation")
        #plt.xlim(0,simtime)
        #plt.ylim(0,100)
        #plt.legend()
        #plt.savefig("SIRGrid.png", dpi=227)
            
           
grid_sim()