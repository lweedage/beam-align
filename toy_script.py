import matplotlib.pyplot as plt
import numpy as np


def find_rain(r, rain_rate):
    k = 0.124
    alpha = 1.061
    rain_att = k * rain_rate ** alpha
    return rain_att * (r / 1000)  # attenuation is in db/km


distances = np.arange(1, 400, 1)
fig, ax = plt.subplots()
plt.plot(distances, [find_rain(r, 2.5) for r in distances], label='2.5')
plt.plot(distances, [find_rain(r, 25) for r in distances], label='25')
plt.plot(distances, [find_rain(r, 150) for r in distances], label='150')
plt.legend()
plt.show()
