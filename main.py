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

alpha, channel_capacity_per_user = new_optimization.optimization()

print(alpha)

print(channel_capacity_per_user)

for t in range(number_of_timeslots):
    G, colorlist, nodesize, edgesize, labels = f.make_graph(x_bs, y_bs, x_user, y_user, alpha[:,:,t], number_of_users)
    f.draw_graph(G, colorlist, nodesize, edgesize, labels)
    plt.show()


fig, ax = plt.subplots()
plt.hist(channel_capacity_per_user, density=True)
plt.show()