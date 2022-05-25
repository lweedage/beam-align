import matplotlib.pyplot as plt
# from parameters import *
import numpy as np
import pickle
import seaborn as sns
import math

colors = ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed', 'grey'] * 100
markers = ['o', 's', 'v', '*', 'p', 'P', '1', '+']

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
xs5 = pickle.load(open(str('Data/Processed/capSNR_k=3' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
                       'rb')).values()

xb = pickle.load(open(str('Data/Processed/cap_blocked' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
                      'rb')).values()
xhb = pickle.load(open(
    str('Data/Processed/cap_blockedbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
    'rb')).values()
xs5b = pickle.load(
    open(str('Data/Processed/cap_blockedSNR_k=3' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()

xc = pickle.load(
    open(str('Data/Processed/cap' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '_clustered.p'),
         'rb')).values()
xhc = pickle.load(open(
    str('Data/Processed/capbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(
        user_rate) + '_clustered.p'),
    'rb')).values()
xs5c = pickle.load(
    open(str('Data/Processed/capSNR_k=3' + str(beamwidth_deg) + str(M) + str(s) + str(
        user_rate) + '_clustered.p'),
         'rb')).values()

x = [i for i, j in zip(x, users)][index]
xh = [i for i, j in zip(xh, users)][index]
xs5 = [i for i, j in zip(xs5, users)][index]

xb = [i for i, j in zip(xb, users)][index]
xhb = [i for i, j in zip(xhb, users)][index]
xs5b = [i for i, j in zip(xs5b, users)][index]

xc = [i for i, j in zip(xc, users)][index]
xhc = [i for i, j in zip(xhc, users)][index]
xs5c = [i for i, j in zip(xs5c, users)][index]

margin = 7

fig, ax = plt.subplots()
plt.bar(1, x, width=1, color=colors[0], alpha=0.7, label='Optimal')
# plt.text(1, x + margin, str(round(x)), horizontalalignment='center')
plt.bar(5, xb, width=1, color=colors[0], alpha=0.7)
# plt.text(5, xb + margin, str(round(xb)), horizontalalignment='center')
plt.bar(9, xc, width=1, color=colors[0], alpha=0.7)
# plt.text(9, xc + margin, str(round(xc)), horizontalalignment='center')

plt.bar(2, xh, width=1, color=colors[1], alpha=0.7, label='ʙᴇᴀᴍ-ᴀʟɪɢɴ')
plt.text(2 - 0.17, xh + (x - xh) / 2, str(str(round(-(1 - xh / x) * 100)) + '%'))
ax.annotate("", xytext=(2 - 0.25, x), xy=(2 - 0.25, xh + margin), arrowprops=dict(arrowstyle="->"))
plt.bar(6, xhb, width=1, color=colors[1], alpha=0.7)
plt.text(6 - 0.17, xhb + (xb - xhb) / 2, str('-' + str(round((1 - xhb / xb) * 100)) + '%'))
ax.annotate("", xytext=(6 - 0.25, xb), xy=(6 - 0.25, xhb + margin), arrowprops=dict(arrowstyle="->"))
plt.bar(10, xhc, width=1, color=colors[1], alpha=0.7)
plt.text(10 - 0.17, xhc + (xc - xhc) / 2, str('-' + str(round((1 - xhc / xc) * 100)) + '%'))
ax.annotate("", xytext=(10 - 0.25, xc), xy=(10 - 0.25, xhc + margin), arrowprops=dict(arrowstyle="->"))

plt.bar(3, xs5, width=1, color=colors[2], alpha=0.7, label='SNR-3')
plt.text(3 - 0.17, xs5 + (x - xs5) / 2, str('-' + str(round((1 - xs5 / x) * 100)) + '%'))
ax.annotate("", xytext=(3 - 0.25, x), xy=(3 - 0.25, xs5 + margin), arrowprops=dict(arrowstyle="->"))
plt.bar(7, xs5b, width=1, color=colors[2], alpha=0.7)
plt.text(7 - 0.17, xs5b + (xb - xs5b) / 2, str('-' + str(round((1 - xs5b / xb) * 100)) + '%'))
ax.annotate("", xytext=(7 - 0.25, xb), xy=(7 - 0.25, xs5b + margin), arrowprops=dict(arrowstyle="->"))
plt.bar(11, xs5c, width=1, color=colors[2], alpha=0.7)
plt.text(11 - 0.17, xs5c + (xc - xs5c) / 2, str('-' + str(round((1 - xs5c / xc) * 100)) + '%'))
ax.annotate("", xytext=(11 - 0.25, xc), xy=(11 - 0.25, xs5c + margin), arrowprops=dict(arrowstyle="->"))

x = pickle.load(
    open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/satbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()
xs5 = pickle.load(open(str('Data/Processed/satSNR_k=3' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
                       'rb')).values()

xb = pickle.load(open(str('Data/Processed/sat_blocked' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
                      'rb')).values()
xhb = pickle.load(open(
    str('Data/Processed/sat_blockedbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
    'rb')).values()
xs5b = pickle.load(
    open(str('Data/Processed/sat_blockedSNR_k=3' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()

xc = pickle.load(
    open(str('Data/Processed/sat' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '_clustered.p'),
         'rb')).values()
xhc = pickle.load(open(
    str('Data/Processed/satbeamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(
        user_rate) + '_clustered.p'),
    'rb')).values()
xs5c = pickle.load(
    open(str('Data/Processed/satSNR_k=3' + str(beamwidth_deg) + str(M) + str(s) + str(
        user_rate) + '_clustered.p'),
         'rb')).values()

margin = 50

x = list(x)[index] * 100
xb = list(xb)[index] * 100
xc = list(xc)[index] * 100
xh = list(xh)[index] * 100
xhb = list(xhb)[index] * 100
xhc = list(xhc)[index] * 100
xs5 = list(xs5)[index] * 100
xs5b = list(xs5b)[index] * 100
xs5c = list(xs5c)[index] * 100

plt.text(1, margin, str(str(round(x)) + '%'), horizontalalignment='center')
plt.text(5, margin, str(str(round(xb)) + '%'), horizontalalignment='center')
plt.text(9, margin, str(str(round(xc)) + '%'), horizontalalignment='center')

plt.text(2, margin, str(str(round(xh)) + '%'), horizontalalignment='center')
plt.text(6, margin, str(str(round(xhb)) + '%'), horizontalalignment='center')
plt.text(10, margin, str(str(round(xhc)) + '%'), horizontalalignment='center')

plt.text(3, margin, str(str(round(xs5)) + '%'), horizontalalignment='center')
plt.text(7, margin, str(str(round(xs5b)) + '%'), horizontalalignment='center')
plt.text(11, margin, str(str(round(xs5c)) + '%'), horizontalalignment='center')

plt.ylabel('Per-user capacity (Mbps)')
plt.ylim((0, 1600))
plt.xticks([2, 6, 10], ['Normal', 'Blocked', 'Clustered'])
plt.legend()
plt.savefig(f'Figures/capacity_blocked{beamwidth_deg}{s}{user_rate}')
plt.show()

# ------------------------- BLOCKED -----------------------------------------
x = pickle.load(
    open(str('Data/Processed/cap2_5' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/cap2_5beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()
xs5 = pickle.load(open(
    str('Data/Processed/cap2_5SNR_k=3' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()

xb = pickle.load(open(
    str('Data/Processed/cap25' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xhb = pickle.load(open(
    str('Data/Processed/cap25beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
    'rb')).values()
xs5b = pickle.load(
    open(str('Data/Processed/cap25SNR_k=3' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()

xc = pickle.load(
    open(str('Data/Processed/cap150' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xhc = pickle.load(open(
    str('Data/Processed/cap150beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(
        user_rate) + '.p'), 'rb')).values()
xs5c = pickle.load(
    open(str('Data/Processed/cap150SNR_k=3' + str(beamwidth_deg) + str(M) + str(s) + str(
        user_rate) + '.p'), 'rb')).values()

x = [i for i, j in zip(x, users)][index]
xh = [i for i, j in zip(xh, users)][index]
xs5 = [i for i, j in zip(xs5, users)][index]

xb = [i for i, j in zip(xb, users)][index]
xhb = [i for i, j in zip(xhb, users)][index]
xs5b = [i for i, j in zip(xs5b, users)][index]

xc = [i for i, j in zip(xc, users)][index]
xhc = [i for i, j in zip(xhc, users)][index]
xs5c = [i for i, j in zip(xs5c, users)][index]

margin = 7

fig, ax = plt.subplots()
plt.bar(1, x, width=1, color=colors[0], alpha=0.7, label='Optimal')
# plt.text(1, x + margin, str(round(x)), horizontalalignment='center')
plt.bar(5, xb, width=1, color=colors[0], alpha=0.7)
# plt.text(5, xb + margin, str(round(xb)), horizontalalignment='center')
plt.bar(9, xc, width=1, color=colors[0], alpha=0.7)
# plt.text(9, xc + margin, str(round(xc)), horizontalalignment='center')

plt.bar(2, xh, width=1, color=colors[1], alpha=0.7, label='ʙᴇᴀᴍ-ᴀʟɪɢɴ')
plt.text(2 - 0.10, xh + (x - xh) / 2, str('-' + str(round((1 - xh / x) * 100)) + '%'))
ax.annotate("", xytext=(2 - 0.25, x), xy=(2 - 0.25, xh + margin), arrowprops=dict(arrowstyle="->"))
plt.bar(6, xhb, width=1, color=colors[1], alpha=0.7)
plt.text(6 - 0.10, xhb + (xb - xhb) / 2, str('-' + str(round((1 - xhb / xb) * 100)) + '%'))
ax.annotate("", xytext=(6 - 0.25, xb), xy=(6 - 0.25, xhb + margin), arrowprops=dict(arrowstyle="->"))
plt.bar(10, xhc, width=1, color=colors[1], alpha=0.7)
plt.text(10 - 0.10, xhc + (xc - xhc) / 2, str('-' + str(round((1 - xhc / xc) * 100)) + '%'))
ax.annotate("", xytext=(10 - 0.25, xc), xy=(10 - 0.25, xhc + margin), arrowprops=dict(arrowstyle="->"))

plt.bar(3, xs5, width=1, color=colors[2], alpha=0.7, label='SNR-3')
plt.text(3 - 0.10, xs5 + (x - xs5) / 2, str('-' + str(round((1 - xs5 / x) * 100)) + '%'))
ax.annotate("", xytext=(3 - 0.25, x), xy=(3 - 0.25, xs5 + margin), arrowprops=dict(arrowstyle="->"))
plt.bar(7, xs5b, width=1, color=colors[2], alpha=0.7)
plt.text(7 - 0.10, xs5b + (xb - xs5b) / 2, str('-' + str(round((1 - xs5b / xb) * 100)) + '%'))
ax.annotate("", xytext=(7 - 0.25, xb), xy=(7 - 0.25, xs5b + margin), arrowprops=dict(arrowstyle="->"))
plt.bar(11, xs5c, width=1, color=colors[2], alpha=0.7)
plt.text(11 - 0.10, xs5c + (xc - xs5c) / 2, str('-' + str(round((1 - xs5c / xc) * 100)) + '%'))
ax.annotate("", xytext=(11 - 0.25, xc), xy=(11 - 0.25, xs5c + margin), arrowprops=dict(arrowstyle="->"))

x = pickle.load(
    open(
        str('Data/Processed/sat2_5' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xh = pickle.load(
    open(str('Data/Processed/sat2_5beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()
xs5 = pickle.load(open(
    str('Data/Processed/sat2_5SNR_k=3' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()

xb = pickle.load(
    open(str('Data/Processed/sat25' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xhb = pickle.load(open(
    str('Data/Processed/sat25beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
    'rb')).values()
xs5b = pickle.load(
    open(str('Data/Processed/sat25SNR_k=3' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()

xc = pickle.load(
    open(str('Data/Processed/sat150' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'), 'rb')).values()
xhc = pickle.load(open(
    str('Data/Processed/sat150beamwidth_heuristic' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
    'rb')).values()
xs5c = pickle.load(
    open(str('Data/Processed/sat150SNR_k=3' + str(beamwidth_deg) + str(M) + str(s) + str(user_rate) + '.p'),
         'rb')).values()

margin = 50

x = list(x)[index] * 100
xb = list(xb)[index] * 100
xc = list(xc)[index] * 100
xh = list(xh)[index] * 100
xhb = list(xhb)[index] * 100
xhc = list(xhc)[index] * 100
xs5 = list(xs5)[index] * 100
xs5b = list(xs5b)[index] * 100
xs5c = list(xs5c)[index] * 100

plt.text(1, margin, str(str(round(x)) + '%'), horizontalalignment='center')
plt.text(5, margin, str(str(round(xb)) + '%'), horizontalalignment='center')
plt.text(9, margin, str(str(round(xc)) + '%'), horizontalalignment='center')

plt.text(2, margin, str(str(round(xh)) + '%'), horizontalalignment='center')
plt.text(6, margin, str(str(round(xhb)) + '%'), horizontalalignment='center')
plt.text(10, margin, str(str(round(xhc)) + '%'), horizontalalignment='center')

plt.text(3, margin, str(str(round(xs5)) + '%'), horizontalalignment='center')
plt.text(7, margin, str(str(round(xs5b)) + '%'), horizontalalignment='center')
plt.text(11, margin, str(str(round(xs5c)) + '%'), horizontalalignment='center')

plt.ylabel('Per-user capacity (Mbps)')

plt.xticks([2, 6, 10], ['$R = 2.5$', '$R = 25$', '$R = 150$'])
plt.legend()
plt.savefig(f'Figures/rain{beamwidth_deg}{s}{user_rate}')
plt.show()
