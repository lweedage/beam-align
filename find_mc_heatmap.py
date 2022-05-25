import matplotlib.pyplot as plt
from parameters import *
import functions as f
import pickle
import progressbar
import matplotlib as mpl
import seaborn as sns

Heuristic, SNRHeuristic, GreedyRate = True, False, False

number_of_users = 120
iteration_max = iterations[number_of_users]

name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))

if Heuristic:
    name = str('beamwidth_heuristic' + name)

elif SNRHeuristic:
    name = str('SNR_k=' + str(k) + name)

elif GreedyRate:
    name = str(name + 'GreedyRate')

if Clustered:
    name = str(name + '_clustered')

if AT:
    name = str(name + 'rate' + str(rain_rate))

xs = pickle.load(open(str('Data/xs' + name + '.p'), 'rb'))
ys = pickle.load(open(str('Data/ys' + name + '.p'), 'rb'))
total_links_per_user = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))


delta = 1
x_max, y_max = int(np.ceil(xmax * delta)), int(np.ceil(ymax * delta))
grid = np.zeros((y_max, x_max))
total_visits = np.zeros((y_max, x_max))

bar = progressbar.ProgressBar(maxval=iteration_max, widgets=[progressbar.Bar('=', f'Finding data... scenario: {scenario}, #users: {number_of_users} [', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()])
bar.start()
for iteration in range(0, iteration_max):
    total_links = total_links_per_user[iteration]
    bar.update(iteration)
    np.random.seed(iteration)
    x_user, y_user = xs[iteration], ys[iteration]

    for user in range(number_of_users):
        u = f.user_coords(user, x_user, y_user)
        grid[int(u[1]*delta), int(u[0]*delta)] += total_links[user]
        total_visits[int(u[1]*delta), int(u[0]*delta)] += 1


x_large = [x * delta for x in x_bs]
y_large = [y * delta for y in y_bs]

xmax = int(np.ceil(xmax))
ymax = int(np.ceil(ymax))

values = range(0, xmax + 1, 200)
real_value = range(0, int(xmax * delta) + 1, int(200 * delta))

values_y = range(0, ymax + 1, 200)
real_value_y = range(0, int(ymax * delta)+ 1, int(200 * delta))


cmap = sns.cubehelix_palette(as_cmap=True)
norm = mpl.colors.Normalize(vmin=0, vmax=np.max(total_links_per_user))

fig, ax = plt.subplots()
plt.imshow(grid / total_visits, cmap=cmap)
plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap))
plt.scatter(x_large, y_large, color='k', marker='o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.show()

x_division = 4
y_division = 6

together = np.zeros((int(y_max/y_division), x_max))
together_visits = np.zeros((int(y_max/y_division), x_max))

for i in range(y_division):
    start = i * int(y_max/y_division)
    end = (i+1) * int(y_max/y_division)
    together += grid[start:end, :]
    together_visits += total_visits[start:end, :]

together_both = np.zeros((int(y_max/y_division), int(x_max/x_division)))
together_visits_both = np.zeros((int(y_max/y_division), int(x_max/x_division)))

for i in range(x_division):
    start =i * int(x_max/x_division)
    end = (i+1) * int(x_max/x_division)
    together_both += together[:, start:end]
    together_visits_both += together_visits[:, start:end]


fig, ax = plt.subplots()
plt.imshow(together_both / together_visits_both, cmap=cmap)
plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap))
# plt.scatter(x_large, y_large, color='k', marker='o')
# plt.xlim((0, x_max//2))
# plt.xticks(real_value, values)
# plt.yticks(real_value_y, values_y)
plt.show()
