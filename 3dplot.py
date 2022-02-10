#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

# Local
from models import MagnetModel, BatteryModel

##################################### MAIN FUNCTION ##########################
def main():
    # Setup model
    model = MagnetModel()
    bat = BatteryModel(6.4, 5.6, 21600, 0.480)

    fig = plt.figure()
    awg = np.arange(2, 51)
    winding = np.arange(1000)

    awg, winding = np.meshgrid(awg, winding)

    pull = np.empty((1000, 49))
    current = np.empty((1000, 49))

    for i in range(1000):
        for j in range(49):
            model.set_params(awg[i][j], winding[i][j])
            pull[i][j], current[i][j] = model.run(bat)
    
 
    ax = fig.add_subplot(1, 3, 1, projection='3d')
    ax.set(xlabel='Wire Guage (AWG)', ylabel='Winding count (Turns)', zlabel='Pull Force (kg)', title='Plot of Pull Force')
    ax.plot_surface(awg, winding, pull, color="red")

    ax = fig.add_subplot(1, 3, 2, projection='3d')
    ax.set(xlabel='Wire Guage (AWG)', ylabel='Winding count (Turns)', zlabel='Winding Current (A)', title='Plot of Winding Current')
    ax.plot_surface(awg, winding, current, color="yellow")
    
    # Defining a fitness function
    fitness = pull - current * 20
    ax = fig.add_subplot(1, 3, 3, projection='3d')
    ax.set(xlabel='Wire Guage (AWG)', ylabel='Winding count (Turns)', zlabel='Model Fitness', title='Plot of Model Fitnes')
    ax.plot_surface(awg, winding, fitness, cmap='viridis', edgecolor='none')

    plt.show()

main()
