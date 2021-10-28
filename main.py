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

np.random.seed(seed)

x = new_optimization.optimization()

for t in range(number_of_timeslots):
    delta = 200
    grid_size = xmax/delta

    x_grid = np.arange(xmin, xmax, grid_size)
    y_grid = np.arange(ymin, ymax, grid_size)

    x_mesh,y_mesh = np.meshgrid(x_grid,y_grid)

    xc, yc = x_mesh + grid_size/2, y_mesh + grid_size/2

    interference = np.zeros((delta, delta))

    blub = 1

    i = (x_user[0], y_user[0])
    j = (x_bs[blub], y_bs[blub])
    # for x in range(delta):
    #     for y in range(delta):
    #         interference[y, x] = f.find_interference_coords((xc[0, x], yc[y, 0]), j, alpha, t)

    fig, ax = plt.subplots()


    # contour_z1 = plt.contourf(x_mesh, y_mesh, interference, cmap='turbo')
    # plt.colorbar(contour_z1)
    plt.scatter(x_user, y_user)
    plt.scatter(x_bs, y_bs)
    plt.xlim((xmin, xmax))
    plt.ylim((ymin, ymax))

    G, colorlist, nodesize, edgesize, labels = f.make_graph(x_bs, y_bs, x_user, y_user, x[:, :, t], number_of_users)
    f.draw_graph(G, colorlist, nodesize, edgesize, labels, ax)
    plt.title('t = ' + str(t))
    plt.show()

