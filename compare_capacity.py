import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import functions as f
import time
import pickle


def average(x):
    return sum(x) / len(x)


beamwidths = [np.radians(5), np.radians(10), np.radians(15)]

capacity, capacitylos, disconnected_users = {i: [] for i in beamwidths}, {i: [] for i in beamwidths}, {i: [] for i in
                                                                                                       beamwidths}
heuristic_beamwidth_capacity, heuristic_beamwidth_capacitylos, disconnected_users_heuristic = {i: [] for i in
                                                                                               beamwidths}, {i: [] for i
                                                                                                             in
                                                                                                             beamwidths}, {
                                                                                                  i: [] for i in
                                                                                                  beamwidths}
MC_closest_heuristic_capacity, MC_SNR_heuristic_capacity = {i: {j: [] for j in [1, 2, 3, 4, 5]} for i in beamwidths}, {
    i: {j: [] for j in [1, 2, 3, 4, 5]} for i in beamwidths}

heuristic_beamwidth_usermis_capacity, heuristic_beamwidth_usermis_capacitylos, disconnected_users_heuristic_usermis = {
                                                                                                                          i: []
                                                                                                                          for
                                                                                                                          i
                                                                                                                          in
                                                                                                                          beamwidths}, {
                                                                                                                          i: []
                                                                                                                          for
                                                                                                                          i
                                                                                                                          in
                                                                                                                          beamwidths}, {
                                                                                                                          i: []
                                                                                                                          for
                                                                                                                          i
                                                                                                                          in
                                                                                                                          beamwidths}

heuristic_beamwidth_capacityfair_comparison, heuristic_beamwidth_capacitylosfair_comparison, disconnected_users_heuristicfair_comparison = {
                                                                                                                                               i: []
                                                                                                                                               for
                                                                                                                                               i
                                                                                                                                               in
                                                                                                                                               beamwidths}, {
                                                                                                                                               i: []
                                                                                                                                               for
                                                                                                                                               i
                                                                                                                                               in
                                                                                                                                               beamwidths}, {
                                                                                                                                               i: []
                                                                                                                                               for
                                                                                                                                               i
                                                                                                                                               in
                                                                                                                                               beamwidths}

user = [100, 300, 500, 750, 1000]
for beamwidth_b in beamwidths:
    for number_of_users in user:
        disconnected_users_heuristic[beamwidth_b].append(pickle.load(open(
            str('Data/disconnected_users' 'beamwidth_heuristicusers=' + str(number_of_users) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)) + '.p'), 'rb')))

        disconnected_users_heuristicfair_comparison[beamwidth_b].append(pickle.load(open(
            str('Data/disconnected_users' 'fair_comparisonbeamwidth_heuristicusers=' + str(
                number_of_users) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)) + '.p'), 'rb')))

        disconnected_users_heuristic_usermis[beamwidth_b].append(pickle.load(open(
            str('Data/disconnected_users' 'beamwidth_heuristic_with_usermisusers=' + str(
                number_of_users) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)) + '.p'), 'rb')))

        heuristic_beamwidth_capacity[beamwidth_b].append(pickle.load(open(
            str('Data/channel_capacity' + 'beamwidth_heuristic' + 'users=' + str(
                number_of_users) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)) + '.p'), 'rb')))

        heuristic_beamwidth_capacityfair_comparison[beamwidth_b].append(pickle.load(open(
            str('Data/channel_capacity' + 'fair_comparisonbeamwidth_heuristic' + 'users=' + str(
                number_of_users) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)) + '.p'), 'rb')))

        heuristic_beamwidth_usermis_capacity[beamwidth_b].append(pickle.load(open(
            str('Data/channel_capacity' + 'beamwidth_heuristic_with_usermis' + 'users=' + str(
                number_of_users) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)) + '.p'), 'rb')))

        heuristic_beamwidth_capacitylos[beamwidth_b].append(pickle.load(open(
            str('Data/channel_capacity_with_los' + 'beamwidth_heuristic' + 'users=' + str(
                number_of_users) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)) + '.p'), 'rb')))

        heuristic_beamwidth_capacitylosfair_comparison[beamwidth_b].append(pickle.load(open(
            str('Data/channel_capacity_with_los' + 'fair_comparisonbeamwidth_heuristic' + 'users=' + str(
                number_of_users) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)) + '.p'), 'rb')))

        heuristic_beamwidth_usermis_capacitylos[beamwidth_b].append(pickle.load(open(
            str('Data/channel_capacity_with_los' + 'beamwidth_heuristic_with_usermis' + 'users=' + str(
                number_of_users) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)) + '.p'), 'rb')))

        capacity[beamwidth_b].append(pickle.load(open(
            str('Data/channel_capacity' + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)) + '.p'), 'rb')))

        capacitylos[beamwidth_b].append(pickle.load(open(
            str('Data/channel_capacity_with_los' + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)) + '.p'), 'rb')))

        disconnected_users[beamwidth_b].append(pickle.load(open(
            str('Data/disconnected_users' + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)) + '.p'), 'rb')))

        for k in [1, 2, 3, 4, 5]:
            MC_SNR_heuristic_capacity[beamwidth_b][k].append(pickle.load(
                open(str('Data/channel_capacity' + 'SNR_' + 'k=' + str(k) + 'users=' + str(
                    number_of_users) + 'beamwidth_b=' + str(
                    np.degrees(beamwidth_b)) + '.p'), 'rb')))

            MC_closest_heuristic_capacity[beamwidth_b][k].append(pickle.load(
                open(str('Data/channel_capacity' + 'closest_k=' + str(k) + 'users=' + str(
                    number_of_users) + 'beamwidth_b=' + str(
                    np.degrees(beamwidth_b)) + '.p'), 'rb')))

        print(average(disconnected_users_heuristic[beamwidth_b][-1]))

