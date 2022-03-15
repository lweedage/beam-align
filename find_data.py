import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import new_optimization
import functions as f
import time
import pickle
import os

def main(optimal, shares, xs, ys, capacities, Heuristic=False, k = 1, SNRHeuristic = False):
    delta = 1
    disconnected = []

    x_max, y_max = int(np.ceil(xmax * delta)), int(np.ceil(ymax * delta))

    grid_sc = np.zeros((y_max, x_max))
    grid_mc = np.zeros((y_max, x_max))

    total_visits = np.zeros((y_max, x_max))

    misalignment_user = []
    misalignment_bs = []
    misalignment_mc = []
    misalignment_sc = []
    distances = []
    distances_sc = []
    distances_mc = []

    total_links_per_user = np.array([])

    no_optimal_value_found = 0

    channel_capacity = []
    channel_capacity_real = []
    channel_capacity_real_per_user = []

    number_of_users = len(xs[0])

    iteration_min = 0
    iteration_max = iterations[number_of_users]


    for iteration in range(iteration_min, iteration_max):
        blockers = pickle.load(open(str('Data/Blockers/blockers' + str(iteration)  + '.p'),'rb'))

        print('Iteration ', iteration)
        np.random.seed(iteration)

        x_user, y_user = xs[iteration], ys[iteration] #f.find_coordinates(number_of_users)
        opt_x = optimal[iteration]

        links_per_user = sum(np.transpose(opt_x))
        total_links_per_user = np.append(total_links_per_user, links_per_user)

        discon = 0

        channel_capacity_per_user = f.find_capacity_per_user(opt_x, x_user, y_user, blockers)
        channel_capacity_real_per_user.append(channel_capacity_per_user)
        channel_capacity_real.append(sum(channel_capacity_per_user))

        for user in range(number_of_users):
            u = f.user_coords(user, x_user, y_user)
            if links_per_user[user] == 1:
                grid_sc[int(u[1]*delta), int(u[0]*delta)] += 1
            elif links_per_user[user] == 0:
                discon += 1
            else:
                grid_mc[int(u[1]*delta), int(u[0]*delta)] += 1
            total_visits[int(u[1]*delta), int(u[0]*delta)] += 1

            for b in range(number_of_bs):
                if opt_x[user, b] == 1:
                    b_coords = f.bs_coords(b)

                    x = f.find_misalignment(b_coords, u, beamwidth_b)
                    dist = f.find_distance(u, b_coords)

                    misalignment_user.append(f.find_misalignment(u, b_coords, beamwidth_u))
                    misalignment_bs.append(x)

                    distances.append(dist)
                    if links_per_user[user] == 1:
                        misalignment_sc.append(x)
                        distances_sc.append(dist)
                    else:
                        misalignment_mc.append(x)
                        distances_mc.append(dist)

        capacity = sum(capacities[iteration])

        if capacity == 0:
            no_optimal_value_found += 1

        channel_capacity.append(capacity)
        disconnected.append(discon)

    name = str('users=' + str(number_of_users) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)) + 'M=' + str(M) + 's=' + str(users_per_beam))

    if Heuristic:
        name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str('SNR_k=' + str(k) + name)


    pickle.dump(grid_mc, open(str('Data/grid_mc_' + name + '.p'),'wb'), protocol=4)
    pickle.dump(grid_sc, open(str('Data/grid_sc_' + name + '.p'),'wb'), protocol=4)
    pickle.dump(total_visits, open(str('Data/grid_total_visits_' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(misalignment_user, open(str('Data/grid_misalignment_user' + name + '.p'),'wb'), protocol=4)
    pickle.dump(misalignment_bs, open(str('Data/grid_misalignment_bs' + name + '.p'),'wb'), protocol=4)
    pickle.dump(misalignment_mc, open(str('Data/grid_misalignment_mc' + name + '.p'),'wb'), protocol=4)
    pickle.dump(misalignment_sc, open(str('Data/grid_misalignment_sc' + name + '.p'),'wb'), protocol=4)

    pickle.dump(distances, open(str('Data/distances' + name + '.p'),'wb'), protocol=4)
    pickle.dump(distances_mc, open(str('Data/distances_mc' + name + '.p'),'wb'), protocol=4)
    pickle.dump(distances_sc, open(str('Data/distances_sc' + name + '.p'),'wb'), protocol=4)

    pickle.dump(total_links_per_user, open(str('Data/total_links_per_user' + name + '.p'),'wb'), protocol=4)

    pickle.dump(channel_capacity, open(str('Data/channel_capacity' + name + '.p'),'wb'), protocol=4)
    pickle.dump(channel_capacity_real, open(str('Data/blocked_capacity' + name + '.p'),'wb'), protocol=4)
    pickle.dump(channel_capacity_real_per_user, open(str('Data/blocked_capacity_per_user' + name + '.p'),'wb'), protocol=4)

    pickle.dump(no_optimal_value_found, open(str('Data/no_optimal_value_found' + name + '.p'),'wb'), protocol=4)
    pickle.dump(disconnected, open(str('Data/disconnected_users' + name + '.p'),'wb'), protocol=4)

    print('average channel capacity:', sum(channel_capacity)/len(channel_capacity))

if __name__ == '__main__':
    Heuristic = False
    SNRHeuristic = False
    number_of_users = int(input('Number of users?'))

    if SNRHeuristic:
        k = int(input('k?'))
    else:
        k = 1

    name = str('users=' + str(number_of_users) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)) + 'M=' + str(M) + 's=' + str(
            users_per_beam))
    if Heuristic:
        name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str('SNR_k=' + str(k) + name)

    optimal = pickle.load(open(str('Data/assignment' + name  + '.p'),'rb'))
    shares = pickle.load(open(str('Data/shares' + name  + '.p'),'rb'))
    xs = pickle.load(open(str('Data/xs' + name + '.p'),'rb'))
    ys = pickle.load(open(str('Data/ys' + name + '.p'),'rb'))
    capacities = pickle.load(open(str('Data/capacity_users' + name + '.p'),'rb'))

    main(optimal, shares, xs, ys, capacities, Heuristic, k, SNRHeuristic)