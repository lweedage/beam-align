import matplotlib.pyplot as plt
# from parameters import *
import numpy as np
import pickle
import seaborn as sns

colors = ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed', 'grey'] * 100
# colors = sns.color_palette('Blues')
markers = ['o', 's' , 'v' , '*', 'p', 'P', '1', '+']

iterations = {50: 1, 100: 1000, 300: 334, 500: 200, 750: 133, 1000: 100}
users = [100, 300, 500, 750, 1000]
M = 100
users_per_beam = 10
beamwidth_deg = 10
s = 10

#
x1 = pickle.load(open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(1) + '.p'), 'rb')).values()
x2 = pickle.load(open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(2) + '.p'), 'rb')).values()
x3 = pickle.load(open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(5) + '.p'), 'rb')).values()
x4 = pickle.load(open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(10) + '.p'), 'rb')).values()
x5 = pickle.load(open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(1000) + '.p'), 'rb')).values()

# x1 = pickle.load(open(str('Data/Processed/fair' + str(5) + str(M) + str(s) + '.p'), 'rb')).values()
# x2 = pickle.load(open(str('Data/Processed/fair' + str(10) + str(M) + str(s) + '.p'), 'rb')).values()
# x3 = pickle.load(open(str('Data/Processed/fair' + str(15) + str(M) + str(s) + '.p'), 'rb')).values()

# x1 = pickle.load(open(str('Data/Processed/cap' + str(10) + str(M) + str(5) + '.p'), 'rb')).values()
# x2 = pickle.load(open(str('Data/Processed/cap_blocked' + str(10) + str(M) + str(5) + '.p'), 'rb')).values()
# x3 = pickle.load(open(str('Data/Processed/fair' + str(15) + str(M) + str(5) + '.p'), 'rb')).values()
# x4 = pickle.load(open(str('Data/Processed/fair' + str(15) + str(M) + str(5) + '.p'), 'rb')).values()

x1 = [sum(x)/len(x) for x in x1]
x2 = [sum(x)/len(x) for x in x2]
x3 = [sum(x)/len(x) for x in x3]
x4 = [sum(x)/len(x) for x in x4]
x5 = [sum(x)/len(x) for x in x5]

# x1 = np.divide(list(x1), users) * 100
# x2 = np.divide(list(x2), users) * 100
# x3 = np.divide(list(x3), users) * 100
# x4 = np.divide(list(x4), users) * 100
# x5 = np.divide(list(x5), users) * 100

# fig, ax = plt.subplots()
# plt.plot(users, x1, '--', marker=markers[0], label='$s=1$', color=colors[0])
# plt.plot(users, x2, '--', marker=markers[1], label='$s=2$', color=colors[1])
# plt.plot(users, x3, '--', marker=markers[2], label='$s=5$', color=colors[2])
# plt.plot(users, x4, '--', marker=markers[3], label='$s=10$', color=colors[3])
# plt.plot(users, x5, '--', marker=markers[4], label='$s=\infty$', color=colors[4])
#
# # plt.plot(users, x1, '--', marker=markers[0], label='$\\theta^b = 5\\degree$', color=colors[0])
# # plt.plot(users, x2, '--', marker=markers[1], label='$\\theta^b = 10\\degree$', color=colors[1])
# # plt.plot(users, x3, '--', marker=markers[2], label='$\\theta^b = 15\\degree$', color=colors[2])
#
# plt.xlabel('Number of users')
# plt.ylabel('Percentage disconnected users')
# # plt.ylabel('Total capacity (Mbps)')
# plt.ylabel('Jain\'s fairness index')
# plt.legend()
#
# plt.show()


# def fairness(x):
#     teller = sum(x)**2
#     noemer = len(x) * sum([i**2 for i in x])
#     return teller/noemer
#
# fair = []
# for s in range(1, 10):
#     x = pickle.load(open(str(f'Data/channel_capacity_per_user100users=1000beamwidth_b=10.0M=100s={s}.p'), 'rb'))
#     f = fairness(x)
#     print(f)
#
#     fair.append(sum(f)/len(f))
#
# plt.plot(range(1,10), fair)
# plt.ylabel('Jain\'s fairness index')
# plt.xlabel('Number of users per beam')
# plt.show()

