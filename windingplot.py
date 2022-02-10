
#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

# Local
from models import MagnetModel, BatteryModel

##################################### MAIN FUNCTION ##########################
def main():
    # Setup model
    model = MagnetModel(verbose=True)
    AWG = 27
    bat = BatteryModel(6, isr=0.480) 

    pull = np.empty(1000)
    current = np.empty(1000)
    for i in range(0, 1000):
        model.set_params(AWG, i)
        pull[i], current[i] = model.run(bat)

    winding = np.arange(1000)
    fig, ax = plt.subplots(2, 1, sharex=True) 
    ax[0].plot(winding, pull, linewidth=2.0)
    ax[1].plot(winding, current, linewidth=2.0)
    ax[0].set(xlabel='Winding (Turns)', ylabel='Pull Weight (kg)',
       title='Plot of Pull Weight against Winding Count ({} AWG)'.format(AWG))
    ax[0].grid()
    
    ax[1].set(xlabel='Winding (Turns)', ylabel='Current (A)',
       title='Plot of Current against Winding Count ({} AWG)'.format(AWG))
    ax[1].grid()

    plt.show()

main()
