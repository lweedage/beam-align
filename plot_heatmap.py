import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import functions as f
import time
import pickle
plt.rcParams["figure.figsize"] = (4, 5)
delta = 2
bs = 0

number_of_users = int(input('Number of users?'))


iteration_min = 0
iteration_max = iterations[number_of_users]

start = time.time()

Heuristic = False
ClosestHeuristic = False

bandwidth_sharing = True


if Heuristic:
    name = str(
        'beamwidth_heuristic' + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(
            np.degrees(beamwidth_b)))
else:
    name = str('users=' + str(number_of_users)  + 'beamwidth_b=' + str(np.degrees(beamwidth_b)))

grid_mc = pickle.load(open(str('Data/grid_mc_' + name + '.p'),'rb'))

total_visits = pickle.load(open(str('Data/grid_total_visits_' + name + '.p'),'rb'))

x_large = [x * delta for x in x_bs]
y_large = [y * delta for y in y_bs]

xmax = int(np.ceil(xmax))
ymax = int(np.ceil(ymax))

values = range(0, xmax + 1, 10)
real_value = range(0, xmax*delta + 1, 10 * delta)

values_y = range(0, ymax + 1, 10)
real_value_y = range(0, ymax*delta + 1, 10 * delta)


fig, ax = plt.subplots()
plt.imshow(grid_mc/total_visits)
plt.colorbar()
plt.scatter(x_large, y_large, color = 'white', marker = 'o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.title("Where do users have MC?")
plt.savefig(str('Figures/mc_heatmap' + name + '.png'))
plt.show()