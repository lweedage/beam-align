import numpy as np
from parameters import *
import new_optimization
import functions as f
import time
import find_data
import pickle
import progressbar
import os
import get_data

# number_of_users = int(input('Number of users?'))

def from_data(name):
    if os.path.exists(name):
        return pickle.load(open(name, 'rb'))
    else:
        return None


for number_of_users in users:
    iteration_min = 0
    iteration_max = iterations[number_of_users]

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(
        M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))

    if Clustered:
        name = str(name + '_clustered')

    optimal = from_data(str('Data/assignment' + name + '.p'))
    shares = from_data(str('Data/shares' + name + '.p'))
    xs = from_data(str('Data/xs' + name + '.p'))
    ys = from_data(str('Data/ys' + name + '.p'))
    user_capacities = from_data(str('Data/capacity_per_user' + name + '.p'))
    satisfaction = from_data(str('Data/satisfaction' + name + '.p'))
    average_distance = from_data(str('Data/average_distance' + name + '.p'))

    if optimal == None:
        optimal = []
        xs, ys = [], []
        shares = []
        capacities = []
        user_capacities = []
        satisfaction = []
        average_distance = []

        start = time.time()
        bar = progressbar.ProgressBar(maxval=iteration_max, widgets=[
            progressbar.Bar('=', f'Scenario: {scenario}, #users: {number_of_users} [', ']'), ' ',
            progressbar.Percentage(), ' ', progressbar.ETA()])
        bar.start()
        for iteration in range(iteration_min, iteration_max):
            bar.update(iteration)
            np.random.seed(iteration)
            x_user, y_user = f.find_coordinates(number_of_users, Clustered=Clustered)
            opt_x, s, user_capacity, satisfied = new_optimization.optimization(x_user, y_user)
            # print('one iteration takes', time.time() - start, 'seconds')
            # print('Number of users:', number_of_users, 'beamwidth is', np.degrees(beamwidth_b), 'M =', M, 'users per beam =', users_per_beam)
            avg_distance = np.zeros(number_of_users)
            for user in range(number_of_users):
                user_coords = f.user_coords(user, x_user, y_user)
                distances = list()
                for bs in range(number_of_bs):
                    if opt_x[user, bs] > 0.5:
                        bs_coords = f.bs_coords(bs)
                        distances.append(f.find_distance(user_coords, bs_coords))
                avg_distance[user] = sum(distances)/max(1, len(distances))

            start = time.time()
            optimal.append(opt_x)
            shares.append(s)
            xs.append(x_user)
            ys.append(y_user)
            user_capacities.append(user_capacity)
            satisfaction.append(satisfied)
            average_distance.append(avg_distance)

        bar.finish()
        pickle.dump(average_distance, open(str('Data/average_distance' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(optimal, open(str('Data/assignment' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(shares, open(str('Data/shares' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(xs, open(str('Data/xs' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(ys, open(str('Data/ys' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(user_capacities, open(str('Data/capacity_per_user' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(satisfaction, open(str('Data/satisfaction' + name + '.p'), 'wb'), protocol=4)
    find_data.main(optimal, shares, xs, ys, user_capacities, satisfaction, Clustered=Clustered)

get_data.get_data(scenario, user_rate)
