import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from parameters import *
import seaborn as sns

data5 = []
data10 = []
data15 = []

for number_of_users in users:
    iteration_max = iterations[number_of_users]
    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(5) + 'M=' + str(
        M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))
    degrees5 = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
    data5.append(degrees5)

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
        M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))
    degrees10 = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
    data10.append(degrees10)

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(15) + 'M=' + str(
        M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))
    degrees15 = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
    data15.append(degrees15)


labels = [100, 250, 500, 750, 1000]
pos = np.array([250, 750, 1250, 1750, 2250])
fig, ax = plt.subplots()
x = np.array(labels)
width = 100
bplot1 = plt.boxplot(data5, positions=pos - (width + 10),  patch_artist=True,  notch=True,labels = ['','','','',''], widths = width, showfliers = False)
bplot2 = plt.boxplot(data10, positions=pos, patch_artist= True, labels = labels, notch=True, widths = width, showfliers = False)
bplot3 = plt.boxplot(data15, positions=pos + (width + 10), patch_artist=True,  notch=True,labels = ['','','','',''],widths = width, showfliers = False)

for i, bplot in zip(range(3),(bplot1, bplot2, bplot3)):
    color = colors[i]
    for patch in bplot['boxes']:
        patch.set_facecolor(color)
ax.legend([bplot1["boxes"][0], bplot2["boxes"][0], bplot3["boxes"][0]], ['$5\degree$', '$10\degree$', '$15\degree$' ], loc='upper right')
plt.xlabel('User density (per km$^2$)')
plt.ylabel('Number of connections per user')
plt.savefig('boxplot.png')
plt.show()

data_optimal = []
data_beamwidth = []
data_snr = []

for number_of_users in users:
    iteration_max = iterations[number_of_users]
    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
        M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))
    optimal = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
    data_optimal.append(optimal)

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
        M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))
    beamwidth = pickle.load(open(str('Data/total_links_per_userbeamwidth_heuristic' + name + '.p'), 'rb'))
    data_beamwidth.append(beamwidth)

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
        M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))
    snr = pickle.load(open(str('Data/total_links_per_userSNR_k=5' + name + '.p'), 'rb'))
    data_snr.append(snr)

labels = [100, 250, 500, 750, 1000]
pos = np.array([250, 750, 1250, 1750, 2250])
fig, ax = plt.subplots()
x = np.array(labels)
width = 100
bplot1 = plt.boxplot(data_optimal, positions=pos - (width + 10), patch_artist=True, notch=True,
                     labels=['', '', '', '', ''], widths=width, showfliers=False)
bplot2 = plt.boxplot(data_beamwidth, positions=pos, patch_artist=True, labels=labels, notch=True, widths=width,
                     showfliers=False)
bplot3 = plt.boxplot(data_snr, positions=pos + (width + 10), patch_artist=True, notch=True, labels=['', '', '', '', ''],
                     widths=width, showfliers=False)

for i, bplot in zip(range(3), (bplot1, bplot2, bplot3)):
    color = colors[i]
    for patch in bplot['boxes']:
        patch.set_facecolor(color)
ax.legend([bplot1["boxes"][0], bplot2["boxes"][0], bplot3["boxes"][0]], ['Optimal', 'Heuristic', 'SNR'],
          loc='upper right')
plt.savefig('boxplot_degrees.png')
plt.show()
