import numpy as np
from geneticalgorithm import geneticalgorithm as ga

# Local
from mag_model import MagnetModel

def model_wrapper(P):
    # P[0] = AWG
    # P[1] = WINDING
    # P[2] = SERIES_RESISTANCE
    # P[3] = Battery comfiguration

    battery_configs = [(9, 3.050), (6, 0.480), (3, 0.120), (1.5, 0.030)] 
    VOLTAGE = battery_configs[int(P[3])][0]
    INTERNAL_RESISTANCE = battery_configs[int(P[3])][1]

    model = MagnetModel(saturate=True)
    pull, winding_current = model.run(int(P[0]), int(P[1]), VOLTAGE, INTERNAL_RESISTANCE + int(P[2]))

    if winding_current > 1.0:
        return 0

    return -1 * pull + (winding_current * 50)

varbound = np.array([[2,50], [0, 1000], [0, 1000], [0, 3]])
model = ga(function=model_wrapper,dimension=4,variable_type='int',variable_boundaries=varbound)
model.run()


