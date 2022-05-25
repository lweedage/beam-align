import pickle
import matplotlib.pyplot as plt
import numpy as np

from parameters import *


def average(x):
    return sum(x) / len(x)


beamwidths = [np.radians(5), np.radians(10), np.radians(15)]
# beamwidths = [np.radians(5)]

capacity = {i: [] for i in beamwidths}
capacity2 = {i: [] for i in beamwidths}
capacity3 = {i: [] for i in beamwidths}

capacitylos = {i: [] for i in beamwidths}
disconnected_users = {i: [] for i in beamwidths}

capacity_nopenalty = {i: [] for i in beamwidths}
capacitylos_nopenalty = {i: [] for i in beamwidths}
disconnected_users_nopenalty = {i: [] for i in beamwidths}

heuristic_beamwidth_capacity = {i: [] for i in beamwidths}
heuristic_beamwidth_capacitylos = {i: [] for i in beamwidths}
disconnected_users_heuristic = {i: [] for i in beamwidths}

MC_closest_heuristic_capacity = {i: {j: [] for j in [1, 2, 3, 4, 5]} for i in beamwidths}
MC_SNR_heuristic_capacity = {i: {j: [] for j in [1, 2, 3, 4, 5, 24]} for i in beamwidths}

MC_closest_disconnected = {i: {j: [] for j in [1, 2, 3, 4, 5]} for i in beamwidths}
MC_SNR_disconnected = {i: {j: [] for j in [1, 2, 3, 4, 5, 24]} for i in beamwidths}

heuristic_beamwidth_usermis_capacity = {i: [] for i in beamwidths}
heuristic_beamwidth_usermis_capacitylos = {i: [] for i in beamwidths}

user = [100, 300, 500, 750, 1000]
for beamwidth_b in beamwidths:
    for number_of_users in user:
        name = 'users=' + str(number_of_users) + 'beamwidth_b=' + str(np.degrees(beamwidth_b))
        name_M0 = name + 'M=0s=1' + '.p'
        name_M100 = name + 'M=100s=1' + '.p'
        # name_M1002 = name + 'M=100s=2' + '.p'
        # name_M1003 = name + 'M=100s=3' + '.p'
        # name_M1003 = name + 'M=100s=10' + '.p'

        # disconnected_users_heuristic[beamwidth_b].append(pickle.load(open(
        #     str('Data/disconnected_users' 'beamwidth_heuristic' + name_M0), 'rb')))
        #
        # heuristic_beamwidth_capacity[beamwidth_b].append(pickle.load(open(
        #     str('Data/channel_capacity' + 'beamwidth_heuristic' + name_M0), 'rb')))
        #
        # heuristic_beamwidth_capacitylos[beamwidth_b].append(pickle.load(open(
        #     str('Data/channel_capacity_with_los' + 'beamwidth_heuristic' + name_M0), 'rb')))

        capacity[beamwidth_b].append(pickle.load(open(
            str('Data/channel_capacity' + name_M100), 'rb')))

        # capacity2[beamwidth_b].append(pickle.load(open(
        #     str('Data/channel_capacity' + name_M1002), 'rb')))
        #
        # capacity3[beamwidth_b].append(pickle.load(open(
        #     str('Data/channel_capacity' + name_M1003), 'rb')))

        capacitylos[beamwidth_b].append(pickle.load(open(
            str('Data/channel_capacity_with_los' + name_M100), 'rb')))

        disconnected_users[beamwidth_b].append(pickle.load(open(
            str('Data/disconnected_users' + name_M100), 'rb')))

        # capacity_nopenalty[beamwidth_b].append(pickle.load(open(
        #     str('Data/channel_capacity' + name_M0), 'rb')))
        #
        # capacitylos_nopenalty[beamwidth_b].append(pickle.load(open(
        #     str('Data/channel_capacity_with_los' + name_M0), 'rb')))
        #
        # disconnected_users_nopenalty[beamwidth_b].append(pickle.load(open(
        #     str('Data/disconnected_users' + name_M0), 'rb')))

        # for k in [1, 2, 3, 4, 5, 24]:
        #     MC_SNR_heuristic_capacity[beamwidth_b][k].append(pickle.load(
        #         open(str('Data/channel_capacity' + 'SNR_' + 'k=' + str(k) + name_M0), 'rb')))
        #
        #     # MC_closest_heuristic_capacity[beamwidth_b][k].append(pickle.load(
        #     #     open(str('Data/channel_capacity' + 'closest_' + 'k=' + str(k) + name_M0), 'rb')))
        #     #
        #     # MC_closest_disconnected[beamwidth_b][k].append(pickle.load(
        #     #     open(str('Data/disconnected_users' + 'closest_k=' + str(k) + name_M0), 'rb')))
        #
        #     MC_SNR_disconnected[beamwidth_b][k].append(pickle.load(
        #         open(str('Data/disconnected_users' + 'SNR_k=' + str(k) + name_M0), 'rb')))
        #
        #     # print(f'MC k={k},', average(MC_closest_disconnected[beamwidth_b][k][-1]))
        #     print(f'SNR k={k},', average(MC_SNR_disconnected[beamwidth_b][k][-1]))

