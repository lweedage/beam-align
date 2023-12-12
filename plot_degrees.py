import pickle

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt

from parameters import *

params = {'legend.fontsize': 'xx-large',
          'axes.labelsize': 'xx-large',
          'axes.titlesize': 'xx-large',
          'xtick.labelsize': 'xx-large',
          'ytick.labelsize': 'xx-large',
          'lines.markersize': 8,
          'figure.autolayout': True}
pylab.rcParams.update(params)


def flatten(data):
    return [item for row in data for item in row]


users_per_beam = 1

data5 = []
data10 = []
data15 = []

meanlineprops = dict(linestyle='--', linewidth=1, color='white')

for number_of_users in users:
    iteration_max = iterations[number_of_users]
    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(5) + 'M=' + str(
        M) + 'k=' + str(max_connections) + 'active_beams=' + str(number_of_active_beams))
    degrees5 = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
    data5.append(flatten(degrees5))

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
        M) + 'k=' + str(max_connections) + 'active_beams=' + str(number_of_active_beams))
    degrees10 = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
    data10.append(flatten(degrees10))

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(15) + 'M=' + str(
        M) + 'k=' + str(max_connections) + 'active_beams=' + str(number_of_active_beams))
    degrees15 = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
    data15.append(flatten(degrees15))

labels = [50, 100, 250, 500, 750]
pos = np.array([250, 750, 1250, 1750, 2250])

fig, ax = plt.subplots()
x = np.array(labels)
width = 100
bplot1 = plt.boxplot(data5, positions=pos - (width + 10), patch_artist=True, medianprops=meanlineprops,
                     labels=['', '', '', '', ''], widths=width, showfliers=False)
bplot2 = plt.boxplot(data10, positions=pos, patch_artist=True, labels=labels, medianprops=meanlineprops, widths=width,
                     showfliers=False)
bplot3 = plt.boxplot(data15, positions=pos + (width + 10), patch_artist=True, medianprops=meanlineprops,
                     labels=['', '', '', '', ''], widths=width, showfliers=False)

for i, bplot in zip(range(3), (bplot1, bplot2, bplot3)):
    color = colors[i]
    for patch in bplot['boxes']:
        patch.set_facecolor(color)
ax.legend([bplot1["boxes"][0], bplot2["boxes"][0], bplot3["boxes"][0]], ['$5\degree$', '$10\degree$', '$15\degree$'],
          loc='upper right')
plt.xlabel('Users per km$^2$')
plt.ylabel('Number of connections per user')
plt.savefig('boxplot.png')
plt.show()

data5 = []
data10 = []
data15 = []

meanlineprops = dict(linestyle='--', linewidth=1, color='white')

for number_of_users in users:
    iteration_max = iterations[number_of_users]
    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
        M) + 'k=' + str(1) + 'active_beams=' + str(number_of_active_beams))
    degrees5 = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
    data5.append(flatten(degrees5))

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
        M) + 'k=' + str(2) + 'active_beams=' + str(number_of_active_beams))
    degrees10 = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
    data10.append(flatten(degrees10))

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
        M) + 'k=' + str(25) + 'active_beams=' + str(number_of_active_beams))
    degrees15 = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
    data15.append(flatten(degrees15))

labels = [50, 100, 250, 500, 750]
pos = np.array([250, 750, 1250, 1750, 2250])

fig, ax = plt.subplots()
x = np.array(labels)
width = 100
bplot1 = plt.boxplot(data5, positions=pos - (width + 10), patch_artist=True, medianprops=meanlineprops,
                     labels=['', '', '', '', ''], widths=width, showfliers=False)
bplot2 = plt.boxplot(data10, positions=pos, patch_artist=True, labels=labels, medianprops=meanlineprops, widths=width,
                     showfliers=False)
bplot3 = plt.boxplot(data15, positions=pos + (width + 10), patch_artist=True, medianprops=meanlineprops,
                     labels=['', '', '', '', ''], widths=width, showfliers=False)

for i, bplot in zip(range(3), (bplot1, bplot2, bplot3)):
    color = colors[i]
    for patch in bplot['boxes']:
        patch.set_facecolor(color)
ax.legend([bplot1["boxes"][0], bplot2["boxes"][0], bplot3["boxes"][0]], ['$k=1$', '$k=2$', '$k = \infty$'],
          loc='upper right')
plt.xlabel('Users per km$^2$')
plt.ylabel('Number of connections per user')
plt.savefig('boxplot_mc.png')
plt.show()

data_optimal = []
data_beamwidth = []
data_snr = []

users_per_beam = 2

for number_of_users in users:
    iteration_max = iterations[number_of_users]
    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(10) + 'M=' + str(
        M) + 'k=' + str(max_connections) + 'active_beams=10')
    optimal = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
    data_optimal.append([item for sublist in optimal for item in sublist])
    beamwidth = pickle.load(open(str('Data/total_links_per_userbeamwidth_heuristic' + name + '.p'), 'rb'))
    data_beamwidth.append([item for sublist in beamwidth for item in sublist])
    snr = pickle.load(open(str('Data/total_links_per_user' + name + '_SNRheuristic.p'), 'rb'))
    data_snr.append([item for sublist in snr for item in sublist])

labels = [50, 100, 250, 500, 750]
pos = np.array([250, 750, 1250, 1750, 2250])
fig, ax = plt.subplots()
x = np.array(labels)
width = 100

bplot1 = plt.boxplot(data_optimal, positions=pos - (width + 10), patch_artist=True,
                     labels=['', '', '', '', ''], widths=width, showfliers=False, medianprops=meanlineprops)
bplot2 = plt.boxplot(data_beamwidth, positions=pos, patch_artist=True, labels=labels, medianprops=meanlineprops,
                     widths=width,
                     showfliers=False)
bplot3 = plt.boxplot(data_snr, positions=pos + (width + 10), patch_artist=True, medianprops=meanlineprops,
                     labels=['', '', '', '', ''],
                     widths=width, showfliers=False)

print([sum([1 for i in data if i == 0]) for data in data_snr])

for i, bplot in zip(range(3), (bplot1, bplot2, bplot3)):
    color = colors[i]
    for patch in bplot['boxes']:
        patch.set_facecolor(color)
ax.legend([bplot1["boxes"][0], bplot2["boxes"][0], bplot3["boxes"][0]], ['Optimal', 'ʙᴇᴀᴍ-ᴀʟɪɢɴ', 'SNR-dynamic'],
          loc='upper right')
plt.xlabel('Users per km$^2$')
plt.ylabel('Number of connections per user')
plt.savefig('boxplot_degrees.png')
plt.show()
