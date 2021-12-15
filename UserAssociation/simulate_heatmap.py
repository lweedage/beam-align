import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import new_optimization_no_interference
import functions as f
import time
import pickle

delta = 5

grid_1bs = np.zeros((xmax*delta, ymax*delta))
grid_2mc = np.zeros((xmax*delta, ymax*delta))
grid_3mc = np.zeros((xmax*delta, ymax*delta))
grid_4mc = np.zeros((xmax*delta, ymax*delta))
grid_5mc = np.zeros((xmax*delta, ymax*delta))

bs = 1

iteration_min = 1000
iteration_max = 2000

start = time.time()
for iteration in range(iteration_min, iteration_max):
    print('Iteration ', iteration)
    np.random.seed(iteration)
    x_user, y_user = f.find_coordinates()
    if Interference:
        opt_x, capacity = new_optimization.optimization(x_user, y_user)
    else:
        opt_x, capacity = new_optimization_no_interference.optimization(x_user, y_user)

    links_per_user = sum(np.transpose(opt_x))
    for user in range(number_of_users):
        u = f.user_coords(user, x_user, y_user)
        if opt_x[user, bs] == 1:
            grid_1bs[int(u[1]*delta), int(u[0]*delta)] += 1
        if links_per_user[user] == 2:
            grid_2mc[int(u[1]*delta), int(u[0]*delta)] += 1
        elif links_per_user[user] == 3:
            grid_3mc[int(u[1]*delta), int(u[0]*delta)] += 1
        elif links_per_user[user] == 4:
            grid_4mc[int(u[1]*delta), int(u[0]*delta)] += 1
        elif links_per_user[user] >= 5:
            grid_5mc[int(u[1]*delta), int(u[0]*delta)] += 1
    print('one iteration takes', time.time() - start, 'seconds')
    start = time.time()

if Interference:
    pickle.dump(grid_1bs, open(str('Data/grid_1bs_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),'wb'), protocol=4)
    pickle.dump(grid_2mc, open(str('Data/grid_2mc_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),'wb'), protocol=4)
    pickle.dump(grid_3mc, open(str('Data/grid_3mc_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),'wb'), protocol=4)
    pickle.dump(grid_4mc, open(str('Data/grid_4mc_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),'wb'), protocol=4)
    pickle.dump(grid_5mc, open(str('Data/grid_5mc_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),'wb'), protocol=4)
else:
    pickle.dump(grid_1bs, open(str('Data/no_interference_grid_1bs_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),'wb'), protocol=4)
    pickle.dump(grid_2mc, open(str('Data/no_interference_grid_2mc_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),'wb'), protocol=4)
    pickle.dump(grid_3mc, open(str('Data/no_interference_grid_3mc_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),'wb'), protocol=4)
    pickle.dump(grid_4mc, open(str('Data/no_interference_grid_4mc_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),'wb'), protocol=4)
    pickle.dump(grid_5mc, open(str('Data/no_interference_grid_5mc_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + '.p'),'wb'), protocol=4)