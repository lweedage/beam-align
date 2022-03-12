import numpy as np
from parameters import *
import new_optimization
import functions as f
import time
import find_data
import pickle

# number_of_users = int(input('Number of users?'))

for number_of_users in [100, 300, 500, 750, 1000]:

    name = str('users=' + str(number_of_users) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)) + 'M=' + str(M) + 's=' + str(users_per_beam))

    iteration_min = 0
    iteration_max = iterations[number_of_users]

    optimal = []
    xs, ys = [], []
    shares = []
    capacities = []

    start = time.time()
    for iteration in range(iteration_min, iteration_max):
        print('Iteration ', iteration)
        np.random.seed(iteration)
        x_user, y_user = f.find_coordinates(number_of_users)
        opt_x, s, capacity = new_optimization.optimization(x_user, y_user)
        print('one iteration takes', time.time() - start, 'seconds')
        print('Number of users:', number_of_users, 'beamwidth is', np.degrees(beamwidth_b), 'M =', M, 'users per beam =', users_per_beam)

        start = time.time()

        optimal.append(opt_x)
        shares.append(s)
        xs.append(x_user)
        ys.append(y_user)
        capacities.append(capacity)


    pickle.dump(optimal, open(str('Data/assignment' + name  + '.p'),'wb'), protocol=4)
    pickle.dump(shares, open(str('Data/shares' + name  + '.p'),'wb'), protocol=4)
    pickle.dump(xs, open(str('Data/xs' + name + '.p'),'wb'), protocol=4)
    pickle.dump(ys, open(str('Data/ys' + name + '.p'),'wb'), protocol=4)
    pickle.dump(capacities, open(str('Data/capacity_users' + name + '.p'),'wb'), protocol=4)
    find_data.main(optimal, shares, xs, ys, capacities)
