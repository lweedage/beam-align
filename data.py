import matplotlib.pyplot as plt
# from parameters import *
import numpy as np
import pickle
import seaborn as sns
import math
import matplotlib.pylab as pylab

params = {'legend.fontsize': 'xx-large',
         'axes.labelsize': 'xx-large',
         'axes.titlesize':'xx-large',
         'xtick.labelsize':'xx-large',
         'ytick.labelsize':'xx-large',
        'lines.markersize': 8,
          'figure.autolayout': True}
pylab.rcParams.update(params)

colors = ['#904C77', '#E49AB0', '#ECB8A5',  '#96ACB7',  '#957D95'] * 100
markers = ['o', 'X', 'v' , 's', '*', 'P', '1', '+']

iterations = {120: 1000, 300: 400, 600: 200, 900: 134, 1200: 100}

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
s = 2

x = pickle.load(
    open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/capbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()
# xgr = pickle.load(
#     open(str('Data/Processed/capbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '_greedy.p'), 'rb')).values()
xs1 = pickle.load(open(str('Data/Processed/capSNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
                       'rb')).values()
xs3 = pickle.load(open(str('Data/Processed/capSNR_k=3' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
                       'rb')).values()
xs5 = pickle.load(open(str('Data/Processed/capSNR_k=24' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
                       'rb')).values()

fig, ax = plt.subplots()
plt.plot(user_density, x, '--', marker=markers[0], label='Optimal', color=colors[0], markersize = 8)
plt.plot(user_density, xh, '--', marker=markers[1], label='ʙᴇᴀᴍ-ᴀʟɪɢɴ', color=colors[1], markersize = 8)
# plt.plot(user_density, xgr, '--', marker=markers[5], label='Optimal $M=0$', color=colors[5])
# plt.plot(user_density, xs3, '--', marker=markers[3], label='SNR-3', color=colors[3], markersize = 8)
plt.plot(user_density, xs5, '--', marker=markers[2], label='SNR-dynamic', color=colors[2], markersize = 8)
plt.plot(user_density, xs1, '--', marker=markers[3], label='SNR-1', color=colors[3], markersize = 8)

plt.xlabel('Users per km$^2$')
plt.ylabel('Per-user capacity (Mbps)')
plt.legend()
plt.savefig(f'Figures/capacity{beamwidth_deg}{s}{user_rate}')
plt.show()

print('Normal scenario')
print('Difference with heuristic:', [(i - j) / i * 100 for i, j in zip(x, xh)],
      sum([(i - j) / i * 100 for i, j in zip(x, xh)]) / 5)
# print('Difference with heuristic:', [(i - j) / i * 100 for i, j in zip(x, xgr)],
#       sum([(i - j) / i * 100 for i, j in zip(x, xgr)]) / 5)
print('Difference with SNR k=1:', [(i - j) / i * 100 for i, j in zip(x, xs1)],
      sum([(i - j) / i * 100 for i, j in zip(x, xs1)]) / 5)
print('Difference with SNR dynamic:', [(i - j) / i * 100 for i, j in zip(x, xs5)],
      sum([(i - j) / i * 100 for i, j in zip(x, xs5)]) / 5)

x_normal = x

x = pickle.load(
    open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/satbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()
# xgr = pickle.load(
#     open(str('Data/Processed/satbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '_greedy.p'), 'rb')).values()
xs1 = pickle.load(open(str('Data/Processed/satSNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
                       'rb')).values()
xs5 = pickle.load(open(str('Data/Processed/satSNR_k=24' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
                       'rb')).values()

fig, ax = plt.subplots()
plt.plot(user_density, x, '--', marker=markers[0], label='Optimal', color=colors[0], markersize = 8)
plt.plot(user_density, xh, '--', marker=markers[1], label='ʙᴇᴀᴍ-ᴀʟɪɢɴ', color=colors[1], markersize = 8)
# plt.plot(user_density, xgr, '--', marker=markers[2], label='Optimal - $M = 0$', color=colors[5])
plt.plot(user_density, xs5, '--', marker=markers[2], label='SNR-dynamic', color=colors[2], markersize = 8)
plt.plot(user_density, xs1, '--', marker=markers[3], label='SNR-1', color=colors[3], markersize = 8)

plt.xlabel('Users per km$^2$')
plt.ylabel('Average satisfaction (per user)')
plt.legend()
plt.savefig(f'Figures/satisfaction{beamwidth_deg}{s}{user_rate}')

plt.show()

x = pickle.load(
    open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/fairbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()
# xgr = pickle.load(open(str('Data/Processed/fair' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + 'GreedyRate.p'), 'rb')).values()
xs1 = pickle.load(open(str('Data/Processed/fairSNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
                       'rb')).values()
xs5 = pickle.load(open(str('Data/Processed/fairSNR_k=3' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
                       'rb')).values()

# x = [sum(x)/len(x) for x in x]
# xh = [sum(x)/len(x) for x in xh]
# xgr = [sum(x)/len(x) for x in xgr]
# xs1 = [sum(x)/len(x) for x in xs1]
# xs5 = [sum(x)/len(x) for x in xs5]

#
# fig, ax = plt.subplots()
# plt.plot(users, x, '--', marker=markers[0], label='Optimal', color=colors[0])
# plt.plot(users, xh, '--', marker=markers[1], label='ʙᴇᴀᴍ-ᴀʟɪɢɴ', color=colors[1])
# # plt.plot(users, xg, '--', marker=markers[2], label='Greedy', color=colors[2])
# # plt.plot(users, xs1, '--', marker=markers[3], label='SNR-1', color=colors[4])
# plt.plot(users, xs5, '--', marker=markers[4], label='SNR-3', color=colors[5])
# plt.xlabel('Users per km$^2$')
# plt.ylabel('Jain\'s fairness index')
# plt.legend()
# plt.savefig(f'Figures/fairness{beamwidth_deg}{s}{user_rate}')
# plt.show()
