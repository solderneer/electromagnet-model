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
        BatteryModel(1.5, isr=0.120, s=4, p=1),
        BatteryModel(1.5, isr=0.120, s=1, p=4)
    ] 

    model = MagnetModel()
    model.set_params(int(P[0]), int(P[1]))
    pull, winding_current = model.run(battery_configs[int(P[2])])
    cell_current = battery_configs[int(P[2])].cell_current(winding_current)

    return -1 * pull + (cell_current * 10)

varbound = np.array([[2,50], [0, 1000], [0, 2]])
model = ga(function=model_wrapper,dimension=3,variable_type='int',variable_boundaries=varbound)
model.run()
