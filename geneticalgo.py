import numpy as np
from geneticalgorithm import geneticalgorithm as ga

# Local
from models import MagnetModel, BatteryModel

def model_wrapper(P):
    # P[0] = AWG
    # P[1] = WINDING
    # P[2] = Battery comfiguration

    battery_configs = [
        BatteryModel(9, isr=3.040), 
        BatteryModel(6, isr=0.480), 
        BatteryModel(3, isr=0.120), 
        BatteryModel(1.5, isr=0.030)
    ] 

    model = MagnetModel()
    model.set_params(int(P[0]), int(P[1]))
    pull, winding_current = model.run(battery_configs[int(P[2])])

    if winding_current > 1.0:
        return 0

    return -1 * pull + (winding_current * 20)

varbound = np.array([[2,50], [0, 1000], [0, 3]])
model = ga(function=model_wrapper,dimension=3,variable_type='int',variable_boundaries=varbound)
model.run()