fig, ax = plt.subplots()
for i, beamwidth_b in zip(range(3), beamwidths):
    if beamwidth_b == np.radians(5):
        name = '$5\degree$'
    elif beamwidth_b == np.radians(10):
        name = '$10\degree$'
    elif beamwidth_b == np.radians(15):
        name = '$15\degree$'

    avg_capacity = [sum(capacity[beamwidth_b][i]) / max(1, len(capacity[beamwidth_b][i])) for i in range(len(user))]
    avg_beamwidth_capacity = [
        sum(heuristic_beamwidth_capacity[beamwidth_b][i]) / len(heuristic_beamwidth_capacity[beamwidth_b][i]) for
        i in range(len(user))]

    plt.plot(user, avg_capacity, '-o', color=colors[i], label=name + ' optimal')
    plt.plot(user, avg_beamwidth_capacity, '--*', color=colors[i], label=name + ' beamwidth')
    # plt.plot(user,
    #          [sum(heuristic_beamwidth_capacityfair_comparison[beamwidth_b][i]) / len(heuristic_beamwidth_capacityfair_comparison[beamwidth_b][i]) for
    #           i in range(len(user))],
    #          '--*', color=colors[i], label=name + ' beamwidth-fair')
    # plt.plot(user,
    #          [sum(heuristic_beamwidth_usermis_capacity[beamwidth_b][i]) / len(heuristic_beamwidth_usermis_capacity[beamwidth_b][i]) for
    #           i in range(len(user))],
    #          '-.d', color=colors[i], label=name + ' beamwidth-both')

plt.xlabel('Number of users')
plt.ylabel('Total channel capacity (Gbit/s/Hz)')
plt.legend()
plt.show()

disconnected_heuristic = [[0.006 / 100 * 100, 1.0809 / 300 * 100, 12.542 / 500 * 100, 60.37631184407796 / 750 * 100,
                           151.854 / 1000 * 100],
                          [1.2532 / 100 * 100, 26.499 / 300 * 100, 98.847 / 500 * 100, 242.4692 / 750 * 100,
                           424.002 / 1000 * 100],
                          [11.133 / 100 * 100, 73.28194361127774 / 300 * 100, 183.85 / 500 * 100,
                           367.32833583208395 / 750 * 100,
                           579.996 / 1000 * 100]]

disconnected_heuristic_faircomparison = [
    [0.0024 / 100 * 100, 0.46850629874025196 / 300 * 100, 12.542 / 500 * 100, 60.37631184407796 / 750 * 100,
     151.854 / 1000 * 100],
    [0.8702 / 100 * 100, 16.699460107978403 / 300 * 100, 98.847 / 500 * 100, 242.4692 / 750 * 100,
     424.002 / 1000 * 100],
    [8.9214 / 100 * 100, 45.887222555488904 / 300 * 100, 183.85 / 500 * 100,
     367.32833583208395 / 750 * 100,
     579.996 / 1000 * 100]]

