import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import functions as f
import time
import pickle

delta = 2
bs = 0

iteration_min = 0
iteration_max = iterations[number_of_users]

start = time.time()

Heuristic = False
ClosestHeuristic = False

bandwidth_sharing = True


if Heuristic:
    if bandwidth_sharing:
        name = str('beamwidth_heuristic_no_interference_until_iteration_' + str(iteration_max) + 'users=' + str(
            number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
            np.degrees(beamwidth_b)) + 'delta=' + str(delta))
    else:
        name = str('beamwidth_heuristic_nosharing_no_interference_until_iteration_' + str(iteration_max) + 'users=' + str(
            number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
            np.degrees(beamwidth_b)) + 'delta=' + str(delta))

elif ClosestHeuristic:
    name = str('closest_heuristic_no_interference_until_iteration_' + str(iteration_max) + 'users=' + str(
        number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
        np.degrees(beamwidth_b)) + 'delta=' + str(delta))
else:
    name = str('no_interference_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b))+ 'delta=' + str(delta))

grid_1bs = pickle.load(open(str('Data/grid_1bs_' + name + '.p'),'rb'))
grid_2mc = pickle.load(open(str('Data/grid_2mc_' + name + '.p'),'rb'))
grid_3mc = pickle.load(open(str('Data/grid_3mc_' + name + '.p'),'rb'))
grid_4mc = pickle.load(open(str('Data/grid_4mc_' + name + '.p'),'rb'))
grid_5mc = pickle.load(open(str('Data/grid_5mc_' + name + '.p'),'rb'))
total_visits = pickle.load(open(str('Data/grid_total_visits_' + name + '.p'),'rb'))

grid_mc1 = np.add(grid_5mc, grid_4mc)
grid_mc2 = np.add( grid_3mc, grid_2mc)
grid_mc = np.add(grid_mc1, grid_mc2)

grid_mc3plus = np.add(grid_mc1, grid_3mc)


x_large = [x * delta for x in x_bs]
y_large = [y * delta for y in y_bs]

print(np.size(grid_2mc))

xmax = int(np.ceil(xmax))
ymax = int(np.ceil(ymax))

values = range(0, xmax + 1, 10)
real_value = range(0, xmax*delta + 1, 10 * delta)

values_y = range(0, ymax + 1, 10)
real_value_y = range(0, ymax*delta + 1, 10 * delta)

fig, ax = plt.subplots()
plt.imshow(grid_1bs)
plt.colorbar()
plt.scatter(x_large, y_large, color = 'white', marker = 'o')
plt.plot(x_large[bs], y_large[bs], color = 'red', marker = 'o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.title("Where do users connect to the red BS")

fig, ax = plt.subplots()
plt.imshow(grid_2mc/total_visits)
plt.colorbar()
plt.scatter(x_large, y_large, color = 'white', marker = 'o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.title("Where do users have 2MC?")


fig, ax = plt.subplots()
plt.imshow(grid_3mc/total_visits)
plt.colorbar()
plt.scatter(x_large, y_large, color = 'white', marker = 'o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.title("Where do users have 3MC?")


fig, ax = plt.subplots()
plt.imshow(grid_4mc/total_visits)
plt.colorbar()
plt.scatter(x_large, y_large, color = 'white', marker = 'o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.title("Where do users have 4MC?")


fig, ax = plt.subplots()
plt.imshow(grid_5mc/total_visits)
plt.colorbar()
plt.scatter(x_large, y_large, color = 'white', marker = 'o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.title("Where do users have >4MC?")


fig, ax = plt.subplots()
plt.imshow(grid_mc/total_visits)
plt.colorbar()
plt.scatter(x_large, y_large, color = 'white', marker = 'o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.title("Where do users have MC?")

fig, ax = plt.subplots()
plt.imshow(grid_mc3plus/total_visits)
plt.colorbar()
plt.scatter(x_large, y_large, color = 'white', marker = 'o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.title("Where do users have >2 MC?")

plt.show()

fig, ax = plt.subplots()
plt.imshow(total_visits)
plt.colorbar()
plt.scatter(x_large, y_large, color = 'white', marker = 'o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.title("Total visits")
plt.show()