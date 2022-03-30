import matplotlib.pyplot as plt
# from parameters import *
import numpy as np
import pickle
import seaborn as sns

colors =  ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed', 'grey'] * 100
# colors = sns.color_palette('Blues')

# deg = pickle.load(open(str('Data/Processed/deg' + str(beamwidth_deg) + str(M) + str(users_per_beam) + '.p'),'rb'))
# cap = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(users_per_beam) + '.p'),'rb'))
# mis = pickle.load(open(str('Data/Processed/mis' + str(beamwidth_deg) + str(M) + str(users_per_beam) + '.p'),'rb'))
# dis = pickle.load(open(str('Data/Processed/dis' + str(beamwidth_deg) + str(M) + str(users_per_beam) + '.p'),'rb'))
# cap_blocked = pickle.load(open(str('Data/Processed/cap_blocked' + str(beamwidth_deg) + str(M) + str(users_per_beam) + '.p'),'rb'))

users = [100, 300, 500, 750, 1000]

M = 100

users_per_beam = 10
#
# x1 = pickle.load(open(str('Data/Processed/cap' + str(10) + str(M) + str(2) + '.p'), 'rb')).values()
# x2 = pickle.load(open(str('Data/Processed/cap' + str(10) + str(M) + str(2) + '_SNRk=1.p'), 'rb')).values()
# x3 = pickle.load(open(str('Data/Processed/cap' + str(10) + str(M) + str(2) + '_SNRk=5.p'), 'rb')).values()
# x4 = pickle.load(open(str('Data/Processed/dis' + str(10) + str(M) + str(2) + '_greedy.p'), 'rb')).values()

x1 = pickle.load(open(str('Data/Processed/cap' + str(10) + str(M) + str(5) + '.p'), 'rb')).values()
x2 = pickle.load(open(str('Data/Processed/cap_blocked' + str(10) + str(M) + str(5) + '.p'), 'rb')).values()
# x3 = pickle.load(open(str('Data/Processed/fair' + str(15) + str(M) + str(5) + '.p'), 'rb')).values()
# x4 = pickle.load(open(str('Data/Processed/fair' + str(15) + str(M) + str(5) + '.p'), 'rb')).values()

# x1 = [sum(x)/len(x) for x in x1]
# x2 = [sum(x)/len(x) for x in x2]
# x3 = [sum(x)/len(x) for x in x3]
# x4 = [sum(x)/len(x) for x in x4]

# x1 = np.divide(list(x1), users) * 100
# x3 = np.divide(list(x3), users) * 100
# x4 = np.divide(list(x4), users) * 100

fig, ax = plt.subplots()
plt.plot(users, x1, '--', marker = '+', label = 'Optimal', color = colors[0])
plt.plot(users, x2, '--', marker = 'o', label = 'Optimal - blocked', color = colors[1])
# plt.plot(users, x3, '--', marker = 'o', label = '10 degrees', color = colors[2])
# plt.plot(users, x4, '--', marker = 'd', label = '15 degrees', color = colors[3])

plt.xlabel('Number of users')
# plt.ylabel('Percentage disconnected users')
plt.ylabel('Total capacity (MBps)')
plt.legend()

