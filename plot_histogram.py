import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from parameters import *
import seaborn as sns

colors = sns.color_palette("ch:s=-.2,r=.6")

# number_of_users = int(input('Number of users?'))
# user = [500]

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
    User_Heuristic = False
    GreedyRate = False
    GreedyHeuristic = False

    k = 0

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(
        M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))

    if Heuristic:
        if User_Heuristic:
            name = str('beamwidth_user_heuristic' + name)
        else:
            name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str('SNR_k=' + str(k) + name)

    elif GreedyRate:
        name = str(name + 'GreedyRate')
    elif GreedyHeuristic:
        name = str(name + 'GreedyHeuristic')

    if Clustered:
        name = str(name + '_clustered')



    misalignment_user = pickle.load(open(str('Data/grid_misalignment_user' + name + '.p'), 'rb'))
    misalignment = pickle.load(open(str('Data/grid_misalignment_bs' + name + '.p'), 'rb'))
    misalignment_mc = pickle.load(open(str('Data/grid_misalignment_mc' + name + '.p'), 'rb'))
    misalignment_sc = pickle.load(open(str('Data/grid_misalignment_sc' + name + '.p'), 'rb'))

    satisfaction = pickle.load(open(str('Data/satisfaction' + name + '.p'), 'rb'))
    average_distance = pickle.load(open(str('Data/average_distance' + name + '.p'), 'rb'))
    mis_bs[number_of_users] = np.std(misalignment) * 2

    degrees = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))

    distances = pickle.load(open(str('Data/distances' + name + '.p'), 'rb'))
    capacity = pickle.load(open(str('Data/channel_capacity_per_user' + name + '.p'), 'rb'))


    name = str(beamwidth_b) + 'b_' + str(number_of_users) + '_users_M=' + str(M) + 's='  + str(users_per_beam)
    if Heuristic:
        name = str('heuristic_' + name)

    fig, ax = plt.subplots()
    data1 = misalignment
    plt.hist(data1, density=True, bins=np.arange(-(beamwidth_b / 2), (beamwidth_b / 2) + 0.1, 0.1),
             alpha=0.3)
    plt.xlabel('Misalignment in degrees')
    # plt.legend()
    plt.savefig(str('Figures/' + name + '_misalignment.png'), dpi = 300)
    # plt.show()


    fig, ax = plt.subplots()
    data = distances
    step = 5
    if data:
        plt.hist(data, density=True) #, bins=np.arange(min(data), max(data) + step, step), alpha=0.3)
    plt.xlabel('Link distance (m)')
    plt.savefig(str('Figures/' + name + '_distances.png'))
    # plt.show()

    fig, ax = plt.subplots()
    plt.scatter(average_distance, satisfaction)
    # plt.xlabel('Number of connections')
    plt.savefig(str('Figures/' + name + '_distance_satisfaction.png'))

    fig, ax = plt.subplots()
    plt.scatter(average_distance, degrees)
    # plt.xlabel('Number of connections')
    plt.savefig(str('Figures/' + name + '_distance_degree.png'))

    fig, ax = plt.subplots()
    plt.scatter(average_distance, capacity)
    # plt.xlabel('Number of connections')
    plt.savefig(str('Figures/' + name + '_distance_rate.png'))
    # print(misalignment_bs)


    plt.show()