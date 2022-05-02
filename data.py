import matplotlib.pyplot as plt
# from parameters import *
import numpy as np
import pickle
import seaborn as sns
import math

colors = ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed', 'grey'] * 100
markers = ['o', 's' , 'v' , '*', 'p', 'P', '1', '+']

iterations = {120: 10, 300: 10, 600: 10, 900: 10, 1200: 10}
users = [120, 300, 600, 900, 1200]
user_density = [100, 250, 500, 750, 1000]

radius = 200  # for triangular grid

xmin, xmax = 0, 800
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

xDelta = xmax - xmin
yDelta = ymax - ymin


M = 10000

# ---------------------------------------- HEURISTICS ------------------------------------------------
user_rate = 500
beamwidth_deg = 10
s = 1


x = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xh = pickle.load(open(str('Data/Processed/capbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xgr = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + 'GreedyRate.p'), 'rb')).values()
xs1 = pickle.load(open(str('Data/Processed/capSNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xs5 = pickle.load(open(str('Data/Processed/capSNR_k=5' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()

x = [i/j for i, j in zip(x, users)]
xh = [i/j for i, j in zip(xh, users)]
xgr = [i/j for i, j in zip(xh, users)]
xs1 = [i/j for i, j in zip(xs1, users)]
xs5 = [i/j for i, j in zip(xs5, users)]

fig, ax = plt.subplots()
plt.plot(user_density, x, '--', marker=markers[0], label='Optimal', color=colors[0])
plt.plot(user_density, xh, '--', marker=markers[1], label='Beamwidth', color=colors[1])
plt.plot(user_density, xgr, '--', marker=markers[2], label='Greedy', color=colors[2])
plt.plot(user_density, xs1, '--', marker=markers[3], label='SNR $k \leq 1$', color=colors[3])
plt.plot(user_density, xs5, '--', marker=markers[4], label='SNR $k \leq 5$', color=colors[4])
print(xgr)
plt.xlabel('User density')
plt.ylabel('Per-user capacity (Mbps)')
plt.legend()
plt.savefig(f'Figures/capacity{beamwidth_deg}{s}{user_rate}')
plt.show()


print('Difference with heuristic:', [(i-j)/i * 100 for i, j in zip(x,xh)], sum([(i-j)/i * 100 for i, j in zip(x,xh)])/5)
print('Difference with SNR k 5:', [(i-j)/i * 100 for i, j in zip(x,xs5)], sum([(i-j)/i * 100 for i, j in zip(x,xs5)])/5)

print(xh)

x = pickle.load(open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xh = pickle.load(open(str('Data/Processed/satbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xgr = pickle.load(open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + 'GreedyRate.p'), 'rb')).values()
xs1 = pickle.load(open(str('Data/Processed/satSNR_k=1'  + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xs5 = pickle.load(open(str('Data/Processed/satSNR_k=5'  + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()


fig, ax = plt.subplots()
plt.plot(users, x, '--', marker=markers[0], label='Optimal', color=colors[0])
plt.plot(users, xh, '--', marker=markers[1], label='Beamwidth', color=colors[1])
plt.plot(users, xgr, '--', marker=markers[2], label='Greedy', color=colors[2])
plt.plot(users, xs1, '--', marker=markers[3], label='SNR $k \leq 1$', color=colors[3])
plt.plot(users, xs5, '--', marker=markers[4], label='SNR $k \leq 5$', color=colors[4])

plt.xlabel('Number of users')
plt.ylabel('Average satisfaction (per user)')
plt.legend()
plt.savefig(f'Figures/satisfaction{beamwidth_deg}{s}{user_rate}')

plt.show()

x = pickle.load(open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xh = pickle.load(open(str('Data/Processed/fairbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xgr = pickle.load(open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + 'GreedyRate.p'), 'rb')).values()
xs1 = pickle.load(open(str('Data/Processed/fairSNR_k=1'  + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xs5 = pickle.load(open(str('Data/Processed/fairSNR_k=5'  + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()

x = [sum(x)/len(x) for x in x]
xh = [sum(x)/len(x) for x in xh]
xgr = [sum(x)/len(x) for x in xgr]
xs1 = [sum(x)/len(x) for x in xs1]
xs5 = [sum(x)/len(x) for x in xs5]

#
# fig, ax = plt.subplots()
# plt.plot(users, x, '--', marker=markers[0], label='Optimal', color=colors[0])
# plt.plot(users, xh, '--', marker=markers[1], label='Beamwidth', color=colors[1])
# # plt.plot(users, xhi, '--', marker=markers[2], label='Beamwidth - iterative', color=colors[2])
# # plt.plot(users, xg, '--', marker=markers[2], label='Greedy', color=colors[2])
# # plt.plot(users, xgr, '--', marker=markers[3], label='Greedy rate', color=colors[3])
# # plt.plot(users, xs1, '--', marker=markers[4], label='SNR $k \leq 1$', color=colors[4])
# plt.plot(users, xs5, '--', marker=markers[5], label='SNR $k \leq 5$', color=colors[5])
# plt.xlabel('Number of users')
# plt.ylabel('Jain\'s fairness index')
# plt.legend()
# plt.savefig(f'Figures/fairness{beamwidth_deg}{s}{user_rate}')
# plt.show()

x = pickle.load(open(str('Data/Processed/cap_blocked' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xh = pickle.load(open(str('Data/Processed/cap_blockedbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xgr = pickle.load(open(str('Data/Processed/cap_blocked' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + 'GreedyRate.p'), 'rb')).values()
xs1 = pickle.load(open(str('Data/Processed/cap_blockedSNR_k=1'  + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xs5 = pickle.load(open(str('Data/Processed/cap_blockedSNR_k=5'  + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()

ox = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
oxh = pickle.load(open(str('Data/Processed/capbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
oxgr = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + 'GreedyRate.p'), 'rb')).values()
oxs1 = pickle.load(open(str('Data/Processed/capSNR_k=1'  + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
oxs5 = pickle.load(open(str('Data/Processed/capSNR_k=5'  + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()


x = [i/j for i, j in zip(x, users)]
xh = [i/j for i, j in zip(xh, users)]
xgr = [i/j for i, j in zip(xh, users)]
xs1 = [i/j for i, j in zip(xs1, users)]
xs5 = [i/j for i, j in zip(xs5, users)]

ox = [i/j for i, j in zip(ox, users)]
oxh = [i/j for i, j in zip(oxh, users)]
oxgr = [i/j for i, j in zip(oxs1, users)]
oxs1 = [i/j for i, j in zip(oxs1, users)]
oxs5 = [i/j for i, j in zip(oxs5, users)]

fig, ax = plt.subplots()
plt.plot(users, x, '--', marker=markers[0], label='Optimal', color=colors[0])
plt.plot(users, xh, '--', marker=markers[1], label='Beamwidth', color=colors[1])
plt.plot(users, xgr, '--', marker=markers[2], label='Greedy', color=colors[2])
plt.plot(users, xs1, '--', marker=markers[3], label='SNR $k \leq 1$', color=colors[3])
plt.plot(users, xs5, '--', marker=markers[4], label='SNR $k \leq 5$', color=colors[4])

# plt.plot(users, ox, '-', marker=markers[0], label='Optimal', color=colors[0])
# plt.plot(users, oxh, '-', marker=markers[1], label='Beamwidth', color=colors[1])
# # plt.plot(users, oxgr, '-', marker=markers[3], label='Greedy rate', color=colors[3])
# # plt.plot(users, oxs1, '-', marker=markers[2], label='SNR $k \leq 1$', color=colors[2])
# plt.plot(users, oxs5, '-', marker=markers[3], label='SNR $k \leq 5$', color=colors[3])

plt.xlabel('Number of users')
plt.ylabel('Per-user capacity (Mbps)')
plt.legend()
plt.savefig(f'Figures/capacity_blocked{beamwidth_deg}{s}{user_rate}')
plt.show()

x = pickle.load(open(str('Data/Processed/sat_blocked' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xh = pickle.load(open(str('Data/Processed/sat_blockedbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xgr = pickle.load(open(str('Data/Processed/sat_blocked' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + 'GreedyRate.p'), 'rb')).values()
xs1 = pickle.load(open(str('Data/Processed/sat_blockedSNR_k=1'  + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xs5 = pickle.load(open(str('Data/Processed/sat_blockedSNR_k=5'  + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()

ox = pickle.load(open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
oxh = pickle.load(open(str('Data/Processed/satbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
oxgr = pickle.load(open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + 'GreedyRate.p'), 'rb')).values()
oxs1 = pickle.load(open(str('Data/Processed/satSNR_k=1'  + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
oxs5 = pickle.load(open(str('Data/Processed/satSNR_k=5'  + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()

print(x)
x = [i/j for i, j in zip(x, users)]
xh = [i/j for i, j in zip(xh, users)]
xgr = [i/j for i, j in zip(xh, users)]
xs1 = [i/j for i, j in zip(xs1, users)]
xs5 = [i/j for i, j in zip(xs5, users)]

ox = [i/j for i, j in zip(ox, users)]
oxh = [i/j for i, j in zip(oxh, users)]
oxgr = [i/j for i, j in zip(oxs1, users)]
oxs1 = [i/j for i, j in zip(oxs1, users)]
oxs5 = [i/j for i, j in zip(oxs5, users)]

fig, ax = plt.subplots()
plt.plot(users, x, '--', marker=markers[0], label='Optimal', color=colors[0])
plt.plot(users, xh, '--', marker=markers[1], label='Beamwidth', color=colors[1])
plt.plot(users, xgr, '--', marker=markers[2], label='Greedy', color=colors[2])
plt.plot(users, xs1, '--', marker=markers[3], label='SNR $k \leq 1$', color=colors[3])
plt.plot(users, xs5, '--', marker=markers[4], label='SNR $k \leq 5$', color=colors[4])

# plt.plot(users, ox, '-', marker=markers[0], label='Optimal', color=colors[0])
# plt.plot(users, oxh, '-', marker=markers[1], label='Beamwidth', color=colors[1])
# # plt.plot(users, oxgr, '-', marker=markers[3], label='Greedy rate', color=colors[3])
# # plt.plot(users, oxs1, '-', marker=markers[2], label='SNR $k \leq 1$', color=colors[2])
# plt.plot(users, oxs5, '-', marker=markers[3], label='SNR $k \leq 5$', color=colors[3])

plt.xlabel('Number of users')
plt.ylabel('Average satisfaction (per user)')
plt.legend()
plt.savefig(f'Figures/satisfaction_blocked{beamwidth_deg}{s}{user_rate}')
plt.show()


x = pickle.load(open(str('Data/Processed/sat_blocked' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xh = pickle.load(open(str('Data/Processed/sat_blockedbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xgr = pickle.load(open(str('Data/Processed/sat_blocked' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + 'GreedyRate.p'), 'rb')).values()
xs1 = pickle.load(open(str('Data/Processed/sat_blockedSNR_k=1'  + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xs5 = pickle.load(open(str('Data/Processed/sat_blockedSNR_k=5'  + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()

x = [i/j for i, j in zip(x, users)]
xh = [i/j for i, j in zip(xh, users)]
xgr = [i/j for i, j in zip(xh, users)]
xs1 = [i/j for i, j in zip(xs1, users)]
xs5 = [i/j for i, j in zip(xs5, users)]

fig, ax = plt.subplots()
plt.plot(users, x, '--', marker=markers[0], label='Optimal', color=colors[0])
plt.plot(users, xh, '--', marker=markers[1], label='Beamwidth', color=colors[1])
plt.plot(users, xgr, '--', marker=markers[2], label='Greedy', color=colors[2])
plt.plot(users, xs1, '--', marker=markers[3], label='SNR $k \leq 1$', color=colors[3])
plt.plot(users, xs5, '--', marker=markers[4], label='SNR $k \leq 5$', color=colors[4])

plt.xlabel('Number of users')
plt.ylabel('Average satisfaction (per user)')
plt.legend()
plt.savefig(f'Figures/satisfaction_blocked{beamwidth_deg}{s}{user_rate}')
plt.show()

# x = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '_clustered.p'), 'rb')).values()
# xh = pickle.load(open(str('Data/Processed/capbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '_clustered.p'), 'rb')).values()
# xgr = pickle.load(open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + 'GreedyRate.p'), 'rb')).values()
# xs1 = pickle.load(open(str('Data/Processed/capSNR_k=1'  + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '_clustered.p'), 'rb')).values()
# xs5 = pickle.load(open(str('Data/Processed/capSNR_k=5'  + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '_clustered.p'), 'rb')).values()
#
#
# fig, ax = plt.subplots()
# plt.plot(users[:-1], x, '--', marker=markers[0], label='Optimal', color=colors[0])
# plt.plot(users, xh, '--', marker=markers[1], label='Beamwidth', color=colors[1])
# plt.plot(users, xgr, '--', marker=markers[2], label='Greedy', color=colors[2])
# plt.plot(users, xs1, '--', marker=markers[3], label='SNR $k \leq 1$', color=colors[3])
# plt.plot(users, xs5, '--', marker=markers[4], label='SNR $k \leq 5$', color=colors[4])
#
# plt.xlabel('Number of users')
# plt.ylabel('Per-user capacity (Mbps)')
# plt.legend()
# plt.savefig(f'Figures/clustered_capacity{beamwidth_deg}{s}{user_rate}')
#
# plt.show()