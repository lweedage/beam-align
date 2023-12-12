import math
# from parameters import *
import pickle

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt

params = {'legend.fontsize': 'xx-large',
          'axes.labelsize': 'xx-large',
          'axes.titlesize': 'xx-large',
          'xtick.labelsize': 'xx-large',
          'ytick.labelsize': 'xx-large',
          'lines.markersize': 8,
          'figure.autolayout': True}
pylab.rcParams.update(params)

colors = ['#904C77', '#E49AB0', '#ECB8A5', '#96ACB7', '#957D95'] * 100
markers = ['o', 'X', 'v', 's', '*', 'P', '1', '+']

iterations = {21: 477, 41: 244, 104: 97, 208: 48, 312: 32, 10: 200, 15: 134, 20: 100}

users = [21, 41, 104, 208, 312]
user_density = [50, 100, 250, 500, 750]

radius = 200  # for triangular grid

xmin, xmax = 0, 600
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 2

xDelta = xmax - xmin
yDelta = ymax - ymin

M = 750

# ---------------------------------------- HEURISTICS ------------------------------------------------
user_rate = 500
beamwidth_deg = 10

max_connections = 25

# for scenario in [1, 2, 3, 31, 32, 33]:
#     get_data.get_data(scenario, Heuristic=False, SNRHeuristic=False)
#     get_data.get_data(scenario, Heuristic=True, SNRHeuristic=False)
#     get_data.get_data(scenario, Heuristic=False, SNRHeuristic=True)

