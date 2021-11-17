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
from parameters import *
import functions as f

def find_metrics(x):
    BS_degrees = [int(x) for x in sum(x)]
    user_degrees = [int(x) for x in sum(np.transpose(x))]
    distances = []
    distances_MC = [[] for i in range(max(user_degrees) + 1)]
    for i in range(number_of_users):
        for j in range(number_of_bs):
            if int(x[i, j]) == 1:
                dist = f.find_distance(f.user_coords(i), f.bs_coords(j))
                distances.append(dist)
                distances_MC[user_degrees[i]].append(dist)
    return user_degrees, BS_degrees, distances, distances_MC

def histogram_BS_degree(x):
    bins = np.arange(0, np.max(x) + 1.5) - 0.5
    plt.hist(x, bins, density=True)
    plt.xlabel("# connections per BS")
    plt.show()

def histogram_user_degree(x):
    bins = np.arange(0, np.max(x) + 1.5) - 0.5
    plt.hist(x, bins, density=True)
    plt.xlabel("# connections per user")
    plt.show()

def histogram_link_distance(x):
    plt.hist(x, density=True)
    plt.xlabel("distance per link")
    plt.show()

def histogram_link_distance_MC(x):
    plt.boxplot(x, [f'$k={k}$' for k in range(len(x))])
    plt.xlabel("distance per link")
    plt.legend()
    plt.show()

def histogram_channel_capacity(x):
    print(x)
    plt.hist(x, density=True)
    plt.xlabel("Capacity per user")
    plt.show()

