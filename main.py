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

if Closest and OneConnection:
    opt_x = np.zeros((number_of_users, number_of_bs))
    C = np.zeros(number_of_users)
    for i in range(number_of_users):
        j = f.find_closest_bs(i)
        opt_x[i,j] = 1
    for i in range(number_of_users):
        C[i] = f.find_C(i, opt_x)
    print(C)
else:
    opt_x = new_optimization.optimization()
print(opt_x)

fig, ax = plt.subplots()
G, colorlist, nodesize, edgesize, labels, edgecolor = f.make_graph(x_bs, y_bs, x_user, y_user, opt_x, number_of_users)
f.draw_graph(G, colorlist, nodesize, edgesize, labels, ax, color = 'black', edgecolor = edgecolor)
plt.show()


if Plot_Interference:
    delta = 100
    bound = 10
    grid_size = (xmax + 2*bound)/delta
    x_grid = np.arange(xmin - bound, xmax + bound, grid_size)
    y_grid = np.arange(ymin - bound, ymax + bound, grid_size)
    x_mesh,y_mesh = np.meshgrid(x_grid,y_grid)
    xc, yc = x_mesh + grid_size/2, y_mesh + grid_size/2

    interference = np.zeros((delta, delta))
    j = (x_bs[bs_of_interest], y_bs[bs_of_interest])
    for x in range(delta):
        for y in range(delta):
            interference[y, x] = f.find_interference((xc[0, x], yc[y, 0]), j, opt_x)

    fig, ax = plt.subplots()
    vmin, vmax = 0, np.max(interference)/10
    contour_z1 = ax.pcolormesh(x_grid, y_grid, interference, vmin = vmin, vmax = vmax, cmap = 'turbo')
    fig.colorbar(ScalarMappable(norm=contour_z1.norm, cmap=contour_z1.cmap))
    plt.xlim((xmin - bound, xmax + bound))
    plt.ylim((ymin - bound, ymax + bound))
    f.draw_graph(G, colorlist, nodesize, edgesize, labels, ax, color = 'white', edgecolor=edgecolor)
    plt.show()