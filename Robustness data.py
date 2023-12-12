import math
import pickle

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
# from parameters import *
import numpy as np

import get_data

params = {'legend.fontsize': 'x-large',
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large',
          'lines.markersize': 8,
          'figure.autolayout': True}
pylab.rcParams.update(params)

colors = ['#904C77', '#E49AB0', '#ECB8A5', '#96ACB7', '#957D95'] * 100
markers = ['o', 'X', 'v', 's', '*', 'P', '1', '+']

iterations = {21: 477, 41: 244, 104: 97, 208: 48, 312: 32, 10: 200, 15: 134, 20: 100}

users = [21, 41, 104, 208, 312]
user_density = [50, 100, 250, 500, 750]

# users = [208]

radius = 200  # for triangular grid

xmin, xmax = 0, 600
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 2

xDelta = xmax - xmin
yDelta = ymax - ymin

M = 750

beamwidth_deg = 10
user_rate = 500

index = 2

max_connections = 25

get_data.get_data(4, SNRHeuristic=True)
get_data.get_data(4)
get_data.get_data(4, Heuristic=True)

x = pickle.load(
    open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'), 'rb')).values()
x = [i / j for i, j in zip(x, users)]
x_normal = x

# ------------------------- BLOCKED -----------------------------------------
x = pickle.load(
    open(str('Data/Processed/capSINR' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'), 'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/capSINRbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'),
         'rb')).values()
xs5 = pickle.load(
    open(str('Data/Processed/capSINR' + str(beamwidth_deg) + str(M) + str(max_connections) + '_SNRheuristic.p'),
         'rb')).values()

xb = pickle.load(open(str('Data/Processed/cap_blocked' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'),
                      'rb')).values()
xhb = pickle.load(open(
    str('Data/Processed/cap_blockedbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'),
    'rb')).values()
xs5b = pickle.load(
    open(str('Data/Processed/cap_blocked' + str(beamwidth_deg) + str(M) + str(max_connections) + '_SNRheuristic.p'),
         'rb')).values()

xc = pickle.load(
    open(str('Data/Processed/capSINR' + str(beamwidth_deg) + str(M) + str(max_connections) + '_clustered.p'),
         'rb')).values()
xhc = pickle.load(open(
    str('Data/Processed/capSINRbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '_clustered.p'),
    'rb')).values()
xs5c = pickle.load(
    open(str('Data/Processed/capSINR' + str(beamwidth_deg) + str(M) + str(max_connections) + '_SNRheuristic_clustered.p'),
         'rb')).values()

opt = [i for i, j in zip(x, users)][index]
beam = [i for i, j in zip(xh, users)][index]
snr_opt = [i for i, j in zip(xs5, users)][index]

opt_blocked = [i for i, j in zip(xb, users)][index]
beam_blocked = [i for i, j in zip(xhb, users)][index]
snr_blocked = [i for i, j in zip(xs5b, users)][index]

opt_clustered = list(xc)[0]  # [i for i, j in zip(xc, users)][index]
beam_clustered = list(xhc)[0]  # [i for i, j in zip(xhc, users)][index]
snr_clustered = list(xs5c)[0]  # [i for i, j in zip(xs5c, users)][index]

print(opt_clustered)

x = pickle.load(
    open(str('Data/Processed/satSINR' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'), 'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/satSINRbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'),
         'rb')).values()
xs5 = pickle.load(
    open(str('Data/Processed/satSINR' + str(beamwidth_deg) + str(M) + str(max_connections) + '_SNRheuristic.p'),
         'rb')).values()

xb = pickle.load(open(str('Data/Processed/sat_blocked' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'),
                      'rb')).values()
xhb = pickle.load(open(
    str('Data/Processed/sat_blockedbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'),
    'rb')).values()
xs5b = pickle.load(
    open(str('Data/Processed/sat_blocked' + str(beamwidth_deg) + str(M) + str(max_connections) + '_SNRheuristic.p'),
         'rb')).values()

xc = pickle.load(
    open(str('Data/Processed/satSINR' + str(beamwidth_deg) + str(M) + str(max_connections) + '_clustered.p'),
         'rb')).values()
xhc = pickle.load(open(
    str('Data/Processed/satSINRbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '_clustered.p'),
    'rb')).values()
xs5c = pickle.load(
    open(str('Data/Processed/satSINR' + str(beamwidth_deg) + str(M) + str(max_connections) + '_SNRheuristic_clustered.p'),
         'rb')).values()

sat_opt = list(x)[index] * 100
sat_blocked = list(xb)[index] * 100
sat_clustered = list(xc)[0] * 100

sat_beam = list(xh)[index] * 100
sat_beam_blocked = list(xhb)[index] * 100
sat_beam_clustered = list(xhc)[0] * 100

sat_snr_opt = list(xs5)[index] * 100
sat_snr_blocked = list(xs5b)[index] * 100
sat_snr_clustered = list(xs5c)[0] * 100

# ------------------------- BLOCKED -----------------------------------------
x = pickle.load(
    open(str('Data/Processed/cap2_5' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'), 'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/cap2_5beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'),
         'rb')).values()
xs5 = pickle.load(open(
    str('Data/Processed/cap2_5' + str(beamwidth_deg) + str(M) + str(max_connections) + '_SNRheuristic.p'),
    'rb')).values()

xb = pickle.load(open(
    str('Data/Processed/cap25' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'), 'rb')).values()
xhb = pickle.load(open(
    str('Data/Processed/cap25beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'),
    'rb')).values()
xs5b = pickle.load(
    open(str('Data/Processed/cap25' + str(beamwidth_deg) + str(M) + str(max_connections) + '_SNRheuristic.p'),
         'rb')).values()

xc = pickle.load(
    open(str('Data/Processed/cap150' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'), 'rb')).values()
xhc = pickle.load(open(
    str('Data/Processed/cap150beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'),
    'rb')).values()
xs5c = pickle.load(
    open(str('Data/Processed/cap150' + str(beamwidth_deg) + str(M) + str(max_connections) + '_SNRheuristic.p'),
         'rb')).values()

optimal_rain2_5 = [i for i, j in zip(x, users)][index]
beam_rain_2_5 = [i for i, j in zip(xh, users)][index]
snr_rain_2_5 = [i for i, j in zip(xs5, users)][index]

optimal_rain25 = [i for i, j in zip(xb, users)][index]
beam_rain_25 = [i for i, j in zip(xhb, users)][index]
snr_rain_25 = [i for i, j in zip(xs5b, users)][index]

optimal_rain150 = [i for i, j in zip(xc, users)][index]
beam_rain_150 = [i for i, j in zip(xhc, users)][index]
snr_rain_150 = [i for i, j in zip(xs5c, users)][index]

x = pickle.load(
    open(str('Data/Processed/sat2_5' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'), 'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/sat2_5beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'),
         'rb')).values()
xs5 = pickle.load(open(
    str('Data/Processed/sat2_5' + str(beamwidth_deg) + str(M) + str(max_connections) + '_SNRheuristic.p'),
    'rb')).values()

xb = pickle.load(
    open(str('Data/Processed/sat25' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'), 'rb')).values()
xhb = pickle.load(open(
    str('Data/Processed/sat25beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'),
    'rb')).values()
xs5b = pickle.load(
    open(str('Data/Processed/sat25' + str(beamwidth_deg) + str(M) + str(max_connections) + '_SNRheuristic.p'),
         'rb')).values()

xc = pickle.load(
    open(str('Data/Processed/sat150' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'), 'rb')).values()
xhc = pickle.load(open(
    str('Data/Processed/sat150beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(max_connections) + '.p'),
    'rb')).values()
xs5c = pickle.load(
    open(str('Data/Processed/sat150' + str(beamwidth_deg) + str(M) + str(max_connections) + '_SNRheuristic.p'),
         'rb')).values()

sat_rain_2_5 = list(x)[index] * 100
sat_beam_rain_2_5 = list(xh)[index] * 100
sat_snr_rain_2_5 = list(xs5)[index] * 100
sat_rain_25 = list(xb)[index] * 100
sat_beam_rain_25 = list(xhb)[index] * 100
sat_snr_rain_25 = list(xs5b)[index] * 100
sat_rain_150 = list(xc)[index] * 100
sat_beam_rain_150 = list(xhc)[index] * 100
sat_snr_rain_150 = list(xs5c)[index] * 100

optimal = [opt_clustered, optimal_rain150, optimal_rain25, optimal_rain2_5, opt_blocked, opt]
beam_align = [beam_clustered, beam_rain_150, beam_rain_25, beam_rain_2_5, beam_blocked, beam]
snr = [snr_clustered, snr_rain_150, snr_rain_25, snr_rain_2_5, snr_blocked, snr_opt]

sat_optimal = [sat_clustered, sat_rain_150, sat_rain_25, sat_rain_2_5, sat_blocked, sat_opt]
sat_beam_align = [sat_beam_clustered, sat_beam_rain_150, sat_beam_rain_25, sat_beam_rain_2_5, sat_beam_blocked,
                  sat_beam]
sat_snr = [sat_snr_clustered, sat_snr_rain_150, sat_snr_rain_25, sat_snr_rain_2_5, sat_snr_blocked, sat_snr_opt]

y = range(6)

print(optimal, beam_align)
print('BEAMALIGN Difference with optimal:', [(i - j) / i * 100 for i, j in zip(optimal, beam_align)])
print('BEAMALIGN Difference with optimal satisfaction:',
      [(i - j) / i * 100 for i, j in zip(sat_optimal, sat_beam_align)])

print('SNRDYNAMIC Difference with optimal:', [(i - j) / i * 100 for i, j in zip(list(optimal), list(snr))])
print('SNRDYNAMIC Difference with optimal satisfaction:', [(i - j) / i * 100 for i, j in zip(sat_optimal, sat_snr)])

print('SNRDYNAMIC Difference with beam:', [(i - j) / i * 100 for i, j in zip(beam_align, snr)])
print('SNRDYNAMIC Difference with beam satisfaction:', [(i - j) / i * 100 for i, j in zip(sat_beam_align, sat_snr)])

fig, ax = plt.subplots()
for i in range(len(y)):
    plt.plot([150, 2000], [i, i], color='grey', zorder=1)

plt.scatter(optimal, y, label='Optimal', color=colors[0], s=100, marker=markers[0], zorder=2)
plt.scatter(beam_align, y, label='ʙᴇᴀᴍ-ᴀʟɪɢɴ', color=colors[1], s=100, marker=markers[1], zorder=2)
plt.scatter(snr, y, label='SNR-dynamic', color=colors[2], s=100, marker=markers[2], zorder=2)

plt.yticks(y, ['Clustered', 'Rain: $R=150$', 'Rain: $R=25$', 'Rain: $R=2.5$', 'Blockage', 'Normal'])
plt.xlabel('Per-user capacity in Mbps')
plt.xlim([400, 1800])
ax.tick_params(top=False,
               bottom=False,
               left=False,
               right=False,
               labelleft=True,
               labelbottom=True)
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.spines.left.set_visible(False)
ax.spines.bottom.set_visible(False)
plt.legend(loc='center left')
# ax.legend(bbox_to_anchor=(0.45, 0.55))
plt.savefig('Figures/capacity_comparison.png')
plt.show()

fig, ax = plt.subplots()
for i in range(len(y)):
    plt.plot([0.0, 1.1], [i, i], color='grey', zorder=1)

plt.scatter(np.divide(sat_optimal, 100), y, label='Optimal', color=colors[0], s=100, marker=markers[0], zorder=2)
plt.scatter(np.divide(sat_beam_align, 100), y, label='ʙᴇᴀᴍ-ᴀʟɪɢɴ', color=colors[1], s=100, marker=markers[1], zorder=2)
plt.scatter(np.divide(sat_snr, 100), y, label='SNR-dynamic', color=colors[2], s=100, marker=markers[2], zorder=2)
plt.yticks(y, ['Clustered', 'Rain: $R=150$', 'Rain: $R=25$', 'Rain: $R=2.5$', 'Blockage', 'Normal'])
plt.xlabel('Satisfaction level')
ax.tick_params(top=False,
               bottom=False,
               left=False,
               right=False,
               labelleft=True,
               labelbottom=True)
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.spines.left.set_visible(False)
ax.spines.bottom.set_visible(False)

plt.legend(loc = 'center left')
# ax.legend(bbox_to_anchor=(0.91, 0.77))
plt.savefig('Figures/satisfaction_comparison.png')
plt.show()
