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
from scipy.spatial import Voronoi, voronoi_plot_2d
import initialization
from matplotlib.cm import ScalarMappable
import seaborn
from scipy.optimize import curve_fit

colors = seaborn.color_palette('rocket')
colors.reverse()

for simulation_number in [1, 4, 7, 10, 13, 16, 19, 22]:
    seed = 5

    name = 'Simulations/simulation_' + str(simulation_number) + 'seed' + str(seed)
    hexagonal, ppp, number_of_users_1, number_of_users_2, number_of_users_3, OBJECTIVE, number_of_iterations, blub = initialization.initialization(
        simulation_number)

    if OBJECTIVE == 0:
        obj = 'log'
    elif OBJECTIVE == 1:
        obj = 'sum'

    channel1 = np.loadtxt(name + 'channel_type1' + obj + 'SNR' + str(number_of_iterations - 1) + '.txt')
    channel2 = np.loadtxt(name + 'channel_type2' + obj + 'SNR' + str(number_of_iterations - 1) + '.txt')
    channel3 = np.loadtxt(name + 'channel_type3' + obj + 'SNR' + str(number_of_iterations - 1) + '.txt')

    data = [channel1, channel2, channel3]


    fig, ax = plt.subplots()
    plt.boxplot(data)
    # plt.title(str(simulation_number))
    plt.ylabel('$C_{ij}^g$')
    plt.savefig('simulation' + str(simulation_number) + 'boxplot.png')
    plt.show()

    fig, ax = plt.subplots()
    plt.hist(channel1, alpha = 0.4, density = True, color = colors[1], label = 'Type 1')
    plt.hist(channel2, alpha = 0.4, density = True, color = colors[2], label = 'Type 2')
    plt.hist(channel3, alpha = 0.4, density = True, color = colors[3], label = 'Type 3')
    # plt.title(str(simulation_number))
    plt.xlabel('$C_{ij}^g$')
    plt.legend()

    plt.savefig('simulation' + str(simulation_number) + 'histogram.png')

    plt.show()