disconnected_heuristic_both = [
    [0.006 / 100 * 100, 1.0641871625674866 / 300 * 100, 12.542 / 500 * 100, 60.18740629685158 / 750 * 100,
     151.96 / 1000 * 100],
    [1.2748 / 100 * 100, 26.729454109178164 / 300 * 100, 99.464 / 500 * 100, 243.70914542728636 / 750 * 100,
     426.286 / 1000 * 100],
    [11.1826 / 100 * 100, 73.24955008998201 / 300 * 100, 183.747 / 500 * 100,
     367.503748125937 / 750 * 100,
     580.74 / 1000 * 100]]
disconnected = [[0, 0, 0, 0, 0],
                [0.0596 / 100 * 100, 0.19916 / 300 * 100, 0.316 / 500 * 100, 0.5712143 / 750 * 100,
                 143.014 / 1000 * 100],
                [6.1478 / 100 * 100, 23.668266346730654 / 300 * 100, 59.066 / 500 * 100, 209.07946026986508 / 750 * 100,
                 433.116 / 1000 * 100]]


fix, ax = plt.subplots()
plt.plot(user, disconnected_heuristic[0], '--*', label='5$\degree$ beamwidth', color=colors[0])
# plt.plot(user, disconnected_heuristic_both[0], '-.d', label='5$\degree$ beamwidth-both', color=colors[0])
plt.plot(user, disconnected[0], '-o', label='5$\degree$', color=colors[0])
plt.plot(user, disconnected_heuristic[1], '--*', label='10$\degree$ beamwidth', color=colors[1])
# plt.plot(user, disconnected_heuristic_both[1], '-.d', label='10$\degree$ beamwidth-both', color=colors[1])
plt.plot(user, disconnected[1], '-o', label='10$\degree$', color=colors[1])
plt.plot(user, disconnected_heuristic[2], '--*', label='15$\degree$ beamwidth', color=colors[2])
# plt.plot(user, disconnected_heuristic_both[2], '-.d', label='15$\degree$ beamwidth-both', color=colors[2])
plt.plot(user, disconnected[2], '-*', label='15$\degree$', color=colors[2])

plt.xlabel('Number of users')
plt.ylabel('Average percentage of disconnected users')
plt.legend()
plt.show()

fig, ax = plt.subplots()
for i, beamwidth_b in zip(range(3), beamwidths):
    if beamwidth_b == np.radians(5):
        name = '$5\degree$'
    elif beamwidth_b == np.radians(10):
        name = '$10\degree$'
    elif beamwidth_b == np.radians(15):
        name = '$15\degree$'

    avg_capacity = [sum(capacity[beamwidth_b][i]) / max(1, len(capacity[beamwidth_b][i])) for i in range(len(user))]
    avg_beamwidth_capacity = [
        sum(heuristic_beamwidth_capacity[beamwidth_b][i]) / len(heuristic_beamwidth_capacity[beamwidth_b][i]) for
        i in range(len(user))]

    plt.plot(user, np.subtract(1,np.divide(disconnected[i], 100)) * avg_capacity, '-o', label=name + ' optimal', color=colors[i])
    plt.plot(user, np.subtract(1,np.divide(disconnected_heuristic[i], 100)) * avg_beamwidth_capacity, '--*', label=name + ' heuristic', color=colors[i])

plt.xlabel('Number of users')
plt.ylabel('(1-disconnected) * throughput')
plt.legend()
plt.show()