for i, beamwidth_b in zip(range(3), beamwidths):
    fig, ax = plt.subplots()

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
    avg_capacity_nopenalty = [sum(capacity_nopenalty[beamwidth_b][i]) / max(1, len(capacity_nopenalty[beamwidth_b][i]))
                              for i in range(len(user))]
    # avg_capacity_all_SNR = [average(MC_SNR_heuristic_capacity[beamwidth_b][24][i]) for i in range(len(user))]

    bars = [2, 5, 8, 11, 14]
    plt.bar([i for i in bars], avg_capacity, label=name + ' optimal')
    plt.bar([i - 0.8 for i in bars], avg_capacity_nopenalty, label=name + ' optimal no penalty')
    plt.bar([i + 0.8 for i in bars], avg_beamwidth_capacity, label=name + ' beamwidth')
    # plt.bar([i + 0.8 for i in bars], avg_capacity_all_SNR,  label=name + ' all SNR')

    for j, bar in zip(range(len(user)), bars):
        ax.annotate("", xy=(bar + 0.7, avg_beamwidth_capacity[j]), xytext=(bar + 0.7, avg_capacity[j]),
                    arrowprops=dict(arrowstyle="->"))
        ax.annotate(f"${round((avg_capacity[j] - avg_beamwidth_capacity[j]) / avg_beamwidth_capacity[j] * 100, 2)}\\%$",
                    xy=(bar +0.8, avg_capacity[j] - (avg_capacity[j] - avg_beamwidth_capacity[j]) / 1.8), fontsize=8)

    plt.xlabel('Number of users')
    plt.ylabel('Total channel capacity (Gbit/s/Hz)')
    plt.xticks(bars, user)
    plt.legend(loc='lower right')
    plt.show()
#
# print(avg_capacity)

disconnected_heuristic = [
    [0.0 / 100 * 100, 0.4415116976604679 / 300 * 100, 8.752 / 500 * 100, 54.76761619190405 / 750 * 100,
     147.354 / 1000 * 100],
    [0.0174 / 100 * 100, 11.775644871025795 / 300 * 100, 84.387 / 500 * 100, 236.83958020989505 / 750 * 100,
     420.954 / 1000 * 100],
    [0.4718 / 100 * 100, 47.088182363527295 / 300 * 100, 164.986 / 500 * 100,
     359.3253373313343 / 750 * 100, 577.14 / 1000 * 100]]

disconnected = [[0, 0, 0, 0, 0],
                [0, 0, 0, 0, 136.012 / 1000 * 100],
                [0, 0, 0, 174.00149925037482 / 750 * 100, 424.0 / 1000 * 100]]