plt.show()
# for beamwidth_deg in [5, 10, 15]:
#     for users_per_beam in [1]:
#         x1 = pickle.load(
#             open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(users_per_beam) + '.p'), 'rb'))
#         # x2 = pickle.load(
#         #     open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(users_per_beam) + '_heuristic' + '.p'), 'rb'))
#         # x1a = pickle.load(
#         #     open(str('Data/Processed/cap' + str(beamwidth_deg) + str(0) + str(users_per_beam) + '.p'), 'rb'))
#         # x2s = pickle.load(
#         #     open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(users_per_beam) + '_SNRk=5.p'), 'rb'))
#
#
#         x1b = pickle.load(
#             open(str('Data/Processed/cap_blocked' + str(beamwidth_deg) + str(M) + str(users_per_beam) + '.p'), 'rb'))
#         # x2b = pickle.load(
#         #     open(str('Data/Processed/cap_blocked' + str(beamwidth_deg) + str(M) + str(users_per_beam) + '_heuristic' + '.p'), 'rb'))
#
#
#
#         x1 = list(x1.values())
#         # x1a = list(x1a.values())
#         # x2 = list(x2.values())
#         # x2s = list(x2s.values())
#
#         x1b = list(x1b.values())
#         # x2b = list(x2b.values())
#
#         fig, ax = plt.subplots()
#
#         bars = [3, 6, 9, 12, 15]
#         # plt.bar([i - 0.8 for i in bars], x1a, label='Optimal - no penalty', color = colors[1])
#         # plt.bar([i  for i in bars], x1, label='Optimal', color = colors[2])
#         # plt.bar([i + 0.8 for i in bars], x2, label='Heuristic', color = colors[4])
#         #
#         plt.bar([i - 0.4 for i in bars], x1, label='Optimal', color = colors[2])
#         plt.bar([i + 0.4 for i in bars], x1b, label='Optimal - blocked', color = colors[4])
#
#         # plt.bar([i - 0.8 for i in bars], x2s, label='SNR Heuristic, k = 5', color = colors[1])
#         # plt.bar([i  for i in bars], x1, label='Optimal', color = colors[2])
#         # plt.bar([i + 0.8 for i in bars], x2, label='Heuristic', color = colors[4])
#
#         # for j in range(5):
#         #     print((x1[j] - x2[j]) / x2[j] * 100)
#         # for j, bar in zip(range(5), bars):
#         #     ax.annotate("", xy=(bar + 0.2, x1[j]), xytext=(bar + 0.2, x2[j]),
#         #                 arrowprops=dict(arrowstyle="->"))
#         #     ax.annotate(
#         #         f"${round((x1[j] - x2[j]) / x2[j] * 100, 2)}\\%$",
#         #         xy=(bar + 0.3, x1[j] - (x1[j] - x2[j]) / 1.8), fontsize=8)
#
#
#         plt.xticks(bars, users)
#         # plt.ylim([9500, max(x1a) * 1.1])
#         plt.xlabel('Number of users')
#         plt.ylabel('Total channel capacity (Gbps)')
#         plt.legend()
#         plt.title(f's = {users_per_beam}, beamwidth = {beamwidth_deg}')
#         # plt.savefig('channel_capacity.png', dpi = 300)
#         plt.show()
#
#
#         #
#         x1 = pickle.load(open(str('Data/Processed/dis' + str(beamwidth_deg) + str(M) + str(users_per_beam) + '.p'), 'rb'))
#         # x1a = pickle.load(
#         #     open(str('Data/Processed/dis' + str(beamwidth_deg) + str(0) + str(users_per_beam) + '.p'), 'rb'))
#         # x2 = pickle.load(
#         #     open(str('Data/Processed/dis' + str(beamwidth_deg) + str(M) + str(users_per_beam) + '_heuristic' + '.p'), 'rb'))
#
#         x1b = pickle.load(open(str('Data/Processed/dis_blocked' + str(beamwidth_deg) + str(M) + str(users_per_beam) + '.p'), 'rb'))
#         # x2b = pickle.load(
#         #     open(str('Data/Processed/dis_blocked' + str(beamwidth_deg) + str(M) + str(users_per_beam) + '_heuristic' + '.p'), 'rb'))
#         # x2s = pickle.load(
#         #     open(str('Data/Processed/dis' + str(beamwidth_deg) + str(M) + str(users_per_beam) + '_SNRk=5.p'), 'rb'))
#
#         # plt.plot(users, np.multiply(np.divide(list(x1a.values()), users), 100), '--', marker = '*',  label = 'Optimal - no penalty', color = colors[1])
#         plt.plot(users, np.multiply(np.divide(list(x1.values()), users), 100), '--', marker = 'o', label = 'Optimal', color = colors[2])
#         # plt.plot(users, np.multiply(np.divide(list(x2.values()), users), 100), '--', marker = 'd',  label = 'Heuristic', color = colors[4])
#         # plt.plot(users, np.multiply(np.divide(list(x2s.values()), users), 100), '--', marker = 'd',  label = 'SNR Heuristic', color = colors[4])
#         plt.plot(users, np.multiply(np.divide(list(x1b.values()), users), 100), '--', marker = 'd',  label = 'Optimal blocked', color = colors[4])
#
#
#         plt.xlabel('Number of users')
#         plt.ylabel('% disconnected users')
#         plt.legend()
#         plt.title(f's = {users_per_beam}, beamwidth = {beamwidth_deg}')
#
#         # plt.savefig('disconnected_users.png', dpi = 300)
#         plt.show()
#
#
