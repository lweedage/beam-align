import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import new_optimization_no_interference
import functions as f
import time
import pickle
import os

def main(optimal, xs, ys, Heuristic=False, bandwidth_sharing=False, user_beamforming = False, MCHeuristic = False, k = 1, SNRHeuristic = False):
    delta = 2

    x_max, y_max = int(np.ceil(xmax * delta)), int(np.ceil(ymax * delta))

    grid_1bs = np.zeros((y_max, x_max))
    grid_2mc = np.zeros((y_max, x_max))
    grid_3mc = np.zeros((y_max, x_max))
    grid_4mc = np.zeros((y_max, x_max))
    grid_5mc = np.zeros((y_max, x_max))

    total_visits = np.zeros((y_max, x_max))

    misalignment_user = []
    misalignment_mc = []
    misalignment_bs = []
    misalignment_sc = []
    misalignment_2mc = []
    misalignment_3mc = []
    misalignment_4mc = []
    misalignment_5mc = []
    distances = []
    distances_sc = []
    distances_mc = []
    distances_2mc = []
    distances_3mc = []
    distances_4mc = []
    distances_5mc = []

    total_links_per_user = np.array([])

    no_optimal_value_found = 0

    bs = 0

    channel_capacity = []
    number_of_users = len(xs[0])

    iteration_min = 0
    iteration_max = iterations[number_of_users]

    # MCClosestHeuristic = False
    #
    # if MCClosestHeuristic:
    #     k = int(input('k='))

    for iteration in range(iteration_min, iteration_max):
        print('Iteration ', iteration)
        np.random.seed(iteration)

        x_user, y_user = xs[iteration], ys[iteration] #f.find_coordinates(number_of_users)
        opt_x = optimal[iteration]

        links_per_user = sum(np.transpose(opt_x))
        total_links_per_user = np.append(total_links_per_user, links_per_user)

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
            total_visits[int(u[1]*delta), int(u[0]*delta)] += 1

            for b in range(number_of_bs):
                if opt_x[user, b] == 1:
                    b_coords = f.bs_coords(b)
                    misalignment_user.append(f.find_misalignment(u, b_coords, beamwidth_u))
                    misalignment_bs.append(f.find_misalignment(b_coords, u, beamwidth_b))
                    x = f.find_misalignment(b_coords, u, beamwidth_b)
                    dist = f.find_distance(u, b_coords)
                    distances.append(dist)
                    if links_per_user[user] == 1:
                        misalignment_sc.append(x)
                        distances_sc.append(dist)
                    elif links_per_user[user] > 1:
                        misalignment_mc.append(x)
                        distances_mc.append(dist)
                    if links_per_user[user] == 2:
                        misalignment_2mc.append(x)
                        distances_2mc.append(dist)
                    elif links_per_user[user] == 3:
                        misalignment_3mc.append(x)
                        distances_3mc.append(dist)
                    elif links_per_user[user] == 4:
                        misalignment_4mc.append(x)
                        distances_4mc.append(dist)
                    elif links_per_user[user] >= 5:
                        misalignment_5mc.append(x)
                        distances_5mc.append(dist)

        capacity = f.find_capacity(opt_x, x_user, y_user)
        print(capacity)
        if capacity == 0:
            no_optimal_value_found += 1
        channel_capacity.append(capacity)


    if Heuristic:
        if bandwidth_sharing:
            name = str('beamwidth_heuristic_no_interference_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b))+ 'delta=' + str(delta))
        elif user_beamforming:
            name = str('beamwidth_heuristic_user_beamforming_no_interference_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b))+ 'delta=' + str(delta))
        else:
            name = str('beamwidth_heuristic_nosharing_no_interference_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b))+ 'delta=' + str(delta))

    elif MCHeuristic:
        name = str('MC_closest_heuristic_no_interference_until_iteration_' + str(iteration_max) + 'k=' + str(k) + 'users=' + str(
            number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
            np.degrees(beamwidth_b)) + 'delta=' + str(delta))

    elif SNRHeuristic:
        name = str('SNR_closest_heuristic_no_interference_until_iteration_' + str(iteration_max) + 'k=' + str(k) + 'users=' + str(
            number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
            np.degrees(beamwidth_b)) + 'delta=' + str(delta))
    else:
        name = str('no_interference_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b))+ 'delta=' + str(delta))

    if not user_misalignment:
        name = str(name + 'no_user_misalignment')

    pickle.dump(grid_1bs, open(str('Data/grid_1bs_' + name + '.p'),'wb'), protocol=4)
    pickle.dump(grid_2mc, open(str('Data/grid_2mc_' + name + '.p'),'wb'), protocol=4)
    pickle.dump(grid_3mc, open(str('Data/grid_3mc_' + name + '.p'),'wb'), protocol=4)
    pickle.dump(grid_4mc, open(str('Data/grid_4mc_' + name + '.p'),'wb'), protocol=4)
    pickle.dump(grid_5mc, open(str('Data/grid_5mc_' + name + '.p'),'wb'), protocol=4)
    pickle.dump(total_visits, open(str('Data/grid_total_visits_' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(misalignment_user, open(str('Data/grid_misalignment_user' + name + '.p'),'wb'), protocol=4)
    pickle.dump(misalignment_bs, open(str('Data/grid_misalignment_bs' + name + '.p'),'wb'), protocol=4)
    pickle.dump(misalignment_mc, open(str('Data/grid_misalignment_mc' + name + '.p'),'wb'), protocol=4)
    pickle.dump(misalignment_sc, open(str('Data/grid_misalignment_sc' + name + '.p'),'wb'), protocol=4)
    pickle.dump(misalignment_2mc, open(str('Data/grid_misalignment_2mc' + name + '.p'),'wb'), protocol=4)
    pickle.dump(misalignment_3mc, open(str('Data/grid_misalignment_3mc' + name + '.p'),'wb'), protocol=4)
    pickle.dump(misalignment_4mc, open(str('Data/grid_misalignment_4mc' + name + '.p'),'wb'), protocol=4)
    pickle.dump(misalignment_5mc, open(str('Data/grid_misalignment_5mc' + name + '.p'),'wb'), protocol=4)

    pickle.dump(distances, open(str('Data/distances' + name + '.p'),'wb'), protocol=4)
    pickle.dump(distances_mc, open(str('Data/distances_mc' + name + '.p'),'wb'), protocol=4)
    pickle.dump(distances_sc, open(str('Data/distances_sc' + name + '.p'),'wb'), protocol=4)
    pickle.dump(distances_2mc, open(str('Data/distances_2mc' + name + '.p'),'wb'), protocol=4)
    pickle.dump(distances_3mc, open(str('Data/distances_3mc' + name + '.p'),'wb'), protocol=4)
    pickle.dump(distances_4mc, open(str('Data/distances_4mc' + name + '.p'),'wb'), protocol=4)
    pickle.dump(distances_5mc, open(str('Data/distances_5mc' + name + '.p'),'wb'), protocol=4)


    pickle.dump(total_links_per_user, open(str('Data/total_links_per_user' + name + '.p'),'wb'), protocol=4)
    pickle.dump(channel_capacity, open(str('Data/total_channel_capacity' + name + '.p'),'wb'), protocol=4)
    pickle.dump(no_optimal_value_found, open(str('Data/no_optimal_value_found' + name + '.p'),'wb'), protocol=4)


    print(str('Data/total_links_per_user' + name + '.p'))
    print('average channel capacity:', sum(channel_capacity)/len(channel_capacity))


if __name__ == "__main__":
    main()