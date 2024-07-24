import os
import pickle

import matplotlib
import matplotlib.pyplot as plt

import functions as f
from parameters import *
import seaborn

matplotlib.rcParams['font.size'] = 20
matplotlib.rcParams['legend.fontsize'] = 18  # using a size in points
matplotlib.rcParams['text.usetex'] = True
# matplotlib.rcParams['axes.grid'] = True
matplotlib.rcParams['lines.markersize'] = 7
matplotlib.rcParams['figure.autolayout'] = True
plt.rcParams['text.latex.preamble'] = " \\usepackage{amsmath} \\usepackage{gensymb} "

colors = ['#904C77', '#E49AB0', '#ECB8A5', '#96ACB7', '#957D95'] * 100
markers = ['o', 'X', 'v', 's', '*', 'P', '1', '+']
# colors = seaborn.color_palette('Set2', 12)

def load_file(name):
    if os.path.exists(name):
        return pickle.load(open(str(name), 'rb'))
    else:
        return None


def find_naam(max_connections, iteration_max, number_of_users, Heuristic, SNRHeuristic, Clustered, M, Greedy=False,
              Harris=False):
    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(
        M) + 'k=' + str(max_connections) + 'active_beams=' + str(number_of_active_beams))

    if Heuristic:
        name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str(name + '_SNRheuristic')

    elif Harris:
        name = str('HHO' + name)

    if Clustered:
        name = str(name + '_clustered')

    if Greedy and Heuristic:
        name = str(name + '_greedy')
    return name


def find_occupied_beams(opt_x, x_user, y_user):
    directions_bs = range(int(360 / beamwidth_b))
    occupied_beams = np.zeros((number_of_bs, len(directions_bs)))
    for bs in range(number_of_bs):
        for user in range(number_of_users):
            if opt_x[user, bs] > 0:
                user_coords = f.user_coords(user, x_user, y_user)
                bs_coords = f.bs_coords(bs)
                geo = f.find_geo(bs_coords, user_coords)
                beam_number = f.find_beam_number(geo, beamwidth_b)
                occupied_beams[bs, beam_number] = 1
    return occupied_beams


Heuristic = False
SNRHeuristic = False

labels = [50, 100, 250, 500, 750]
pos = np.array([250, 750, 1250, 1750, 2250])

# fig, ax = plt.subplots()
x = np.array(labels)
width = 100

number_of_beams = dict()
# users = [312]
for max_connections in [1, 2, 25]:
# for max_connections in [25]:

    number_of_beams[max_connections] = dict()
    for number_of_users in users:

        number_of_beams[max_connections][number_of_users] = []
        iteration_max = iterations[number_of_users]
        name = find_naam(max_connections, iteration_max, number_of_users, Heuristic, SNRHeuristic, Clustered, M)
        assignment = load_file('Data/assignment' + name + '.p')
        x_users = load_file('Data/xs' + name + '.p')
        y_users = load_file('Data/ys' + name + '.p')
        occupied = np.zeros((number_of_bs, 360 // beamwidth_b))
        for opt_x, x_user, y_user in zip(assignment, x_users, y_users):
            occupied_beams = find_occupied_beams(opt_x, x_user, y_user)
            if np.sum(occupied_beams) > 0:
                number_of_beams[max_connections][number_of_users].append(np.sum(occupied_beams))
            # occupied += np.sum(occupied_beams, axis = 0)
            # occupied += np.sum(occupied_beams, axis = 0)
            occupied += occupied_beams
        occupied = occupied_beams
        w = 0.3
        h = 0.3
        maximum = ymax * 1.1
        coords = [(x/maximum, y/maximum, w, h) for x, y in zip(x_bs, y_bs)]

        # fig = plt.figure(figsize = (12, 14))
        # for bs in range(number_of_bs):
        #     ax = fig.add_axes(coords[bs], polar = True, frameon = False)
        #     width = beamwidth_b / 360 * (2 * pi)
        #
        #     # Compute the angle each bar is centered on:
        #     indices = list(range(1, 360 // beamwidth_b + 1))
        #     angles = [width * i for i in range(int(-pi / width), int(pi / width))]
        #     # Draw bars
        #     bars = ax.bar(
        #         x=angles,
        #         height=occupied[bs],
        #         width=width,
        #         bottom=0,
        #         linewidth=3,
        #         edgecolor="white",
        #         color=colors[bs])
        #     ax.axis('off')
        #
        # plt.show()

fig, ax = plt.subplots()
meanlineprops = dict(linestyle='--', linewidth=1, color='white')

# bplot1 = plt.boxplot([j for j in number_of_beams[5].values()], positions=pos - (width + 10), patch_artist=True, medianprops=meanlineprops,
#                      labels=['', '', '', '', ''], widths=width, showfliers=False)
# bplot2 = plt.boxplot([j for j in number_of_beams[10].values()], positions=pos, patch_artist=True, labels=labels, medianprops=meanlineprops, widths=width,
#                      showfliers=False)
# bplot3 = plt.boxplot([j for j in number_of_beams[15].values()], positions=pos + (width + 10), patch_artist=True, medianprops=meanlineprops,
#                      labels=['', '', '', '', ''], widths=width, showfliers=False)
#


# plt.bar(pos - (width + 10), [sum(j) / max(1, len(j)) for j in number_of_beams[5].values()], width=width,
#         color=colors[0], label = '$5\\degree$')
# plt.bar(pos, [sum(j) / max(1, len(j)) for j in number_of_beams[10].values()], width=width, color=colors[1], label = '$10\\degree$')
# plt.bar(pos + (width + 10), [sum(j) / max(1, len(j)) for j in number_of_beams[15].values()], color=colors[2],
#         width=width, label = '$15\\degree$')

print(number_of_beams)
plt.bar(pos - (width + 10), [sum(j) / max(1, len(j)) for j in number_of_beams[1].values()], width=width,
        color=colors[0], label='$k=1$')
plt.bar(pos, [sum(j) / max(1, len(j)) for j in number_of_beams[2].values()], width=width, color=colors[1],
        label='$k=2$')
plt.bar(pos + (width + 10), [sum(j) / max(1, len(j)) for j in number_of_beams[25].values()], color=colors[2],
        width=width, label='$k=\\infty$')

# for i, bplot in zip(range(3), (bplot1, bplot2, bplot3)):
#     color = colors[i]
#     for patch in bplot['boxes']:
#         patch.set_facecolor(color)
# ax.legend([bplot1["boxes"][0], bplot2["boxes"][0], bplot3["boxes"][0]], ['$5\degree$', '$10\degree$', '$15\degree$'],
#           loc='lower right')
plt.legend(loc='upper left')
plt.xticks(pos, [50, 100, 250, 500, 750])
plt.xlabel('Users per km$^2$')
plt.ylabel('Number of active beams')
plt.savefig('number_of_active_beams.pdf')
plt.show()
