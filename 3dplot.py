#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

# Local
from model import MagnetModel

##################################### MAIN FUNCTION ##########################
def main():
    # Setup model
    model = MagnetModel()

    fig = plt.figure()
    awg = np.arange(2, 51)
    winding = np.arange(1000)

    awg, winding = np.meshgrid(awg, winding)

    pull = np.empty((1000, 49))
    current = np.empty((1000, 49))

    for i in range(1000):
        for j in range(49):
            pull[i][j], current[i][j] = model.run(awg[i][j], winding[i][j], 6, 0.480 + 100)

    ax = fig.add_subplot(1, 2, 1, projection='3d')
    ax.set(xlabel='Wire Guage (AWG)', ylabel='Winding count (Turns)', zlabel='Winding Current (A)', title='Plot of Winding Current based on Wire Guage and Winding Count (4 * 1.5V Battery) (100 Ohm Series Resistor)')
    ax.plot_surface(awg, winding, pull, color="red")
    plt.show()

main()
