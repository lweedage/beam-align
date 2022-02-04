import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import new_optimization_no_interference
import functions as f
import time
import pickle
import os
import find_data

number_of_users = int(input('Number of users?'))

name = str('users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)))
if not user_misalignment:
    name = str(name + 'no_user_misalignment')

iteration_min = 0
iteration_max = iterations[number_of_users]

optimal = []
xs, ys = [], []

start = time.time()
for iteration in range(iteration_min, iteration_max):
    print('Iteration ', iteration)
    np.random.seed(iteration)
    x_user, y_user = f.find_coordinates(number_of_users)
    opt_x, capacity = new_optimization_no_interference.optimization(x_user, y_user)
    pickle.dump(opt_x, open(str('Data/opt_x/iteration_' + str(iteration) + name + '.p'), 'wb'), protocol=4)

    print('one iteration takes', time.time() - start, 'seconds')
    start = time.time()

    optimal.append(opt_x)
    xs.append(x_user)
    ys.append(y_user)

find_data.main(optimal, xs, ys)