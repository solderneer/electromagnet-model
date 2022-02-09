
#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

# Local
from model import MagnetModel

##################################### MAIN FUNCTION ##########################
def main():
    # Setup model
    model = MagnetModel()

    AWG = 27
    VOLTAGE = 6
    INTERNAL_RESISTANCE = 0.480
    SERIES_RESISTANCE = 100

    pull = np.empty(1000)
    current = np.empty(1000)
    for i in range(0, 1000):
        pull[i], current[i] = model.run(AWG, i, VOLTAGE, INTERNAL_RESISTANCE + SERIES_RESISTANCE)

    winding = np.arange(1000)
    fig, ax = plt.subplots(2, 1, sharex=True) 
    ax[0].plot(winding, pull, linewidth=2.0)
    ax[1].plot(winding, current, linewidth=2.0)
    ax[0].set(xlabel='Winding (Turns)', ylabel='Pull Weight (kg)',
       title='Plot of Pull Weight against Wire Guage ({} AWG, {} Ohm Resistor)'.format(AWG, SERIES_RESISTANCE))
    ax[0].grid()
    
    ax[1].set(xlabel='Winding (Turns)', ylabel='Current (A)',
       title='Plot of Current against Wire Guage ({} AWG, {} Ohm Resistor)'.format(AWG, SERIES_RESISTANCE))
    ax[1].grid()

    plt.show()

main()
