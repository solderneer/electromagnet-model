#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

# Local
from models import MagnetModel, BatteryModel

##################################### MAIN FUNCTION ##########################
def main():
    WINDING = 1000
    
    # Setup model
    model = MagnetModel(verbose=True)
    # bat = BatteryModel(9, isr=3.040, s=1, p=1) 
    bat = BatteryModel(1.5, isr=0.120, s=4, p=1) 

    awg = np.arange(2, 51)
    pull = np.empty(49)
    current = np.empty(49)
    count = 0
    for i in range(0, 49):
        model.set_params(awg[i], WINDING)
        pull[count], winding_current = model.run(bat)
        current[count] = bat.cell_current(winding_current)
        count += 1

    fig, ax = plt.subplots(2, 1, sharex=True) 
    ax[0].plot(awg, pull, linewidth=2.0)
    ax[1].plot(awg, current, linewidth=2.0)
    ax[0].set(xlabel='Wire Guage (AWG)', ylabel='Pull Weight (kg)',
       title='Plot of Pull Weight against Wire Guage ({} turns)'.format(WINDING))
    ax[0].grid()
    
    ax[1].set(xlabel='Wire Guage (AWG)', ylabel='Current (A)',
       title='Plot of Cell Current against Wire Guage ({} turns)'.format(WINDING))
    ax[1].grid()

    plt.show()

main()
