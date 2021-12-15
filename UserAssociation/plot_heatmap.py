import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import functions as f
import time
import pickle

delta = 5
bs = 1

iteration_min = 0
iteration_max = 1000

start = time.time()
if Interference:
    grid_1bs = pickle.load(open(str('Data/grid_1bs_total_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),'rb'))
    grid_2mc = pickle.load(open(str('Data/grid_2mc_total_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),'rb'))
    grid_3mc = pickle.load(open(str('Data/grid_3mc_total_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),'rb'))
    grid_4mc = pickle.load(open(str('Data/grid_4mc_total_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),'rb'))
    grid_5mc = pickle.load(open(str('Data/grid_5mc_total_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),'rb'))
else:
    grid_1bs = pickle.load(
        open(str('Data/no_interference_grid_1bs_total_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),
             'rb'))
    grid_2mc = pickle.load(
        open(str('Data/no_interference_grid_2mc_total_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),
             'rb'))
    grid_3mc = pickle.load(
        open(str('Data/no_interference_grid_3mc_total_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),
             'rb'))
    grid_4mc = pickle.load(
        open(str('Data/no_interference_grid_4mc_total_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),
             'rb'))
    grid_5mc = pickle.load(
        open(str('Data/no_interference_grid_5mc_total_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),
             'rb'))

grid_mc1 = np.add(grid_5mc, grid_4mc)
grid_mc2 = np.add( grid_3mc, grid_2mc)
grid_mc = np.add(grid_mc1, grid_mc2)

grid_mc3plus = np.add(grid_mc1, grid_3mc)

x_large = [x * delta for x in x_bs]
y_large = [y * delta for y in y_bs]


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
plt.savefig('number_of_users' + str(number_of_users) + 'bs0.png')

fig, ax = plt.subplots()
plt.imshow(grid_2mc)
plt.colorbar()
plt.scatter(x_large, y_large, color = 'white', marker = 'o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.title("Where do users have 2MC?")

plt.savefig('number_of_users' + str(number_of_users) + '2mc.png')

fig, ax = plt.subplots()
plt.imshow(grid_3mc)
plt.colorbar()
plt.scatter(x_large, y_large, color = 'white', marker = 'o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.title("Where do users have 3MC?")

plt.savefig('number_of_users' + str(number_of_users) + '3mc.png')

fig, ax = plt.subplots()
plt.imshow(grid_4mc)
plt.colorbar()
plt.scatter(x_large, y_large, color = 'white', marker = 'o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.title("Where do users have 4MC?")

plt.savefig('number_of_users' + str(number_of_users) + '4mc.png')

fig, ax = plt.subplots()
plt.imshow(grid_5mc)
plt.colorbar()
plt.scatter(x_large, y_large, color = 'white', marker = 'o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.title("Where do users have >4MC?")

plt.savefig('number_of_users' + str(number_of_users) + '5mc.png')

fig, ax = plt.subplots()
plt.imshow(grid_mc)
plt.colorbar()
plt.scatter(x_large, y_large, color = 'white', marker = 'o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.title("Where do users have MC?")
plt.savefig('number_of_users' + str(number_of_users) + 'general_mc.png')

fig, ax = plt.subplots()
plt.imshow(grid_mc3plus)
plt.colorbar()
plt.scatter(x_large, y_large, color = 'white', marker = 'o')
plt.xticks(real_value, values)
plt.yticks(real_value_y, values_y)
plt.title("Where do users have >2 MC?")
plt.savefig('number_of_users' + str(number_of_users) + 'general_3_mc.png')

plt.show()