y = {5: [], 10: [], 15: []}
x = [1, 2, 5, 10, 20]

# for beamwidth_deg in [15]: #[5, 10, 15]:
#     for s in [10]: #[1, 2, 5, 10, 1000]:
#         data = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(s) + '.p'), 'rb')).values()
#         # data = [sum(x) / len(x) for x in data]
#         y[beamwidth_deg].append(list(data)[-1])
#         # y[beamwidth_deg].append(data[-1])
#
# print(data, y)
# #
# fig, ax = plt.subplots()
# plt.plot(x, y[5], '--', marker='d', label='$\\theta^b = 5\\degree$', color=colors[0])
# plt.plot(x, y[10], '--', marker='d', label='$\\theta^b = 10\\degree$', color=colors[1])
# plt.plot(x, y[15], '--', marker='d', label='$\\theta^b = 15\\degree$', color=colors[2])
# plt.legend()
# plt.show()

# boxplot_data = []
# available_connections = []
#
# beamwidth_deg = 10
# M = 100
# s = 1
#
# for number_of_users in [100, 300, 500, 750, 1000]:
#     iteration_max = iterations[number_of_users]
#     name = str(f'Data/total_links_per_user{iteration_max}users={number_of_users}beamwidth_b=10.0M={M}s={s}.p')
#     degrees = pickle.load(open(name, 'rb'))
#     boxplot_data.append(degrees)
#     available_connections.append(sum(degrees)/(iteration_max * 24*s*(360/beamwidth_deg)) * 100)
#
# #todo something strange happens for s = 1, beamwidthdeg = 15, more beams in use than there are...
#
# print(available_connections)
# fig, ax = plt.subplots()
# bplot = ax.boxplot(boxplot_data, showfliers = False,
#                      vert=True,  # vertical box alignment
#                      patch_artist=True,  # fill with color
#                      labels=users)  # will be used to label x-ticks
# for patch, color in zip(bplot['boxes'], colors):
#     patch.set_facecolor(color)
# plt.xlabel('Number of users')
# plt.ylabel('Number of connections')
# plt.show()

# ---------------------------------------- HEURISTICS ------------------------------------------------

beamwidth_deg = 5
s = 10

x = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(s) + '.p'), 'rb')).values()
xh = pickle.load(open(str('Data/Processed/capbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + '.p'), 'rb')).values()
xg = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(s) + 'GreedyHeuristic.p'), 'rb')).values()
xgr = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(s) + 'GreedyRate.p'), 'rb')).values()
xs1 = pickle.load(open(str('Data/Processed/capSNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + '.p'), 'rb')).values()
xs5 = pickle.load(open(str('Data/Processed/capSNR_k=5' + str(beamwidth_deg) + str(M) + str(s) + '.p'), 'rb')).values()


print(xs1)
print(xs5)

fig, ax = plt.subplots()
plt.plot(users, x, '--', marker=markers[0], label='Optimal', color=colors[0])
plt.plot(users, xh, '--', marker=markers[1], label='Beamwidth', color=colors[1])
plt.plot(users, xg, '--', marker=markers[2], label='Greedy', color=colors[2])
plt.plot(users, xgr, '--', marker=markers[3], label='Greedy rate', color=colors[3])
plt.plot(users, xs1, '--', marker=markers[4], label='SNR k = 1', color=colors[4])
plt.plot(users, xs5, '--', marker=markers[5], label='SNR k = 5', color=colors[5])

plt.xlabel('Number of users')
# plt.ylabel('Percentage disconnected users')
plt.ylabel('Total capacity (Mbps)')
# plt.ylabel('Jain\'s fairness index')
plt.legend()

plt.show()

x = pickle.load(open(str('Data/Processed/dis' + str(beamwidth_deg) + str(M) + str(s) + '.p'), 'rb')).values()
xh = pickle.load(open(str('Data/Processed/disbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + '.p'), 'rb')).values()
xg = pickle.load(open(str('Data/Processed/dis' + str(beamwidth_deg) + str(M) + str(s) + 'GreedyHeuristic.p'), 'rb')).values()
xgr = pickle.load(open(str('Data/Processed/dis' + str(beamwidth_deg) + str(M) + str(s) + 'GreedyRate.p'), 'rb')).values()
xs1 = pickle.load(open(str('Data/Processed/disSNR_k=1'  + str(beamwidth_deg) + str(M) + str(s) + '.p'), 'rb')).values()
xs5 = pickle.load(open(str('Data/Processed/disSNR_k=5'  + str(beamwidth_deg) + str(M) + str(s) + '.p'), 'rb')).values()

# x1 = [sum(x)/len(x) for x in x1]

x = np.divide(list(x), users) * 100
xh = np.divide(list(xh), users) * 100
xg = np.divide(list(xg), users) * 100
xgr = np.divide(list(xgr), users) * 100
xs1 = np.divide(list(xs1), users) * 100
xs5 = np.divide(list(xs5), users) * 100

fig, ax = plt.subplots()
plt.plot(users, x, '--', marker=markers[0], label='Optimal', color=colors[0])
plt.plot(users, xh, '--', marker=markers[1], label='Beamwidth', color=colors[1])
plt.plot(users, xg, '--', marker=markers[2], label='Greedy', color=colors[2])
plt.plot(users, xgr, '--', marker=markers[3], label='Greedy rate', color=colors[3])
plt.plot(users, xs1, '--', marker=markers[4], label='SNR k = 1', color=colors[4])
plt.plot(users, xs5, '--', marker=markers[5], label='SNR k = 5', color=colors[5])
plt.xlabel('Number of users')
plt.ylabel('Percentage disconnected users')
# plt.ylabel('Total capacity (Mbps)')
# plt.ylabel('Jain\'s fairness index')
plt.legend()

plt.show()

x = pickle.load(open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(s) + '.p'), 'rb')).values()
xh = pickle.load(open(str('Data/Processed/fairbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + '.p'), 'rb')).values()
xg = pickle.load(open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(s) + 'GreedyHeuristic.p'), 'rb')).values()
xgr = pickle.load(open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(s) + 'GreedyRate.p'), 'rb')).values()
xs1 = pickle.load(open(str('Data/Processed/fairSNR_k=1'  + str(beamwidth_deg) + str(M) + str(s) + '.p'), 'rb')).values()
xs5 = pickle.load(open(str('Data/Processed/fairSNR_k=5'  + str(beamwidth_deg) + str(M) + str(s) + '.p'), 'rb')).values()

x = [sum(x)/len(x) for x in x]
xh = [sum(x)/len(x) for x in xh]
xg = [sum(x)/len(x) for x in xg]
xgr = [sum(x)/len(x) for x in xgr]
xs1 = [sum(x)/len(x) for x in xs1]
xs5 = [sum(x)/len(x) for x in xs5]

print(xh)

fig, ax = plt.subplots()
plt.plot(users, x, '--', marker=markers[0], label='Optimal', color=colors[0])
plt.plot(users, xh, '--', marker=markers[1], label='Beamwidth', color=colors[1])
plt.plot(users, xg, '--', marker=markers[2], label='Greedy', color=colors[2])
plt.plot(users, xgr, '--', marker=markers[3], label='Greedy rate', color=colors[3])
plt.plot(users, xs1, '--', marker=markers[4], label='SNR k = 1', color=colors[4])
plt.plot(users, xs5, '--', marker=markers[5], label='SNR k = 5', color=colors[5])
plt.xlabel('Number of users')
# plt.ylabel('Percentage disconnected users')
# plt.ylabel('Total capacity (Mbps)')
plt.ylabel('Jain\'s fairness index')
plt.legend()

plt.show()