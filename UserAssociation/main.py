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
import analysis
import new_optimization_no_interference
import new_optimization
import os
import functions as f
from matplotlib.cm import ScalarMappable
from parameters import *

for iteration in range(1):
    np.random.seed(iteration)
    #
    # opt_x = np.zeros((number_of_users, number_of_bs))
    # for i in range(number_of_users):
    #     j = f.find_closest_bs(i)
    #     opt_x[i,j] = 1
    x_user, y_user = f.find_coordinates()
    # x_user, y_user = [xmin + i*(xmax-xmin)/(number_of_users - 1) for i in range(number_of_users)], [5] * number_of_users
    if Interference:
        opt_x, capacity = new_optimization.optimization(x_user, y_user)
    else:
        opt_x, capacity = new_optimization_no_interference.optimization(x_user, y_user)

    print('Average connections per user: ', np.sum(opt_x)/number_of_users)

    fig, ax = plt.subplots()
    G, colorlist, nodesize, edgesize, labels, edgecolor = f.make_graph(x_bs, y_bs, x_user, y_user, opt_x, number_of_users)
    f.draw_graph(G, colorlist, nodesize, edgesize, labels, ax, color = 'black', edgecolor = edgecolor)
    bound = 0.1 * xDelta
    plt.xlim((xmin - bound, xmax + bound))
    plt.ylim((ymin - bound, ymax + bound))
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.show()


if Plot_Interference:
    delta = 200
    bound = 10
    grid_size = (xmax + 2*bound)/delta
    x_grid = np.arange(xmin - bound, xmax + bound, grid_size)
    y_grid = np.arange(ymin - bound, ymax + bound, grid_size)
    x_mesh,y_mesh = np.meshgrid(x_grid,y_grid)
    xc, yc = x_mesh + grid_size/2, y_mesh + grid_size/2
    j = (x_bs[bs_of_interest], y_bs[bs_of_interest])
    for bs in range(number_of_bs):
        interference = np.zeros((delta, delta))
        j = (x_bs[bs], y_bs[bs])
        for x in range(delta):
            for y in range(delta):
                interference[y, x] = f.find_interference((xc[0, x], xc[0, y]), j, opt_x)

        fig, ax = plt.subplots()
        vmin, vmax = 0, np.max(interference)/10
        contour_z1 = ax.pcolormesh(x_grid, x_grid.transpose(), interference, vmin = vmin, vmax = vmax, cmap = 'turbo')
        fig.colorbar(ScalarMappable(norm=contour_z1.norm, cmap=contour_z1.cmap))
        plt.xlim((xmin - bound, xmax + bound))
        plt.ylim((ymin - bound, ymax + bound))
        f.draw_graph(G, colorlist, nodesize, edgesize, labels, ax, color = 'white', edgecolor=edgecolor)
        plt.show()


degree_U, degree_BS, link_distances, link_distances_MC = analysis.find_metrics(opt_x, x_user, y_user)
#
# analysis.histogram_user_degree(degree_U)
# analysis.histogram_BS_degree(degree_BS)
# analysis.histogram_link_distance(link_distances)
# analysis.histogram_link_distance_MC(link_distances_MC)
#
# analysis.histogram_channel_capacity(capacity)