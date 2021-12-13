import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import functions as f
import time

grid_1bs = np.zeros((xmax, ymax))
grid_2mc = np.zeros((xmax, ymax))
grid_3mc = np.zeros((xmax, ymax))
grid_4mc = np.zeros((xmax, ymax))
grid_5mc = np.zeros((xmax, ymax))

bs = 1

start = time.time()
for iteration in range(10):
    print('Iteration ', iteration)
    np.random.seed(iteration)
    x_user, y_user = f.find_coordinates()
    opt_x, capacity = new_optimization.optimization(x_user, y_user)
    links_per_user = sum(np.transpose(opt_x))
    for user in range(number_of_users):
        if opt_x[user, bs] == 1:
            u = f.user_coords(user, x_user, y_user)
            grid_1bs[int(u[1]), int(u[0])] += 1
        if links_per_user[user] == 2:
            grid_2mc[int(u[1]), int(u[0])] += 1
        elif links_per_user[user] == 3:
            grid_3mc[int(u[1]), int(u[0])] += 1
        elif links_per_user[user] == 4:
            grid_4mc[int(u[1]), int(u[0])] += 1
        elif links_per_user[user] >= 5:
            grid_5mc[int(u[1]), int(u[0])] += 1
    print('one iteration takes', time.time() - start, 'seconds')
    start = time.time()

fig, ax = plt.subplots()
plt.imshow(grid_1bs)
plt.colorbar()
plt.scatter(x_bs, y_bs, color = 'white', marker = 'o')
plt.plot(x_bs[bs], y_bs[bs], color = 'red', marker = 'o')
plt.savefig('number_of_users' + str(number_of_users) + 'bs0.png')

fig, ax = plt.subplots()
plt.imshow(grid_2mc)
plt.colorbar()
plt.scatter(x_bs, y_bs, color = 'white', marker = 'o')
plt.savefig('number_of_users' + str(number_of_users) + '2mc.png')

fig, ax = plt.subplots()
plt.imshow(grid_3mc)
plt.colorbar()
plt.scatter(x_bs, y_bs, color = 'white', marker = 'o')
plt.savefig('number_of_users' + str(number_of_users) + '3mc.png')

fig, ax = plt.subplots()
plt.imshow(grid_4mc)
plt.colorbar()
plt.scatter(x_bs, y_bs, color = 'white', marker = 'o')
plt.savefig('number_of_users' + str(number_of_users) + '4mc.png')

fig, ax = plt.subplots()
plt.imshow(grid_5mc)
plt.colorbar()
plt.scatter(x_bs, y_bs, color = 'white', marker = 'o')
plt.savefig('number_of_users' + str(number_of_users) + '5mc.png')