disconnected_nopenalty = [
    [0.0008 / 100 * 100, 0.4979004199160168 / 300 * 100, 9.267 / 500 * 100, 53.90554722638681 / 750 * 100,
     141.428 / 1000 * 100],
    [0.0314 / 100 * 100, 13.804439112177565 / 300 * 100, 80.867 / 500 * 100,
     225.2383808095952 / 750 * 100,
     408.098 / 1000 * 100],
    [0.286 / 100 * 100, 37.95380923815237 / 300 * 100, 149.319 / 500 * 100,
     340.73313343328334 / 750 * 100,
     556.264 / 1000 * 100]]
#
for i, beamwidth_b in zip(range(3), beamwidths):
    if beamwidth_b == np.radians(5):
        name = '$5\degree$'
    elif beamwidth_b == np.radians(10):
        name = '$10\degree$'
    elif beamwidth_b == np.radians(15):
        name = '$15\degree$'

    fig, ax = plt.subplots()
    bars = [2, 5, 8, 11, 14]
    plt.bar([i - 0.8 for i in bars], disconnected[i], label=name + ' optimal')
    plt.bar(bars, disconnected_nopenalty[i], label=name + ' no penalty')
    plt.bar([i + 0.8 for i in bars], disconnected_heuristic[i], label=name + ' beamwidth')

    # plt.plot(user, disconnected_heuristic[1], '--*', label='10$\degree$ beamwidth')
    # plt.plot(user, disconnected[1], '-o', label='10$\degree$')
    # plt.plot(user, disconnected_nopenalty[1], '-.o', label='10$\degree$ no penalty')
    #
    # plt.plot(user, disconnected_heuristic[2], '--*', label='15$\degree$ beamwidth')
    # plt.plot(user, disconnected[2], '-o', label='15$\degree$')
    # plt.plot(user, disconnected_nopenalty[2], '-.o', label='15$\degree$ no penalty')
    #
    plt.xlabel('Number of users')
    plt.ylabel('Average percentage of disconnected users')
    plt.xticks(bars, user)

    plt.legend()
    plt.show()

# print(average(MC_SNR_heuristic_capacity[beamwidth_b][1][0]))
# for beamwidth in beamwidths:
#     fig, ax = plt.subplots()
#     plt.plot(user, [average(heuristic_beamwidth_capacity[beamwidth][i]) for i in range(len(user))], '-o',
#              label='beamwidth')
#     plt.plot(user, [average(MC_SNR_heuristic_capacity[beamwidth][1][i]) for i in range(len(user))], '-*',
#              label='$SNR - k = 1$')
#     plt.plot(user, [average(MC_SNR_heuristic_capacity[beamwidth][2][i]) for i in range(len(user))], '-d',
#              label='$SNR - k = 2$')
#     plt.plot(user, [average(MC_SNR_heuristic_capacity[beamwidth][3][i]) for i in range(len(user))], '-+',
#              label='$SNR - k = 3$')
#     plt.plot(user, [average(MC_SNR_heuristic_capacity[beamwidth][4][i]) for i in range(len(user))], '-v',
#              label='$SNR - k = 4$')
#     plt.plot(user, [average(MC_SNR_heuristic_capacity[beamwidth][5][i]) for i in range(len(user))], '-1',
#              label='$SNR - k = 5$')

#     plt.legend()
#     plt.xlabel('Number of users')
#     plt.ylabel('Total channel capacity (Gbit/s/Hz)')
#     plt.show()


