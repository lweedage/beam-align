import numpy as np
import scipy.sparse as sp
import math
import matplotlib.pyplot as plt
import networkx as nx
import sys
from itertools import product
from matplotlib.cm import ScalarMappable
import new_optimization
import os
from parameters import *
import functions as f

xmax = 50
ymax = 50

number_of_users = 3

delta = 100
bound = 2
grid_size = (xmax + 2*bound)/delta
x_grid = np.arange(xmin - bound, xmax + bound, grid_size)
y_grid = np.arange(ymin - bound, ymax + bound, grid_size)
x_mesh,y_mesh = np.meshgrid(x_grid,y_grid)
xc, yc = x_mesh + grid_size/2, y_mesh + grid_size/2

gain = np.zeros((delta, delta))
x_user, y_user = f.find_coordinates()
coords_i = (x_user[0], y_user[0])

for j in range(number_of_bs):
    coords_j = (x_bs[j], y_bs[j])
    for x in range(delta):
        for y in range(delta):
            coords_k = (xc[0,x], yc[y, 0])
            gain[x, y] += 10 * math.log10(f.find_gain(coords_j, coords_k, coords_j, coords_k, beamwidth_b))

fig, ax = plt.subplots()
vmin, vmax = 150, np.max(gain)
contour_z1 = ax.pcolormesh(x_grid, y_grid, gain, vmin = vmin, vmax = vmax, cmap = 'turbo')
fig.colorbar(ScalarMappable(norm=contour_z1.norm, cmap=contour_z1.cmap))

# G, colorlist, nodesize, edgesize, labels, edgecolor = f.make_graph(x_bs, y_bs, x_user, y_user, np.zeros((number_of_users, number_of_bs)), 1)
# f.draw_graph(G, colorlist, nodesize, edgesize, labels, ax, color = 'white', edgecolor= 'white')
plt.xlim((xmin - bound, xmax + bound))
plt.ylim((ymin - bound, ymax + bound))
plt.scatter(x_bs, y_bs, color = 'white')
contour_z1.set_label('gain (dB)')
# plt.plot(x_user, y_user)
plt.show()

def path_loss(r):
    if r <= critical_distance:
        p_los = 1
    else:
        p_los = 0

    p_nlos = 1 - p_los
    if r > d0:
        l_los = k * (r / d0) ** (alpha_los)
        l_nlos = k * (r / d0) ** (alpha_nlos)
    else:
        l_los = k
        l_nlos = k
    return p_los * l_los + p_nlos * l_nlos

def find_gain(alpha, w):
    beamwidth_ml = w * 2.58
    G0 = 20 * math.log10(1.62 / math.sin(math.radians(w / 2)))
    print(G0)
    if 0 <= alpha <= beamwidth_ml / 2:
        return G0 - 3.01*(2 * alpha / w)**2
    else:
        return -0.4111 * math.log(math.degrees(w)) - 10.579


# distances = np.arange(0, 100, 1)
# y = [10*math.log10(path_loss(x)) for x in distances]
# plt.plot(distances, y)
# plt.xlabel('$R_{ij}$')
# plt.ylabel('Path loss (dB)')
# plt.xscale('log')
# plt.show()