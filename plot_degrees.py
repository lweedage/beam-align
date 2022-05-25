import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from parameters import *
import seaborn as sns

users_per_beam = 1

data5 = []
data10 = []
data15 = []

# for number_of_users in users:
#     iteration_max = iterations[number_of_users]
#     name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(5) + 'M=' + str(
#         M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))
#     degrees5 = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
#     data5.append(degrees5)
#
#     name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
#         M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))
#     degrees10 = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
#     data10.append(degrees10)
#
#     name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(15) + 'M=' + str(
#         M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))
#     degrees15 = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
#     data15.append(degrees15)
#
#
# labels = [100, 250, 500, 750, 1000]
# pos = np.array([250, 750, 1250, 1750, 2250])
# fig, ax = plt.subplots()
# x = np.array(labels)
# width = 100
# bplot1 = plt.boxplot(data5, positions=pos - (width + 10),  patch_artist=True,  notch=True,labels = ['','','','',''], widths = width, showfliers = False)
# bplot2 = plt.boxplot(data10, positions=pos, patch_artist= True, labels = labels, notch=True, widths = width, showfliers = False)
# bplot3 = plt.boxplot(data15, positions=pos + (width + 10), patch_artist=True,  notch=True,labels = ['','','','',''],widths = width, showfliers = False)
#
# for i, bplot in zip(range(3),(bplot1, bplot2, bplot3)):
#     color = colors[i]
#     for patch in bplot['boxes']:
#         patch.set_facecolor(color)
# ax.legend([bplot1["boxes"][0], bplot2["boxes"][0], bplot3["boxes"][0]], ['$5\degree$', '$10\degree$', '$15\degree$' ], loc='upper right')
# plt.xlabel('Users per km$^2$')
# plt.ylabel('Number of connections per user')
# plt.savefig('boxplot.png')
# plt.show()

# data_optimal = []
# data_beamwidth = []
# data_snr = []
#
# users_per_beam = 2
#
# for number_of_users in users:
#     iteration_max = iterations[number_of_users]
#     name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
#         M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))
#     optimal = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
#     data_optimal.append(optimal)
#
#     name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
#         M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))
#     beamwidth = pickle.load(open(str('Data/total_links_per_userbeamwidth_heuristic' + name + '.p'), 'rb'))
#     data_beamwidth.append(beamwidth)
#
#     name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
#         M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))
#     snr = pickle.load(open(str('Data/total_links_per_userSNR_k=3' + name + '.p'), 'rb'))
#     data_snr.append(snr)
#
# labels = [100, 250, 500, 750, 1000]
# pos = np.array([250, 750, 1250, 1750, 2250])
# fig, ax = plt.subplots()
# x = np.array(labels)
# width = 100
# bplot1 = plt.boxplot(data_optimal, positions=pos - (width + 10), patch_artist=True, notch=True,
#                      labels=['', '', '', '', ''], widths=width, showfliers=False)
# bplot2 = plt.boxplot(data_beamwidth, positions=pos, patch_artist=True, labels=labels, notch=True, widths=width,
#                      showfliers=False)
# bplot3 = plt.boxplot(data_snr, positions=pos + (width + 10), patch_artist=True, notch=True, labels=['', '', '', '', ''],
#                      widths=width, showfliers=False)
#
# for i, bplot in zip(range(3), (bplot1, bplot2, bplot3)):
#     color = colors[i]
#     for patch in bplot['boxes']:
#         patch.set_facecolor(color)
# ax.legend([bplot1["boxes"][0], bplot2["boxes"][0], bplot3["boxes"][0]], ['Optimal', 'ʙᴇᴀᴍ-ᴀʟɪɢɴ', 'SNR-3'],
#           loc='upper right')
# plt.savefig('boxplot_degrees.png')
# plt.show()

data_optimal = []
data_beamwidth = []
data_snr1 = []
data_snr3 = []

users_per_beam = 2

