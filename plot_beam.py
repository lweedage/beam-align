import numpy as np
import scipy.sparse as sp
import math
import matplotlib.pyplot as plt
import networkx as nx
import sys
from itertools import product

from matplotlib.cm import ScalarMappable

import initialization
import new_optimization
import os
from parameters import *
import functions as f


x_bs, y_bs, x_user, y_user = [50], [10], [50], [90]
opt_x = np.ones((1, 1))

# delta = 500
# bound = 10
# grid_size = (xmax + 2*bound)/delta
# x_grid = np.arange(xmin - bound, xmax + bound, grid_size)
# y_grid = np.arange(ymin - bound, ymax + bound, grid_size)
# x_mesh,y_mesh = np.meshgrid(x_grid,y_grid)
# xc, yc = x_mesh + grid_size/2, y_mesh + grid_size/2
#
# gain = np.zeros((delta, delta))
# coords_j = (x_bs[bs_of_interest], y_bs[bs_of_interest])
# coords_i = (x_user[0], y_user[0])
# for x in range(delta):
#     for y in range(delta):
#         coords_k = (xc[0,x], yc[y, 0])
#         gain[y,x] = f.find_gain(coords_j, coords_k, coords_j, coords_i, beamwidth_b)
#
# fig, ax = plt.subplots()
# vmin, vmax = 0, np.max(gain)
# contour_z1 = ax.pcolormesh(x_grid, y_grid, gain, vmin = vmin, vmax = vmax, cmap = 'turbo')
# fig.colorbar(ScalarMappable(norm=contour_z1.norm, cmap=contour_z1.cmap))
#
# G, colorlist, nodesize, edgesize, labels = f.make_graph(x_bs, y_bs, x_user, y_user, opt_x, 1)
# f.draw_graph(G, colorlist, nodesize, edgesize, labels, ax, color = 'white')
# plt.xlim((xmin - bound, xmax + bound))
# plt.ylim((ymin - bound, ymax + bound))
# plt.plot(x_bs, y_bs)
# plt.plot(x_user, y_user)
# plt.show()

def path_loss(r):
    if r <= critical_distance:
        p_los = 1
    else:
        p_los = 0

    p_nlos = 1 - p_los
    if r > d0:
        l_los =  k * (r/d0) ** (-alpha_los)
        l_nlos = k * (r/d0)**(-alpha_nlos)
    else:
        l_los = k
        l_nlos = k
    return 20 * math.log10(p_los * l_los + p_nlos * l_nlos)

distances = np.arange(0, 100, 1)
y = [path_loss(x) for x in distances]
plt.plot(distances, y)
plt.xlabel('Distance $r_{ij}$')
plt.ylabel('Path loss (dB)')
# plt.yscale('log')
plt.show()