import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

from parameters import *

number_of_users = int(input('Number of users?'))
user = [100, 500, 1000]

for number_of_users in [100]: #user:
    print(number_of_users)
    iteration_min = 0
    iteration_max = iterations[number_of_users]

    Heuristic = False

    start = time.time()
    if Heuristic:
        name = str(
            'beamwidth_heuristic' + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)))
    else:
        name = str(
            'users=' + str(number_of_users) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)) + 'M=' + str(
                M) + 's=' + str(
                s[0]))

    beamwidths = [np.radians(5)] #, np.radians(10), np.radians(15)]

    degrees = {i: [] for i in beamwidths}

    for beamwidth_b in beamwidths:
        for number_of_users in user:
            name = str('users=' + str(number_of_users) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)) + 'M=' + str(
                M) + 's=' + str(s[0]))
            degrees[beamwidth_b].append(pickle.load(open(
                str('Data/total_links_per_user' + name + '.p'), 'rb')))

        fig, ax = plt.subplots()
        bplot = plt.boxplot(degrees[beamwidth_b], showfliers=False, patch_artist=True, medianprops={'color': 'black'})
        for patch, color in zip(bplot['boxes'], colors[:5]):
            patch.set_facecolor(color)
        plt.xticks([1, 2, 3], user)
        plt.xlabel('Number of users')
        plt.ylabel('Number of connections per user')
        plt.show()

    misalignment_user = pickle.load(open(str('Data/grid_misalignment_user' + name + '.p'), 'rb'))
    misalignment_bs = pickle.load(open(str('Data/grid_misalignment_bs' + name + '.p'), 'rb'))
    misalignment_mc = pickle.load(open(str('Data/grid_misalignment_mc' + name + '.p'), 'rb'))
    misalignment_sc = pickle.load(open(str('Data/grid_misalignment_sc' + name + '.p'), 'rb'))

    distances = pickle.load(open(str('Data/distances' + name + '.p'), 'rb'))
    distances_mc = pickle.load(open(str('Data/distances_mc' + name + '.p'), 'rb'))
    distances_sc = pickle.load(open(str('Data/distances_sc' + name + '.p'), 'rb'))

    degrees = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
    degrees = [i for i in degrees if i != 0]

    disconnected = pickle.load(open(str('Data/disconnected_users' + name + '.p'), 'rb'))

    data = misalignment_bs

    print('2 sigma misalignment', np.degrees(np.std(data) * 2))

    print('Disconnected users:', np.sum(disconnected) / len(disconnected))
    if not (Heuristic):
        no_optimal_value = pickle.load(open(str('Data/no_optimal_value_found' + name + '.p'), 'rb'))
        print('No succes in', no_optimal_value / iterations[number_of_users] * 100, 'percent of the iterations')

    name = str(int(math.ceil(np.degrees(beamwidth_b)))) + 'b_' + str(number_of_users) + '_users'
    if Heuristic:
        name = str('heuristic_' + name)

    # fig, ax = plt.subplots()
    # data1 = np.degrees(misalignment_sc)
    # data2 = np.degrees(misalignment_mc)
    # plt.hist(data1, density=True, bins=np.arange(-np.degrees(beamwidth_b / 2), np.degrees(beamwidth_b / 2) + 0.1, 0.1),
    #          alpha=0.3, label='single connections')
    # plt.hist(data2, density=True, bins=np.arange(-np.degrees(beamwidth_b / 2), np.degrees(beamwidth_b / 2) + 0.1, 0.1),
    #          alpha=0.3, label='multiple connections')
    # plt.xlabel('Misalignment in degrees')
    # plt.legend()
    # plt.savefig(str('Figures/' + name + '_misalignment.png'))
    # plt.show()

    # fig, ax = plt.subplots()
    # data = distances_sc
    # if data:
    #     plt.hist(data, density=True, bins=np.arange(min(data), 55 + step, step), alpha=0.3, label='single connections')
    # data = distances_mc
    # if data:
    #     plt.hist(data, density=True, bins=np.arange(min(data), 55 + step, step), alpha=0.3,
    #              label='multiple connections')
    # plt.legend()
    # plt.xlabel('Link distance (m)')
    # plt.savefig(str('Figures/' + name + '_distances.png'))
    # plt.show()

    # fig, ax = plt.subplots()
    # step = 2
    # data = distances_2mc
    # plt.hist(data, density=True, bins = np.arange(min(data), 55 + step, step), alpha = 0.3, label = '2mc')
    # data = distances_3mc
    # plt.hist(data, density=True, bins = np.arange(min(data), 55 + step, step), alpha = 0.3, label = '3mc')
    # data = distances_4mc
    # plt.hist(data, density=True, bins = np.arange(min(data), 55 + step, step), alpha = 0.3, label = '4mc')
    # data = distances_5mc
    # plt.hist(data, density=True, bins = np.arange(min(data), 55 + step, step), alpha = 0.3, label = '>5mc')
    # plt.xlabel('Link distance (m)')
    # plt.legend()
    # plt.show()

    # fig, ax = plt.subplots()
    # plt.hist(degrees, density=True)
    # plt.xlabel('Number of connections')
    # plt.savefig(str('Figures/' + name + '_degrees.png'))
    # print('Average number of connections:', sum(degrees) / len(degrees))
    # plt.show()

    # print(misalignment_bs)

    # fig, ax = plt.subplots()
    # plt.scatter(np.degrees(np.abs(misalignment_bs)), distances, s = 0.5, label = 'SC')
    # plt.scatter(np.degrees(np.abs(misalignment_mc)), distances_mc, s = 0.5, label = 'MC')
    # plt.xlabel('Misalignment')
    # plt.ylabel('Distance')
    # plt.legend()
    # plt.savefig(str('Figures/' + name + '_degrees_scatter.png'))
    # plt.show()
