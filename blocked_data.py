import matplotlib.pyplot as plt
# from parameters import *
import numpy as np
import pickle
import seaborn as sns
import math
import matplotlib.pylab as pylab

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

iterations = {120: 1000, 300: 400, 600: 200, 900: 134, 1200: 100}

users = [120, 300, 600, 900, 1200]
user_density = [100, 250, 500, 750, 1000]

radius = 200  # for triangular grid

xmin, xmax = 0, 800
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

xDelta = xmax - xmin
yDelta = ymax - ymin

M = 10000

s = 2
beamwidth_deg = 10
user_rate = 500

index = 3

x = pickle.load(
    open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
x = [i / j for i, j in zip(x, users)]
x_normal = x

# ------------------------- BLOCKED -----------------------------------------
x = pickle.load(
    open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/capbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()
xs5 = pickle.load(open(str('Data/Processed/capSNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
                       'rb')).values()

xb = pickle.load(open(str('Data/Processed/cap_blocked' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
                      'rb')).values()
xhb = pickle.load(open(
    str('Data/Processed/cap_blockedbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
    'rb')).values()
xs5b = pickle.load(
    open(str('Data/Processed/cap_blockedSNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()

xc = pickle.load(
    open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '_clustered.p'),
         'rb')).values()
xhc = pickle.load(open(
    str('Data/Processed/capbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(
        user_rate) + '_clustered.p'),
    'rb')).values()
xs5c = pickle.load(
    open(str('Data/Processed/capSNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + str(
        user_rate) + '_clustered.p'),
         'rb')).values()

opt = [i for i, j in zip(x, users)][index]
beam = [i for i, j in zip(xh, users)][index]
snr_opt = [i for i, j in zip(xs5, users)][index]

opt_blocked = [i for i, j in zip(xb, users)][index]
beam_blocked = [i for i, j in zip(xhb, users)][index]
snr_blocked = [i for i, j in zip(xs5b, users)][index]

opt_clustered = [i for i, j in zip(xc, users)][index]
beam_clustered = [i for i, j in zip(xhc, users)][index]
snr_clustered = [i for i, j in zip(xs5c, users)][index]

x = pickle.load(
    open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/satbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()
xs5 = pickle.load(open(str('Data/Processed/satSNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
                       'rb')).values()

xb = pickle.load(open(str('Data/Processed/sat_blocked' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
                      'rb')).values()
xhb = pickle.load(open(
    str('Data/Processed/sat_blockedbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
    'rb')).values()
xs5b = pickle.load(
    open(str('Data/Processed/sat_blockedSNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()

xc = pickle.load(
    open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '_clustered.p'),
         'rb')).values()
xhc = pickle.load(open(
    str('Data/Processed/satbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(
        user_rate) + '_clustered.p'),
    'rb')).values()
xs5c = pickle.load(
    open(str('Data/Processed/satSNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + str(
        user_rate) + '_clustered.p'),
         'rb')).values()

sat_opt = list(x)[index] * 100
sat_blocked = list(xb)[index] * 100
sat_clustered = list(xc)[index] * 100

sat_beam = list(xh)[index] * 100
sat_beam_blocked = list(xhb)[index] * 100
sat_beam_clustered = list(xhc)[index] * 100

sat_snr_opt = list(xs5)[index] * 100
sat_snr_blocked = list(xs5b)[index] * 100
sat_snr_clustered = list(xs5c)[index] * 100

# ------------------------- BLOCKED -----------------------------------------
x = pickle.load(
    open(str('Data/Processed/cap2_5' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/cap2_5beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()
xs5 = pickle.load(open(
    str('Data/Processed/cap2_5SNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()

xb = pickle.load(open(
    str('Data/Processed/cap25' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xhb = pickle.load(open(
    str('Data/Processed/cap25beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
    'rb')).values()
xs5b = pickle.load(
    open(str('Data/Processed/cap25SNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()

xc = pickle.load(
    open(str('Data/Processed/cap150' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xhc = pickle.load(open(
    str('Data/Processed/cap150beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(
        user_rate) + '.p'), 'rb')).values()
xs5c = pickle.load(
    open(str('Data/Processed/cap150SNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + str(
        user_rate) + '.p'), 'rb')).values()

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
    open(str('Data/Processed/sat2_5' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/sat2_5beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()
xs5 = pickle.load(open(
    str('Data/Processed/sat2_5SNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()

xb = pickle.load(
    open(str('Data/Processed/sat25' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xhb = pickle.load(open(
    str('Data/Processed/sat25beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
    'rb')).values()
xs5b = pickle.load(
    open(str('Data/Processed/sat25SNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()

xc = pickle.load(
    open(str('Data/Processed/sat150' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xhc = pickle.load(open(
    str('Data/Processed/sat150beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
    'rb')).values()
xs5c = pickle.load(
    open(str('Data/Processed/sat150SNR_k=1' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
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
print('BEAMALIGN Difference with optimal:', [(i - j) / i * 100 for i, j in zip(optimal, beam_align)])
print('BEAMALIGN Difference with optimal satisfaction:',
      [(i - j) / i * 100 for i, j in zip(sat_optimal, sat_beam_align)])

print('SNRDYNAMIC Difference with optimal:', [(i - j) / i * 100 for i, j in zip(optimal, snr)])
print('SNRDYNAMIC Difference with optimal satisfaction:', [(i - j) / i * 100 for i, j in zip(sat_optimal, sat_snr)])

fig, ax = plt.subplots()
for i in range(len(y)):
    plt.plot([150, 1100], [i, i], color='grey', zorder=1)

plt.scatter(optimal, y, label='Optimal', color=colors[0], s=100, marker=markers[0], zorder=2)
plt.scatter(beam_align, y, label='ʙᴇᴀᴍ-ᴀʟɪɢɴ', color=colors[1], s=100, marker=markers[1], zorder=2)
plt.scatter(snr, y, label='SNR-dynamic', color=colors[2], s=100, marker=markers[2], zorder=2)

plt.yticks(y, ['Clustered', 'Rain: $R=150$', 'Rain: $R=25$', 'Rain: $R=2.5$', 'Blockage', 'Normal'])
plt.xlabel('Per-user capacity in Mbps')
plt.xlim([100, 1150])
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
plt.legend()
ax.legend(bbox_to_anchor=(0.45, 0.55))
plt.savefig('Figures/capacity_comparison.png')
plt.show()

fig, ax = plt.subplots()
for i in range(len(y)):
    plt.plot([0.15, 1.1], [i, i], color='grey', zorder=1)

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

plt.legend()
ax.legend(bbox_to_anchor=(0.91, 0.77))
plt.savefig('Figures/satisfaction_comparison.png')
plt.show()
