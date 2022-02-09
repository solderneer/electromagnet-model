#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

# Local
from model import MagnetModel

##################################### MAIN FUNCTION ##########################
def main():
    # Setup model
    model = MagnetModel(saturate=True)

    WINDING = 1000
    VOLTAGE = 9
    INTERNAL_RESISTANCE = 3.050
    SERIES_RESISTANCE = 0

    awg = np.arange(2, 51)
    pull = np.empty(49)
    current = np.empty(49)
    count = 0
    for i in range(0, 49):
        pull[count], current[count] = model.run(awg[i], WINDING, VOLTAGE, INTERNAL_RESISTANCE + SERIES_RESISTANCE)
        count += 1

    fig, ax = plt.subplots(2, 1, sharex=True) 
    ax[0].plot(awg, pull, linewidth=2.0)
    ax[1].plot(awg, current, linewidth=2.0)
    ax[0].set(xlabel='Wire Guage (AWG)', ylabel='Pull Weight (kg)',
       title='Plot of Pull Weight against Wire Guage ({} turns, {} Ohm Resistor)'.format(WINDING, SERIES_RESISTANCE))
    ax[0].grid()
    
    ax[1].set(xlabel='Wire Guage (AWG)', ylabel='Current (A)',
       title='Plot of Current against Wire Guage ({} turns, {} Ohm Resistor)'.format(WINDING, SERIES_RESISTANCE))
    ax[1].grid()

    plt.show()

main()
