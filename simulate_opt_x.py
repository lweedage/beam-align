import numpy as np
from parameters import *
import new_optimization
import functions as f
import time
import find_data
import pickle
import progressbar

# number_of_users = int(input('Number of users?'))

for number_of_users in [100, 300, 500, 750, 1000]:

    iteration_min = 0
    iteration_max = iterations[number_of_users]

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)) + 'M=' + str(M) + 's=' + str(users_per_beam))
    if Clustered:
        name = str(name + '_clustered')

    optimal = pickle.load(open(str('Data/assignment' + name + '.p'), 'rb'))
    shares = pickle.load(open(str('Data/shares' + name + '.p'), 'rb'))
    xs = pickle.load(open(str('Data/xs' + name + '.p'), 'rb'))
    ys = pickle.load(open(str('Data/ys' + name + '.p'), 'rb'))
    user_capacities = pickle.load(open(str('Data/capacity_per_user' + name + '.p'), 'rb'))

    if optimal == None:
        optimal = []
        xs, ys = [], []
        shares = []
        capacities = []
        user_capacities = []


        start = time.time()
        bar = progressbar.ProgressBar(maxval=iteration_max, widgets=[progressbar.Bar('=', f'Scenario: {scenario}, #users: {number_of_users} [', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()])
        bar.start()
        for iteration in range(iteration_min, iteration_max):
            bar.update(iteration)
            np.random.seed(iteration)
            x_user, y_user = f.find_coordinates(number_of_users, Clustered = True)
            opt_x, s, user_capacity = new_optimization.optimization(x_user, y_user)
            # print('one iteration takes', time.time() - start, 'seconds')
            # print('Number of users:', number_of_users, 'beamwidth is', np.degrees(beamwidth_b), 'M =', M, 'users per beam =', users_per_beam)
            start = time.time()

            optimal.append(opt_x)
            shares.append(s)
            xs.append(x_user)
            ys.append(y_user)
            user_capacities.append(user_capacity)
        bar.finish()


        pickle.dump(optimal, open(str('Data/assignment' + name  + '.p'),'wb'), protocol=4)
        pickle.dump(shares, open(str('Data/shares' + name  + '.p'),'wb'), protocol=4)
        pickle.dump(xs, open(str('Data/xs' + name + '.p'),'wb'), protocol=4)
        pickle.dump(ys, open(str('Data/ys' + name + '.p'),'wb'), protocol=4)
        pickle.dump(user_capacities, open(str('Data/capacity_per_user' + name + '.p'),'wb'), protocol=4)

    find_data.main(optimal, shares, xs, ys, user_capacities, Clustered = Clustered)