print(average(MC_SNR_heuristic_capacity[beamwidth_b][1][0]))
for beamwidth in beamwidths:
    fig, ax = plt.subplots()
    plt.plot(user, [average(heuristic_beamwidth_capacity[beamwidth][i]) for i in range(len(user))], '-o',
             label='beamwidth')
    plt.plot(user, [average(MC_SNR_heuristic_capacity[beamwidth][1][i]) for i in range(len(user))], '-*',
             label='$SNR - k = 1$')
    plt.plot(user, [average(MC_SNR_heuristic_capacity[beamwidth][2][i]) for i in range(len(user))], '-d',
             label='$SNR - k = 2$')
    plt.plot(user, [average(MC_SNR_heuristic_capacity[beamwidth][3][i]) for i in range(len(user))], '-+',
             label='$SNR - k = 3$')
    plt.plot(user, [average(MC_SNR_heuristic_capacity[beamwidth][4][i]) for i in range(len(user))], '-v',
             label='$SNR - k = 4$')
    plt.plot(user, [average(MC_SNR_heuristic_capacity[beamwidth][5][i]) for i in range(len(user))], '-1',
             label='$SNR - k = 5$')

    plt.legend()
    plt.xlabel('Number of users')
    plt.ylabel('Total channel capacity (Gbit/s/Hz)')
    plt.show()
#
#     fig, ax = plt.subplots()
#     plt.plot(user, [average(heuristic_beamwidth_capacity[beamwidth][i]) for i in range(len(user))], '-o',
#              label='beamwidth')
#     plt.plot(user, [average(MC_closest_heuristic_capacity[beamwidth][1][i]) for i in range(len(user))], '-*',
#              label='$Closest - k = 1$')
#     plt.plot(user, [average(MC_closest_heuristic_capacity[beamwidth][2][i]) for i in range(len(user))], '-d',
#              label='$Closest - k = 2$')
#     plt.plot(user, [average(MC_closest_heuristic_capacity[beamwidth][3][i]) for i in range(len(user))], '-+',
#              label='$Closest - k = 3$')
#     plt.plot(user, [average(MC_closest_heuristic_capacity[beamwidth][4][i]) for i in range(len(user))], '-v',
#              label='$Closest - k = 4$')
#     plt.plot(user, [average(MC_closest_heuristic_capacity[beamwidth][5][i]) for i in range(len(user))], '-1',
#              label='$Closest - k = 5$')
#
#     plt.legend()
#     plt.xlabel('Number of users')
#     plt.ylabel('Total channel capacity (Gbit/s/Hz)')
#     plt.show()

fig, ax = plt.subplots()
for i, beamwidth_b in [(0, np.radians(15))]: #zip(range(3), beamwidths):
    if beamwidth_b == np.radians(5):
        name = '$5\degree$'
    elif beamwidth_b == np.radians(10):
        name = '$10\degree$'
    elif beamwidth_b == np.radians(15):
        name = '$15\degree$'

    avg_capacitylos = [sum(capacitylos[beamwidth_b][i]) / max(1, len(capacitylos[beamwidth_b][i])) for i in range(len(user))]
    avg_beamwidth_capacitylos = [
        sum(heuristic_beamwidth_capacitylos[beamwidth_b][i]) / len(heuristic_beamwidth_capacitylos[beamwidth_b][i]) for
        i in range(len(user))]

    plt.plot(user, avg_capacitylos, '-o', color=colors[0], label=name + ' optimal - los')
    plt.plot(user, avg_beamwidth_capacitylos, '--*', color=colors[0], label=name + ' beamwidth - los')

    avg_capacity = [sum(capacity[beamwidth_b][i]) / max(1, len(capacity[beamwidth_b][i])) for i in range(len(user))]
    avg_beamwidth_capacity = [
        sum(heuristic_beamwidth_capacity[beamwidth_b][i]) / len(heuristic_beamwidth_capacity[beamwidth_b][i]) for
        i in range(len(user))]

    plt.plot(user, avg_capacity, '-o', color=colors[1], label=name + ' optimal')
    plt.plot(user, avg_beamwidth_capacity, '--*', color=colors[1], label=name + ' beamwidth')
    # plt.plot(user,
    #          [sum(heuristic_beamwidth_capacityfair_comparison[beamwidth_b][i]) / len(heuristic_beamwidth_capacityfair_comparison[beamwidth_b][i]) for
    #           i in range(len(user))],
    #          '--*', color=colors[i], label=name + ' beamwidth-fair')
    # plt.plot(user,
    #          [sum(heuristic_beamwidth_usermis_capacity[beamwidth_b][i]) / len(heuristic_beamwidth_usermis_capacity[beamwidth_b][i]) for
    #           i in range(len(user))],
    #          '-.d', color=colors[i], label=name + ' beamwidth-both')

plt.xlabel('Number of users')
plt.ylabel('Total channel capacity (Gbit/s/Hz)')
plt.legend()
plt.show()