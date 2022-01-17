import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import new_optimization_no_interference
import functions as f
import time
import pickle
import os

if Interference:
    name = str('with_interference_users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)))
else:
    name = str('users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)))

iteration_min = 1000
iteration_max = 5000

start = time.time()
for iteration in range(iteration_min, iteration_max):
    print('Iteration ', iteration)
    np.random.seed(iteration)
    x_user, y_user = f.find_coordinates()

    if Interference:
        opt_x, capacity = new_optimization.optimization(x_user, y_user)
    else:
        opt_x, capacity = new_optimization_no_interference.optimization(x_user, y_user)
    pickle.dump(opt_x, open(str('Data/opt_x/iteration_' + str(iteration) + name + '.p'), 'wb'), protocol=4)

    print('one iteration takes', time.time() - start, 'seconds')
    start = time.time()