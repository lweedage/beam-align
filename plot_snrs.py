import math
import pickle

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
# from parameters import *
import numpy as np

params = {'legend.fontsize': 'large',
          'axes.labelsize': 'large',
          'axes.titlesize': 'large',
          'xtick.labelsize': 'large',
          'ytick.labelsize': 'large',
          'figure.autolayout': True}
pylab.rcParams.update(params)

colors = ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed', 'grey'] * 100
markers = ['o', 's', 'v', '*', 'p', 'P', '1', '+'] * 100

iterations = {120: 10, 300: 10, 600: 10, 900: 10, 1200: 10}
users = [120, 300, 600, 900, 1200]

radius = 200  # for triangular grid

xmin, xmax = 0, 800
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

xDelta = xmax - xmin
yDelta = ymax - ymin

M = 10000
maximum = 16

# ---------------------------------------- HEURISTICS ------------------------------------------------
user_rate = 500
beamwidth_deg = 10
s = 10
fig, ax = plt.subplots()
y120, y300, y600, y900, y1200 = [], [], [], [], []
for k in np.arange(1, maximum, 1):
    x = pickle.load(
        open(str('Data/Processed/capSNR_k=' + str(k) + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
             'rb')).values()
    x = [i / j for i, j in zip(x, users)]
    # plt.plot(users, x, '--', marker=markers[k-1], label=f'$k={k}$', color=colors[k-1])

    y120.append(x[0])
    y300.append(x[1])
    y600.append(x[2])
    y900.append(x[3])
    y1200.append(x[4])

    maxima = [np.argmax(i) + 1 for i in [y120, y300, y600, y900, y1200]]

plt.plot(np.arange(1, maximum, 1), y120, label='$\lambda_U = 100$', color=colors[0])
plt.plot(np.arange(1, maximum, 1), y300, label='$\lambda_U = 250$', color=colors[1])
plt.plot(np.arange(1, maximum, 1), y600, label='$\lambda_U = 500$', color=colors[2])
plt.plot(np.arange(1, maximum, 1), y900, label='$\lambda_U = 750$', color=colors[3])
plt.plot(np.arange(1, maximum, 1), y1200, label='$\lambda_U = 1000$', color=colors[4])

plt.plot(maxima, [max(i) for i in [y120, y300, y600, y900, y1200]], '--', marker=markers[0], color=colors[6],
         label='Maximum')

plt.xlabel('$k$')
plt.ylabel('Per-user capacity (Mbps)')
plt.legend()
plt.savefig(f'Figures/snrscapacity{beamwidth_deg}{s}{user_rate}')
plt.show()