# fig, ax = plt.subplots()
# plt.plot(user, [average(heuristic_beamwidth_capacity[beamwidth][i]) for i in range(len(user))], '-o',
#          label='beamwidth')
# plt.plot(user, [average(MC_closest_heuristic_capacity[beamwidth][1][i]) for i in range(len(user))], '-*',
#          label='$Closest - k = 1$')
# plt.plot(user, [average(MC_closest_heuristic_capacity[beamwidth][2][i]) for i in range(len(user))], '-d',
#          label='$Closest - k = 2$')
# plt.plot(user, [average(MC_closest_heuristic_capacity[beamwidth][3][i]) for i in range(len(user))], '-+',
#          label='$Closest - k = 3$')
# plt.plot(user, [average(MC_closest_heuristic_capacity[beamwidth][4][i]) for i in range(len(user))], '-v',
#          label='$Closest - k = 4$')
# plt.plot(user, [average(MC_closest_heuristic_capacity[beamwidth][5][i]) for i in range(len(user))], '-1',
#          label='$Closest - k = 5$')
#
# plt.legend()
# plt.xlabel('Number of users')
# plt.ylabel('Total channel capacity (Gbit/s/Hz)')
# plt.show()
#
for i, beamwidth_b in zip(range(3), beamwidths):
    fig, ax = plt.subplots()

    if beamwidth_b == np.radians(5):
        name = '$5\degree$'
    elif beamwidth_b == np.radians(10):
        name = '$10\degree$'
    elif beamwidth_b == np.radians(15):
        name = '$15\degree$'

    avg_capacitylos = [sum(capacitylos[beamwidth_b][i]) / max(1, len(capacitylos[beamwidth_b][i])) for i in
                       range(len(user))]
    avg_beamwidth_capacitylos = [
        sum(heuristic_beamwidth_capacitylos[beamwidth_b][i]) / len(heuristic_beamwidth_capacitylos[beamwidth_b][i]) for
        i in range(len(user))]

    avg_capacity = [sum(capacity[beamwidth_b][i]) / max(1, len(capacity[beamwidth_b][i])) for i in range(len(user))]
    avg_beamwidth_capacity = [
        sum(heuristic_beamwidth_capacity[beamwidth_b][i]) / len(heuristic_beamwidth_capacity[beamwidth_b][i]) for
        i in range(len(user))]
    size = 8

    bars = [2, 4.5, 7, 9.5, 12]
    plt.bar([i - 0.4 for i in bars], avg_capacity, label=name + ' optimal')
    plt.bar([i - 0.4 for i in bars], avg_capacitylos, label=name + ' optimal - with los')
    for j, bar in zip(range(len(user)), bars):
        ax.annotate("", xy=(bar - 0.7, avg_capacitylos[j]), xytext=(bar - 0.7, avg_capacity[j]),
                    arrowprops=dict(arrowstyle="->"))
        ax.annotate(f"${round((avg_capacity[j] - avg_capacitylos[j]) / avg_capacity[j] * 100, 2)}\\%$",
                    xy=(bar - 0.6, avg_capacity[j] - (avg_capacity[j] - avg_capacitylos[j]) / 2), fontsize=size)
    plt.bar([i + 0.4 for i in bars], avg_beamwidth_capacity, label=name + ' beamwidth')
    plt.bar([i + 0.4 for i in bars], avg_beamwidth_capacitylos, label=name + ' beamwidth - with los')
    for j, bar in zip(range(len(user)), bars):
        ax.annotate("", xy=(bar + 0.6, avg_beamwidth_capacitylos[j]), xytext=(bar + 0.6, avg_beamwidth_capacity[j]),
                    arrowprops=dict(arrowstyle="->"))
        ax.annotate(
            f"${round((avg_beamwidth_capacity[j] - avg_beamwidth_capacitylos[j]) / avg_beamwidth_capacity[j] * 100, 2)}\\%$",
            xy=(bar + 0.7, avg_beamwidth_capacity[j] - (avg_beamwidth_capacity[j] - avg_beamwidth_capacitylos[j]) / 2),
            fontsize=size)

    # plt.plot(user, np.multiply(np.divide(np.subtract(avg_capacity, avg_capacitylos), avg_capacity), 100), '-o',
    #           label=name + ' optimal')
    # plt.plot(user, np.multiply(np.divide(np.subtract(avg_beamwidth_capacity, avg_beamwidth_capacitylos), avg_beamwidth_capacity), 100), '--*',
    #           label=name + ' beamwidth')
    plt.xlabel('Number of users')
    plt.ylabel('Percentage capacity loss')
    plt.xticks(bars, user)
    plt.ylim((10000, np.max(avg_capacity) * 1.2))
    plt.legend()
    plt.show()
