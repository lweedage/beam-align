import pickle

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import matplotlib
from parameters import *

matplotlib.rcParams['font.size'] = 20
matplotlib.rcParams['legend.fontsize'] = 18 # using a size in points
matplotlib.rcParams['text.usetex'] = True
# matplotlib.rcParams['axes.grid'] = True
matplotlib.rcParams['lines.markersize'] = 7
matplotlib.rcParams['figure.autolayout'] = True
plt.rcParams['text.latex.preamble'] = " \\usepackage{amsmath} \\usepackage{gensymb} "
markers = ['o', 's', 'p', 'd', '*']

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
    plt.hist(data1, density=True, bins=np.arange(-(beamwidth_b / 2), (beamwidth_b / 2) + 0.1, 0.2),
             alpha=0.6, color=colors[0])
    plt.axvline(x=2 * np.std(np.abs(data1)), color='r', label='$\\sigma(\\theta^b)$')
    plt.axvline(x=-2 * np.std(np.abs(data1)), color='r')
    plt.xlabel('Misalignment in degrees')
    # plt.legend()
    plt.savefig(str('Figures/' + name + '_misalignment.pdf'), dpi=300)
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

    # for iteration in range(iteration_max):
    #     opt_x = optimal[iteration]
    #     x_user, y_user = xs[iteration], ys[iteration]
    #     for i in range(number_of_users):
    #         for j in range(number_of_bs):
    #             if opt_x[i, j] == 1:
    #                 user_coords = functions.user_coords(i, x_user, y_user)
    #                 bs_coords = functions.bs_coords(j)
    #                 distances.append(functions.find_distance(user_coords, bs_coords))
    #
    # fig, ax = plt.subplots()
    # plt.hist(distances, density=True, alpha=0.3)
    #
    # plt.xlabel('Distance')
    # # plt.legend()
    # plt.savefig(str('Figures/' + name + '_distances.pdf'), dpi=300)
    # plt.show()
