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

np.random.seed(1)
x_user, y_user = f.find_coordinates()

opt_x = np.zeros((number_of_users, number_of_bs))

fig, ax = plt.subplots()
G, colorlist, nodesize, edgesize, labels, edgecolor = f.make_graph(x_bs, y_bs, x_user, y_user, opt_x, number_of_users)
f.draw_graph(G, colorlist, nodesize, edgesize, labels, ax, color = 'black', edgecolor = edgecolor)
bound = 0.1 * xDelta
plt.xlim((xmin - bound, xmax + bound))
plt.ylim((ymin - bound, ymax + bound))
ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
plt.show()

def find_sorted_users_torus(bs, x_user, y_user):
    x = np.minimum((bs[0] - np.array(x_user)) % xDelta, (np.array(x_user) - bs[0]) % xDelta)
    y = np.minimum((bs[1] - np.array(y_user)) % yDelta, (np.array(y_user) - bs[1]) % yDelta)
    return np.argsort(np.sqrt(x ** 2 + y ** 2))


def find_closest(bs):
    users = []
    possible_directions = list(directions_bs)
    bs_coords = f.bs_coords(bs)
    sorted_users = find_sorted_users_torus(bs_coords, x_user, y_user)
    for u in sorted_users:
        user_coord = f.user_coords(u, x_user, y_user)
        (bs_x, bs_y) = bs_coords
        (user_x, user_y) = user_coord
        if (max(bs_coords[0], user_coord[0]) - min(bs_coords[0], user_coord[0])) > (min(bs_coords[0], user_coord[0]) - max(bs_coords[0], user_coord[0])) % xDelta:
            if bs_coords[0] > user_coord[0]:
                bs_x = bs_coords[0] - xDelta
            else:
                user_x = user_coord[0] - xDelta

        if (max(bs_coords[1], user_coord[1]) - min(bs_coords[1], user_coord[1])) > (min(bs_coords[1], user_coord[1]) - max(bs_coords[1], user_coord[1])) % yDelta:
            if bs_coords[1] > user_coord[1]:
                bs_y = bs_coords[1] - yDelta
            else:
                user_y = user_coord[1] - yDelta

        new_bs = (bs_x, bs_y)
        new_user = (user_x, user_y)
        beam_number = f.find_beam_number(f.find_beam(f.find_geo(new_bs, new_user), beamwidth_b), beamwidth_b)
        if beam_number in possible_directions:
            possible_directions.remove(beam_number)
            users.append(u)
            print(u, bs, np.degrees(f.find_beam(f.find_geo(new_bs, new_user), beamwidth_b)))

    return users


for bs in range(number_of_bs):
    u = find_closest(bs)
    for user in u:
        opt_x[user, bs] = 1

print([(x_user[i], y_user[i]) for i in range(number_of_users)])


fig, ax = plt.subplots()
G, colorlist, nodesize, edgesize, labels, edgecolor = f.make_graph(x_bs, y_bs, x_user, y_user, opt_x, number_of_users)
f.draw_graph(G, colorlist, nodesize, edgesize, labels, ax, color = 'black', edgecolor = edgecolor)
bound = 0.1 * xDelta
plt.xlim((xmin - bound, xmax + bound))
plt.ylim((ymin - bound, ymax + bound))
ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
plt.show()