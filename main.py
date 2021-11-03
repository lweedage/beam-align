import gurobipy as gp
from gurobipy import GRB
from gurobipy import quicksum
import numpy as np
import scipy.sparse as sp
import math
import matplotlib.pyplot as plt
import networkx as nx
import sys
from itertools import product
import initialization
import new_optimization
import os
from parameters import *
import functions as f
from matplotlib.cm import ScalarMappable

np.random.seed(seed)

opt_x = new_optimization.optimization()
print(opt_x)

# opt_x = np.ones((number_of_users, number_of_bs))

delta = 200
bound = 10
grid_size = (xmax + 2*bound)/delta

x_grid = np.arange(xmin - bound, xmax + bound, grid_size)
y_grid = np.arange(ymin - bound, ymax + bound, grid_size)

x_mesh,y_mesh = np.meshgrid(x_grid,y_grid)

xc, yc = x_mesh + grid_size/2, y_mesh + grid_size/2

interference = np.zeros((delta, delta))

blub = 0

j = (x_bs[0], y_bs[0])

for x in range(delta):
    for y in range(delta):
        interference[y, x] = f.find_new_interference((xc[0, x], yc[y, 0]), j, opt_x)

print(interference)

fig, ax = plt.subplots()

vmin, vmax = 0, np.max(interference)/10

contour_z1 = ax.pcolormesh(x_grid, y_grid, interference, vmin = vmin, vmax = vmax, cmap = 'turbo')
fig.colorbar(ScalarMappable(norm=contour_z1.norm, cmap=contour_z1.cmap))

plt.scatter(x_user, y_user)
plt.scatter(x_bs, y_bs)
plt.xlim((xmin - bound, xmax + bound))
plt.ylim((ymin - bound, ymax + bound))

G, colorlist, nodesize, edgesize, labels = f.make_graph(x_bs, y_bs, x_user, y_user, opt_x, number_of_users)
f.draw_graph(G, colorlist, nodesize, edgesize, labels, ax)
plt.show()