for number_of_users in users:
    iteration_max = iterations[number_of_users]
    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
        M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))
    optimal = pickle.load(open(str('Data/capacity_per_user' + name + '.p'), 'rb'))
    lijst = []
    for i in range(len(optimal)):
        for x in range(len(optimal[i])):
            lijst.append(optimal[i][x])
    data_optimal.append(lijst)

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
        M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))
    beamwidth = pickle.load(open(str('Data/capacity_per_userbeamwidth_heuristic' + name + '.p'), 'rb'))
    lijst = []
    for i in range(len(beamwidth)):
        for x in range(len(beamwidth[i])):
            lijst.append(beamwidth[i][x])
    data_beamwidth.append(lijst)

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
        M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))
    snr1 = pickle.load(open(str('Data/capacity_per_userSNR_k=1' + name + '.p'), 'rb'))
    lijst = []
    for i in range(len(snr1)):
        for x in range(len(snr1[i])):
            lijst.append(snr1[i][x])
    data_snr1.append(lijst)

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
        M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))
    snr3 = pickle.load(open(str('Data/capacity_per_userSNR_k=3' + name + '.p'), 'rb'))
    lijst = []
    for i in range(len(snr3)):
        for x in range(len(snr3[i])):
            lijst.append(snr3[i][x])
    data_snr3.append(lijst)

# print(data_optimal[0])
# print(data_beamwidth[0])
# print(data_snr[0])

# labels = [100, 250, 500, 750, 1000]
# pos = np.array([250, 750, 1250, 1750, 2250])
# fig, ax = plt.subplots()
# x = np.array(labels)
# width = 100
# bplot1 = plt.boxplot(data_optimal, positions=pos - (width + 10), patch_artist=True, notch=True,
#                      labels=['', '', '', '', ''], widths=width, showfliers=False)
# bplot2 = plt.boxplot(data_beamwidth, positions=pos, patch_artist=True, labels=labels, notch=True, widths=width,
#                      showfliers=False)
# bplot3 = plt.boxplot(data_snr3, positions=pos + (width + 10), patch_artist=True, notch=True, labels=['', '', '', '', ''],
#                      widths=width, showfliers=False)
#
# for i, bplot in zip(range(3), (bplot1, bplot2, bplot3)):
#     color = colors[i]
#     for patch in bplot['boxes']:
#         patch.set_facecolor(color)
# ax.legend([bplot1["boxes"][0], bplot2["boxes"][0], bplot3["boxes"][0]], ['Optimal', 'ʙᴇᴀᴍ-ᴀʟɪɢɴ', 'SNR-3'],
#           loc='upper right')
# plt.savefig('boxplot_capacities.png')
# plt.show()

cap_optimal = dict()
cap_beamwidth = dict()
cap_snr1 = dict()
cap_snr3 = dict()

for i,j in zip(users, range(5)):
    cap_optimal[i] = sum(data_optimal[j])/len(data_optimal[j])
    cap_beamwidth[i] = sum(data_beamwidth[j])/len(data_beamwidth[j])
    cap_snr1[i] = sum(data_snr1[j])/len(data_snr1[j])
    cap_snr3[i] = sum(data_snr3[j])/len(data_snr3[j])

print(cap_optimal)

name = str(str(beamwidth_deg) + str(M) + str(users_per_beam) + str(user_rate))
pickle.dump(cap_optimal, open(str('Data/Processed/cap' + name + '.p'), 'wb'), protocol=4)
name_beamwidth = str('beamwidth_heuristic' + name)
pickle.dump(cap_beamwidth, open(str('Data/Processed/cap' + name_beamwidth + '.p'), 'wb'), protocol=4)
name_snr1 = str('SNR_k=' + str(1) + name)
pickle.dump(cap_snr1, open(str('Data/Processed/cap' + name_snr1 + '.p'), 'wb'), protocol=4)
name_snr3 = str('SNR_k=' + str(3) + name)
pickle.dump(cap_snr1, open(str('Data/Processed/cap' + name_snr3 + '.p'), 'wb'), protocol=4)