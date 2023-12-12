import pickle

import matplotlib as mpl
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import progressbar
import seaborn as sns

import functions as f
from parameters import *

params = {'legend.fontsize': 'x-large',
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large',
          'lines.markersize': 8,
          'figure.autolayout': True}
pylab.rcParams.update(params)

Heuristic, SNRHeuristic = False, False
k = 0

number_of_users = 104
iteration_max = 5000 #iterations[number_of_users]

name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(
    M) + 'k=' + str(max_connections)+ 'active_beams=' + str(number_of_active_beams))

if Heuristic:
    name = str('beamwidth_heuristic' + name)

elif SNRHeuristic:
    name = str('SNR_k=' + str(k) + name)

xs = pickle.load(open(str('Data/xs' + name + '.p'), 'rb'))
ys = pickle.load(open(str('Data/ys' + name + '.p'), 'rb'))
total_links_per_user = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
optimal = pickle.load(open(str('Data/assignment' + name + '.p'), 'rb'))

delta = 0.25
x_max, y_max = int(np.ceil(xmax * delta)), int(np.ceil(ymax * delta))
grid = np.zeros((y_max, x_max))
grid_bs = np.zeros((y_max, x_max))

total_visits = np.zeros((y_max, x_max))


bar = progressbar.ProgressBar(maxval=iteration_max, widgets=[
    progressbar.Bar('=', f'Finding data... scenario: {scenario}, #users: {number_of_users} [', ']'), ' ',
    progressbar.Percentage(), ' ', progressbar.ETA()])
bar.start()
for iteration in range(0, iteration_max):
    total_links = total_links_per_user[iteration]
    opt_x = optimal[iteration]
    bar.update(iteration)
    np.random.seed(iteration)
    x_user, y_user = xs[iteration], ys[iteration]

    for user in range(number_of_users):
        u = f.user_coords(user, x_user, y_user)
        grid[int(u[1] * delta), int(u[0] * delta)] += total_links[user]
        total_visits[int(u[1] * delta), int(u[0] * delta)] += 1
        if opt_x[user, bs_of_interest] > 0:
            grid_bs[int(u[1] * delta), int(u[0] * delta)] += 1

x_large = [x * delta for x in x_bs]
y_large = [y * delta for y in y_bs]

xmax = int(np.ceil(xmax))
ymax = int(np.ceil(ymax))

values = range(0, xmax + 1, 200)
real_value = range(0, int(xmax * delta) + 1, int(200 * delta))

values_y = range(0, ymax + 1, 200)
real_value_y = range(0, int(ymax * delta) + 1, int(200 * delta))

cmap = sns.cubehelix_palette(as_cmap=True)
norm = mpl.colors.Normalize(vmin=0, vmax=1)

fig, ax = plt.subplots(figsize = (6,6))
plt.imshow(grid /total_visits, cmap=cmap)
print(grid/total_visits)
plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
plt.scatter(x_large, y_large, color='k', marker='o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.savefig('heatmap_MC.png')
plt.show()

fig, ax = plt.subplots(figsize = (6,6))
plt.imshow(grid_bs / total_visits, cmap=cmap)
plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
plt.scatter(x_large, y_large, color='k', marker='o')
# plt.xlim((0, x_max * delta))
# plt.ylim((0, ymax * delta))
plt.scatter(x_large[bs_of_interest], y_large[bs_of_interest], color='r', marker='*')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
# plt.axis('off')
plt.savefig('heatmap.png')
plt.show()
