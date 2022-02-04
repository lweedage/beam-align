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
import new_optimization_no_interference
import new_optimization
import os
import functions as f
from matplotlib.cm import ScalarMappable
from parameters import *

fig, ax = plt.subplots()

iteration = 5
for number_of_users in [100]:
    np.random.seed(iteration)
    x_user, y_user = f.find_coordinates(number_of_users)
    print(len(x_user))
    opt_x, capacity = new_optimization_no_interference.optimization(x_user, y_user)

    print('Average connections per user: ', np.sum(opt_x)/number_of_users)
    print('Capacity:', np.sum(capacity))

    calculated_capacity = f.find_capacity(opt_x, x_user ,y_user)
    calculated_capacity_per_user = f.find_capacity_per_user(opt_x, x_user ,y_user)

    print('Calculated capacity:', calculated_capacity)
    print(f.find_capacity(opt_x, x_user, y_user))
    # fig, ax = plt.subplots()
    # G, colorlist, nodesize, edgesize, labels, edgecolor = f.make_graph(x_bs, y_bs, x_user, y_user, opt_x, number_of_users)
    # f.draw_graph(G, colorlist, nodesize, edgesize, labels, ax, color = 'black', edgecolor = edgecolor)
    # bound = 0.1 * xDelta
    # plt.xlim((xmin - bound, xmax + bound))
    # plt.ylim((ymin - bound, ymax + bound))
    # ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    # plt.show()
#     n_bins = 50
#     plt.hist(calculated_capacity_per_user, n_bins, density=True, histtype='step',
#                                cumulative=True, label = f'{number_of_users} users')
# plt.legend()
# plt.xlabel('Capacity per user (Gbps)')
# plt.ylabel('CDF')
# plt.show()