x = pickle.load(
    open(str('Data/Processed/capSINR' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'), 'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/capSINRbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'),
         'rb')).values()
xs1 = pickle.load(
    open(str('Data/Processed/capSINR' + str(beamwidth_deg) + str(M) + str(1) + '_SNRheuristic.p'),
         'rb')).values()
xs5 = pickle.load(
    open(str('Data/Processed/capSINR' + str(beamwidth_deg) + str(M) + str(25) + '_SNRheuristic.p'),
         'rb')).values()

fig, ax = plt.subplots()
plt.plot(user_density, x, '--', marker=markers[0], label='Optimal', color=colors[0], markersize=8)
plt.plot(user_density, xh, '--', marker=markers[1], label='ʙᴇᴀᴍ-ᴀʟɪɢɴ', color=colors[1], markersize=8)
plt.plot(user_density, xs5, '--', marker=markers[2], label='SNR-dynamic', color=colors[2], markersize=8)
plt.plot(user_density, xs1, '--', marker=markers[3], label='SNR-1', color=colors[3], markersize=8)

plt.xlabel('Users per km$^2$')
plt.ylabel('Per-user capacity (Mbps)')
plt.legend()
plt.savefig(f'Figures/capacity{beamwidth_deg}{max_connections}{user_rate}.png')
plt.show()

print('Normal scenario')
print('Difference with heuristic:', [(i - j) / i * 100 for i, j in zip(x, xh)],
      sum([(i - j) / i * 100 for i, j in zip(x, xh)]) / 5)

print('Difference with SNR k=1:', [(i - j) / i * 100 for i, j in zip(x, xs1)],
      sum([(i - j) / i * 100 for i, j in zip(x, xs1)]) / 5)
print('Difference with SNR dynamic:', [(i - j) / i * 100 for i, j in zip(x, xs5)],
      sum([(i - j) / i * 100 for i, j in zip(x, xs5)]) / 5)

x_normal = x

x = pickle.load(
    open(str('Data/Processed/satSINR' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'), 'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/satSINRbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'),
         'rb')).values()
# xgr = pickle.load(
#     open(str('Data/Processed/satbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '_greedy.p'), 'rb')).values()
xs1 = pickle.load(open(str('Data/Processed/satSINR' + str(beamwidth_deg) + str(M) + str(1) + '_SNRheuristic.p'),
                       'rb')).values()
xs5 = pickle.load(open(str('Data/Processed/satSINR' + str(beamwidth_deg) + str(M) + str(25) + '_SNRheuristic.p'),
                       'rb')).values()

fig, ax = plt.subplots()
plt.plot(user_density, x, '--', marker=markers[0], label='Optimal', color=colors[0], markersize=8)
plt.plot(user_density, xh, '--', marker=markers[1], label='ʙᴇᴀᴍ-ᴀʟɪɢɴ', color=colors[1], markersize=8)
# plt.plot(user_density, xgr, '--', marker=markers[2], label='Optimal - $M = 0$', color=colors[5])
plt.plot(user_density, xs5, '--', marker=markers[2], label='SNR-dynamic', color=colors[2], markersize=8)
plt.plot(user_density, xs1, '--', marker=markers[3], label='SNR-1', color=colors[3], markersize=8)

plt.xlabel('Users per km$^2$')
plt.ylabel('Average satisfaction (per user)')
plt.legend()
plt.xticks(([100, 250, 500, 750]))

plt.savefig(f'Figures/satisfaction{beamwidth_deg}{max_connections}{user_rate}.png')

plt.show()

# --------------------------------------------------------------------------------------------

users = [10, 15, 20]

radius = 200  # for triangular grid

xmin, xmax = 0, 400
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius

xDelta = xmax - xmin
yDelta = ymax - ymin

area = xDelta * yDelta / (1000 * 1000)

user_density = [i / area for i in users]

# for scenario in [1, 2, 3]:
#     get_data.get_data(scenario, Harris=True)
#     get_data.get_data(scenario, Heuristic=True)

xhho_cap = pickle.load(
    open(str('Data/Processed/capSINRHHO' + str(beamwidth_deg) + str(300) + str(max_connections) + '10.p'),
         'rb')).values()
xh_cap = pickle.load(
    open(str('Data/Processed/capSINRbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '10.p'),
         'rb')).values()

fig, ax = plt.subplots()
plt.bar([i - 1 for i in users], xh_cap, 2, label='ʙᴇᴀᴍ-ᴀʟɪɢɴ', color=colors[1])
plt.bar([i + 1 for i in users], xhho_cap, 2, label='MOHHO', color=colors[5])

plt.xlabel('Number of users')
plt.ylabel('Per-user capacity (Mbps)')
plt.legend()
plt.savefig(f'Figures/HHOcapacity{beamwidth_deg}{max_connections}{user_rate}.png')
plt.xticks([10, 15, 20])
plt.show()

xhho = pickle.load(
    open(str('Data/Processed/satSINRHHO' + str(beamwidth_deg) + str(300) + str(max_connections) + '10.p'),
         'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/satSINRbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '10.p'),
         'rb')).values()

fig, ax = plt.subplots()
plt.bar([i - 1 for i in users], xh, 2, label='ʙᴇᴀᴍ-ᴀʟɪɢɴ', color=colors[1])
plt.bar([i + 1 for i in users], xhho, 2, label='MOHHO', color=colors[5])

plt.xlabel('Number of users')
plt.ylabel('Average satisfaction (per user)')
plt.legend(loc='lower left')
plt.xticks(([10, 15, 20]))

plt.savefig(f'Figures/satisfaction{beamwidth_deg}{max_connections}{user_rate}HHO.png')

plt.show()

xhho = pickle.load(
    open(str('Data/Processed/energyHHO' + str(beamwidth_deg) + str(300) + str(max_connections) + '10.p'),
         'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/energybeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '10.p'),
         'rb')).values()

fig, ax = plt.subplots()
plt.bar([i - 1 for i in users], [(j * k) / i for i, j, k in zip(xh, xh_cap, users)], 2, label='ʙᴇᴀᴍ-ᴀʟɪɢɴ',
        color=colors[1])
plt.bar([i + 1 for i in users], [(j * k) / i for i, j, k in zip(xhho, xhho_cap, users)], 2, label='MOHHO',
        color=colors[5])

print([x/10 for x in xh], xh_cap)
print(xhho, xhho_cap)

plt.xlabel('Number of users')
plt.ylabel('Energy efficiency (Mbps/W)')
plt.legend(loc = 'lower right')
plt.xticks(([10, 15, 20]))

plt.savefig(f'Figures/EE{beamwidth_deg}{max_connections}{user_rate}')

plt.show()

xhhoU = pickle.load(
    open(str('Data/Processed/sigmaUHHO' + str(beamwidth_deg) + str(300) + str(max_connections) + '10.p'),
         'rb')).values()
xhU = pickle.load(
    open(str('Data/Processed/sigmaUbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '10.p'),
         'rb')).values()
xhho = pickle.load(
    open(str('Data/Processed/sigmaBSHHO' + str(beamwidth_deg) + str(300) + str(max_connections) + '10.p'),
         'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/sigmaBSbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '10.p'),
         'rb')).values()

fig, ax = plt.subplots()
plt.bar([i - 1.5 for i in users], xh, 1, label='ʙᴇᴀᴍ-ᴀʟɪɢɴ', color=colors[1])
plt.bar([i + 0.5 for i in users], xhU, 1, color=colors[1], hatch='//', edgecolor=colors[5])

plt.bar([i - 0.5 for i in users], xhho, 1, label='MOHHO', color=colors[5])
plt.bar([i + 1.5 for i in users], xhhoU, 1, color=colors[5], hatch='//', edgecolor=colors[1])

plt.xlabel('Number of users')
plt.ylabel('STD user rates/BS loads (Mbps)')
plt.legend()
plt.xticks(([10, 15, 20]))

plt.savefig(f'Figures/sigmaBS{beamwidth_deg}{max_connections}{user_rate}.png')

plt.show()
