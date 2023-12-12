import math
# from parameters import *
import pickle

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt

import get_data

params = {'legend.fontsize': 'xx-large',
          'axes.labelsize': 'xx-large',
          'axes.titlesize': 'xx-large',
          'xtick.labelsize': 'xx-large',
          'ytick.labelsize': 'xx-large',
          'lines.markersize': 8,
          'figure.autolayout': True}
pylab.rcParams.update(params)

colors = ['#904C77', '#E49AB0', '#ECB8A5', '#96ACB7', '#957D95'] * 100
markers = ['o', 'X', 'v', 's', '*', 'P', '1', '+']

radius = 200  # for triangular grid

xmin, xmax = 0, 600
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 2

xDelta = xmax - xmin
yDelta = ymax - ymin

users = [21, 41, 104, 208, 312]

user_density = [50, 100, 250, 500, 750]

M = 750
beamwidth_deg = 10
user_rate = 500

# for scenario in [1, 2, 3, 21, 22, 23, 31, 32, 33]:
#     get_data.get_data(scenario, Heuristic=False, SNRHeuristic=False)
#     get_data.get_data(scenario, Heuristic=True, SNRHeuristic=False)
#     get_data.get_data(scenario, Heuristic=False, SNRHeuristic=True)

max_connections = 25

x1 = pickle.load(open(str('Data/Processed/dis' + str(5) + str(M) + str(max_connections) + '.p'), 'rb')).values()
x2 = pickle.load(open(str('Data/Processed/dis' + str(10) + str(M) + str(max_connections) + '.p'), 'rb')).values()
x3 = pickle.load(open(str('Data/Processed/dis' + str(15) + str(M) + str(max_connections) + '.p'), 'rb')).values()

print('disconnected = ', x1)
print('disconnected = ', x2)
print('disconnected = ', x3)

x1 = pickle.load(open(str('Data/Processed/cap' + str(5) + str(M) + str(max_connections) + '.p'), 'rb')).values()
x2 = pickle.load(open(str('Data/Processed/cap' + str(10) + str(M) + str(max_connections) + '.p'), 'rb')).values()
x3 = pickle.load(open(str('Data/Processed/cap' + str(15) + str(M) + str(max_connections) + '.p'), 'rb')).values()

# x1 = [i / j for i, j in zip(x1, users)]
# x2 = [i / j for i, j in zip(x2, users)]
# x3 = [i / j for i, j in zip(x3, users)]
print(x1)
print(x2)
print(x3)
plt.plot(user_density, [x for x in x1], '--', marker=markers[0], label='$\\theta^b = 5\\degree$', color=colors[0])
plt.plot(user_density, [x for x in x2], '--', marker=markers[1], label='$\\theta^b = 10\\degree$', color=colors[1])
plt.plot(user_density, [x for x in x3], '--', marker=markers[2], label='$\\theta^b = 15\\degree$', color=colors[2])

plt.xlabel('Users per km$^2$')
plt.ylabel('Per-user capacity (Mbps)')
plt.xticks(([100, 250, 500, 750]))
plt.legend()
plt.show()

x1 = pickle.load(open(str('Data/Processed/sat' + str(5) + str(M) + str(max_connections) + '.p'), 'rb')).values()
x2 = pickle.load(open(str('Data/Processed/sat' + str(10) + str(M) + str(max_connections) + '.p'), 'rb')).values()
x3 = pickle.load(open(str('Data/Processed/sat' + str(15) + str(M) + str(max_connections) + '.p'), 'rb')).values()
print('sat', x1, x2, x3)
plt.plot(user_density, x1, '--', marker=markers[0], label='$\\theta^b = 5\\degree$', color=colors[0])
plt.plot(user_density, x2, '--', marker=markers[1], label='$\\theta^b = 10\\degree$', color=colors[1])
plt.plot(user_density, x3, '--', marker=markers[2], label='$\\theta^b = 15\\degree$', color=colors[2])

plt.xlabel('Users per km$^2$')
plt.ylabel('Average satisfaction (per user)')
plt.legend()
plt.xticks(([100, 250, 500, 750]))

plt.show()


x1 = pickle.load(open(str('Data/Processed/sat' + str(10) + str(M) + str(1) + '.p'), 'rb')).values()
x2 = pickle.load(open(str('Data/Processed/sat' + str(10) + str(M) + str(2) + '.p'), 'rb')).values()
x3 = pickle.load(open(str('Data/Processed/sat' + str(10) + str(M) + str(25) + '.p'), 'rb')).values()
plt.plot(user_density, x1, '--', marker=markers[0], label='$k = 1$', color=colors[0])
plt.plot(user_density, x2, '--', marker=markers[1], label='$k = 2$', color=colors[1])
plt.plot(user_density, x3, '--', marker=markers[2], label='$k = \\infty$', color=colors[2])

plt.xlabel('Users per km$^2$')
plt.ylabel('Average satisfaction (per user)')
plt.legend()
plt.xticks(([100, 250, 500, 750]))

plt.show()

x1 = pickle.load(open(str('Data/Processed/cap' + str(10) + str(M) + str(1) + '.p'), 'rb')).values()
x2 = pickle.load(open(str('Data/Processed/cap' + str(10) + str(M) + str(2) + '.p'), 'rb')).values()
x3 = pickle.load(open(str('Data/Processed/cap' + str(10) + str(M) + str(25) + '.p'), 'rb')).values()
plt.plot(user_density, x1, '--', marker=markers[0], label='$k = 1$', color=colors[0])
plt.plot(user_density, x2, '--', marker=markers[1], label='$k = 2$', color=colors[1])
plt.plot(user_density, x3, '--', marker=markers[2], label='$k = \\infty$', color=colors[2])

plt.xlabel('Users per km$^2$')
plt.ylabel('Per-user capacity (Mbps)')
plt.legend()
plt.xticks(([100, 250, 500, 750]))

plt.show()


