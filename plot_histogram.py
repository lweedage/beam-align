import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from parameters import *
import seaborn as sns

colors = sns.color_palette("ch:s=-.2,r=.6")

# number_of_users = int(input('Number of users?'))
user = [100, 300, 500, 750, 1000]
# user = [500]

mis = dict()
dis = dict()
deg = dict()

mis_user = dict()
mis_bs = dict()

for number_of_users in user:
    iteration_min = 0
    iteration_max = iterations[number_of_users]

    Heuristic = False
    SNRHeuristic = False
    User_Heuristic = False
    GreedyRate = False
    GreedyHeuristic = False


    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(
        np.degrees(beamwidth_b)) + 'M=' + str(M) + 's=' + str(users_per_beam))

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
    misalignment_bs = pickle.load(open(str('Data/grid_misalignment_bs' + name + '.p'), 'rb'))
    misalignment_mc = pickle.load(open(str('Data/grid_misalignment_mc' + name + '.p'), 'rb'))
    misalignment_sc = pickle.load(open(str('Data/grid_misalignment_sc' + name + '.p'), 'rb'))

    mis_bs[number_of_users] = np.std(misalignment_bs) * 2


    # distances = pickle.load(open(str('Data/distances' + name + '.p'), 'rb'))
    # distances_mc = pickle.load(open(str('Data/distances_mc' + name + '.p'), 'rb'))
    # distances_sc = pickle.load(open(str('Data/distances_sc' + name + '.p'), 'rb'))
    #
    # degrees = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
    # deg[number_of_users] = sum(degrees)/len(degrees)
    #
    # degrees = [i for i in degrees if i != 0]


    # disconnected = pickle.load(open(str('Data/disconnected_users' + name + '.p'), 'rb'))

    name = str(int(math.ceil(np.degrees(beamwidth_b)))) + 'b_' + str(number_of_users) + '_users_M=' + str(M) + 's='  + str(users_per_beam)
    if Heuristic:
        name = str('heuristic_' + name)

    fig, ax = plt.subplots()
    data1 = misalignment_sc
    data2 = misalignment_mc
    plt.hist(data1, density=True, bins=np.arange(-np.degrees(beamwidth_b / 2), np.degrees(beamwidth_b / 2) + 0.1, 0.1),
             alpha=0.3, label='single connections')
    plt.hist(data2, density=True, bins=np.arange(-np.degrees(beamwidth_b / 2), np.degrees(beamwidth_b / 2) + 0.1, 0.1),
             alpha=0.3, label='multiple connections')
    plt.xlabel('Misalignment in degrees')
    plt.legend()
    plt.savefig(str('Figures/' + name + '_misalignmentmc.png'))
    # plt.show()

    fig, ax = plt.subplots()
    data1 = misalignment_user
    (n, bins, patches) = plt.hist(data1, density=True, bins=np.arange(-np.degrees(beamwidth_b / 2), np.degrees(beamwidth_b / 2) + 0.1, 0.1),
             alpha=0.3)
    plt.xlabel('Misalignment in degrees')
    plt.savefig(str('Figures/' + name + '_user_misalignment.png'))
    # plt.show()
    mis_user[number_of_users] = np.std(data1) * 2
    # print(np.std(data1) * 2)

print(f'misalignment_user={mis_user}')
print(f'misalignment={mis_bs}')


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


# degrees = {i: [] for i in beamwidths}
# for beamwidth_b in beamwidths:
#     for number_of_users in user:
#         name = str('users=' + str(number_of_users) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)) + 'M=' + str(
#             M) + 's=' + str(users_per_beam))
#         degrees[beamwidth_b].append(pickle.load(open(
#             str('Data/total_links_per_user' + name + '.p'), 'rb')))
#
#     fig, ax = plt.subplots()
#     bplot = plt.boxplot(degrees[beamwidth_b], showfliers=False, patch_artist=True, medianprops={'color': 'black'})
#     for patch, color in zip(bplot['boxes'], colors[:5]):
#         patch.set_facecolor(color)
#     plt.xticks([1, 2, 3, 4, 5], user)
#     plt.xlabel('Number of users')
#     plt.ylabel('Number of connections per user')
#     plt.savefig('Figures/links_all_users'  + name + '.png')
#     plt.show()

