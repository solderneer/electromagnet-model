import numpy as np
import matplotlib.pyplot as plt

# Local
from models import MagnetModel, BatteryModel

model = MagnetModel(verbose=True)
bat1 = BatteryModel(9, 5.0, 600, isr=3.040) # Drawing 500mA constant current
bat2 = BatteryModel(6.4, 5.2, 3600, isr=0.480) # Drawing 500mA constant current
bat3 = BatteryModel(3.2, 2.8, 3600, isr=0.120) # Drawing 250mA constant current per battery
bat4 = BatteryModel(1.6, 1.4, 9000,  isr=0.030) # Drawing 125mA constant current per battery

model.set_params(27, 1000)

t = np.arange(500)
pull = np.empty((4, 500))
current = np.empty((4, 500))

for i in t:
    pull[0][i], current[0][i] = model.run(bat1)
    pull[1][i], current[1][i] = model.run(bat2)
    pull[2][i], current[2][i] = model.run(bat3)
    pull[3][i], current[3][i] = model.run(bat4)

    bat1.use(1)
    bat2.use(1)
    bat3.use(1)
    bat4.use(1)


fig, ax = plt.subplots(2, 1, sharex=True) 

ax[0].plot(t, pull[0], linewidth=2.0, label='9V Battery')
ax[0].plot(t, pull[1], linewidth=2.0, label='6V Battery')
ax[0].plot(t, pull[2], linewidth=2.0, label='3V Battery')
ax[0].plot(t, pull[3], linewidth=2.0, label='1.5V Battery')

ax[1].plot(t, current[0], linewidth=2.0, label='9V Battery')
ax[1].plot(t, current[1], linewidth=2.0, label='6V Battery')
ax[1].plot(t, current[2], linewidth=2.0, label='3V Battery')
ax[1].plot(t, current[3], linewidth=2.0, label='1.5V Battery')

ax[0].set(xlabel='Time (s)', ylabel='Pull Weight (kg)',
   title='Plot of Pull Weight against Time')
ax[0].grid()

ax[1].set(xlabel='Time (s)', ylabel='Current (A)',
   title='Plot of Current against Time')
ax[1].grid()

plt.legend()
plt.show()
