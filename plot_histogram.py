import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

import functions
from parameters import *
import seaborn as sns
import matplotlib.pylab as pylab

params = {'legend.fontsize': 'x-large',
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large',
          'lines.markersize': 8,
          'figure.autolayout': True}
pylab.rcParams.update(params)

colors = ['#904C77', '#E49AB0', '#ECB8A5', '#96ACB7', '#957D95'] * 100
markers = ['o', 'X', 'v', 's', '*', 'P', '1', '+']

mis = dict()
dis = dict()
deg = dict()

mis_user = dict()
mis_bs = dict()

for number_of_users in users:
    iteration_min = 0
    iteration_max = iterations[number_of_users]

    Heuristic = False
    SNRHeuristic = False

    k = 3

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(
        M) + 'k=' + str(max_connections) + 'active_beams=' + str(number_of_active_beams))

    if Heuristic:
        name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str('SNR_k=' + str(k) + name)

    if Clustered:
        name = str(name + '_clustered')

    misalignment = pickle.load(open(str('Data/grid_misalignment_bs' + name + '.p'), 'rb'))
    satisfaction = pickle.load(open(str('Data/satisfaction' + name + '.p'), 'rb'))
    mis_bs[number_of_users] = np.std(misalignment) * 2
    degrees = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
    capacity = pickle.load(open(str('Data/capacity_per_user' + name + '.p'), 'rb'))

    name = str(beamwidth_b) + 'b_' + str(number_of_users) + '_users_M=' + str(M) + 'k=' + str(max_connections)
    if Heuristic:
        name = str('heuristic_' + name)
    if Clustered:
        name = str(name + '_clustered')

    fig, ax = plt.subplots()
    data1 = misalignment
    plt.hist(data1, density=True, bins=np.arange(-(beamwidth_b / 2), (beamwidth_b / 2) + 0.1, 0.1),
             alpha=0.3)
    plt.axvline(x=2 * np.std(np.abs(data1)), color='r', label='$\\sigma(\\theta^b)$')
    plt.axvline(x=-2 * np.std(np.abs(data1)), color='r')
    plt.xlabel('Misalignment in degrees')
    # plt.legend()
    plt.savefig(str('Figures/' + name + '_misalignment.png'), dpi=300)
    plt.show()

print(mis_bs)

for number_of_users in users:
    iteration_min = 0
    iteration_max = iterations[number_of_users]

    Heuristic = False
    SNRHeuristic = False

    k = 3

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(
        M) + 'k=' + str(max_connections) + 'active_beams=' + str(number_of_active_beams))
    if Heuristic:
        name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str('SNR_k=' + str(k) + name)

    if Clustered:
        name = str(name + '_clustered')

    optimal = pickle.load(open(str('Data/assignment' + name + '.p'), 'rb'))
    xs = pickle.load(open(str('Data/xs' + name + '.p'), 'rb'))
    ys = pickle.load(open(str('Data/ys' + name + '.p'), 'rb'))

    distances = []

    for iteration in range(iteration_max):
        opt_x = optimal[iteration]
        x_user, y_user = xs[iteration], ys[iteration]
        for i in range(number_of_users):
            for j in range(number_of_bs):
                if opt_x[i, j] == 1:
                    user_coords = functions.user_coords(i, x_user, y_user)
                    bs_coords = functions.bs_coords(j)
                    distances.append(functions.find_distance(user_coords, bs_coords))

    fig, ax = plt.subplots()
    plt.hist(distances, density=True, alpha=0.3)

    plt.xlabel('Distance')
    # plt.legend()
    plt.savefig(str('Figures/' + name + '_distances.png'), dpi=300)
    plt.show()

