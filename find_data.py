import matplotlib.pyplot as plt
import numpy as np

import get_data
import simulate_blockers
from parameters import *
import new_optimization
import new_optimization
import functions as f


import time
import pickle
import os
import progressbar

Optimal = True
Blocked = True
Plotting = True


def main(optimal, shares, xs, ys, capacities, satisfaction, Heuristic=False, k = 1, SNRHeuristic = False, Clustered = False, User_Heuristic = False, GreedyHeuristic = False, GreedyRate = False, Iterative = False):

    delta = 1
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

    grid_bs = np.zeros((y_max, x_max))

    disconnected = []
    total_links_per_user = np.array([])
    channel_capacity = []
    cap_per_user = []

    channel_capacity_real = []
    channel_capacity_real_per_user = []
    satisfaction_blocked = []

    channel_capacity_SINR = []
    number_of_users = len(xs[0])

    iteration_min = 0
    iteration_max = iterations[number_of_users]

    bar = progressbar.ProgressBar(maxval=iteration_max, widgets=[progressbar.Bar('=', f'Finding data... scenario: {scenario}, #users: {number_of_users} [', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()])
    bar.start()
    for iteration in range(iteration_min, iteration_max):
        bar.update(iteration)
        np.random.seed(iteration)

        # x_user, y_user = f.find_coordinates(number_of_users)
        x_user, y_user = xs[iteration], ys[iteration]

        opt_x = optimal[iteration]
        share = shares[iteration]
        links_per_user = sum(np.transpose(opt_x))
        discon = 0

        total_links_per_user = np.append(total_links_per_user, links_per_user)
        capacity_per_user = f.find_capacity_per_user(share, x_user, y_user)

        blocked_connections = simulate_blockers.find_blocked_connections(opt_x, x_user, y_user, number_of_users)
        discon_blocked = 0

        for user in range(number_of_users):
            u = f.user_coords(user, x_user, y_user)
            if opt_x[user, bs_of_interest] == 1:
                grid_bs[int(u[1] * delta), int(u[0] * delta)] += 1

            if Plotting and links_per_user[user] == 1:
                grid_sc[int(u[1]*delta), int(u[0]*delta)] += 1
            elif links_per_user[user] == 0:
                discon += 1
            else:
                grid_mc[int(u[1]*delta), int(u[0]*delta)] += 1
            total_visits[int(u[1]*delta), int(u[0]*delta)] += 1

            # SINR_capacity_per_user = f.SINR_capacity_per_user(share, x_user, y_user)
            # channel_capacity_SINR.append(SINR_capacity_per_user)
            capacity = sum(capacities[iteration])
            channel_capacity.append(capacity)
            disconnected.append(discon)
            cap_per_user.append(capacity_per_user)

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

                    if f.find_snr(user, b, x_user, y_user, blocked_connections[user, b]) < SINR_min:
                        opt_x[user, b] = 0

        links_per_user = sum(np.transpose(opt_x))
        for user in range(number_of_users):
            if links_per_user[user] == 0:
                discon_blocked += 1

        channel_capacity_per_user = f.find_capacity_per_user(share, x_user, y_user, blocked_connections = blocked_connections)
        channel_capacity_real_per_user.append(channel_capacity_per_user)
        channel_capacity_real.append(sum(channel_capacity_per_user))
        satisfied = np.ones(number_of_users)
        for u in range(number_of_users):
            if channel_capacity_per_user[u] < user_rate:
                satisfied[u] = channel_capacity_per_user[u]/user_rate
        satisfaction_blocked.append(satisfied)


    bar.finish()
    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))

    if Heuristic:
        if User_Heuristic:
            name = str('beamwidth_user_heuristic' + name)
        else:
            name = str('beamwidth_heuristic' + name)
        if Iterative:
            name = str(name + '_Iterative')
    elif SNRHeuristic:
        name = str('SNR_k=' + str(k) + name)

    elif GreedyRate:
        name = str(name + 'GreedyRate')
    elif GreedyHeuristic:
        name = str(name + 'GreedyHeuristic')

    if Clustered:
        name = str(name + '_clustered')

    pickle.dump(grid_mc, open(str('Data/grid_mc_' + name + '.p'),'wb'), protocol=4)
    pickle.dump(grid_bs, open(str('Data/grid_bs_' + name + '.p'),'wb'), protocol=4)
    pickle.dump(total_visits, open(str('Data/grid_total_visits_' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(misalignment_user, open(str('Data/grid_misalignment_user' + name + '.p'),'wb'), protocol=4)
    pickle.dump(misalignment_bs, open(str('Data/grid_misalignment_bs' + name + '.p'),'wb'), protocol=4)
    pickle.dump(misalignment_mc, open(str('Data/grid_misalignment_mc' + name + '.p'),'wb'), protocol=4)

    # pickle.dump(distances, open(str('Data/distances' + name + '.p'),'wb'), protocol=4)
    pickle.dump(total_links_per_user, open(str('Data/total_links_per_user' + name + '.p'),'wb'), protocol=4)
    pickle.dump(channel_capacity, open(str('Data/channel_capacity' + name + '.p'),'wb'), protocol=4)
    pickle.dump(channel_capacity_SINR, open(str('Data/channel_capacity_SINR' + name + '.p'),'wb'), protocol=4)

    pickle.dump(cap_per_user, open(str('Data/capacity_per_user' + name + '.p'),'wb'), protocol=4)
    pickle.dump(disconnected, open(str('Data/disconnected_users' + name + '.p'),'wb'), protocol=4)
    pickle.dump(satisfaction, open(str('Data/satisfaction' + name + '.p'),'wb'), protocol=4)

    pickle.dump(satisfaction_blocked, open(str('Data/satisfaction_blocked' + name + '.p'),'wb'), protocol=4)
    pickle.dump(channel_capacity_real, open(str('Data/blocked_capacity' + name + '.p'),'wb'), protocol=4)
    pickle.dump(channel_capacity_real_per_user, open(str('Data/blocked_capacity_per_user' + name + '.p'),'wb'), protocol=4)

if __name__ == '__main__':
    for scenario in [7, 8, 9]: #range(1, 24):
        beamwidth_deg, users_per_beam, Penalty, Clustered = find_scenario(scenario)
        Heuristic = False
        SNRHeuristic = False
        User_Heuristic = False
        GreedyRate = False
        GreedyHeuristic = False
        Iterative = True

        beamwidth_b = np.radians(beamwidth_deg)
        for number_of_users in [100, 300, 500, 750, 1000]:
            if SNRHeuristic:
                k = int(input('k?'))
            else:
                k = 1
            iteration_max = iterations[number_of_users]
            name = str(
                str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(
                    M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))

            if Heuristic:
                if User_Heuristic:
                    name = str('beamwidth_user_heuristic' + name)
                else:
                    name = str('beamwidth_heuristic' + name)
                if Iterative:
                    name = str(name + '_Iterative')

            elif SNRHeuristic:
                name = str('SNR_k=' + str(k) + name)

            elif GreedyRate:
                name = str(name + 'GreedyRate')
            elif GreedyHeuristic:
                name = str(name + 'GreedyHeuristic')

            if Clustered:
                name = str(name + '_clustered')

            optimal = pickle.load(open(str('Data/assignment' + name  + '.p'),'rb'))
            shares = pickle.load(open(str('Data/shares' + name  + '.p'),'rb'))
            xs = pickle.load(open(str('Data/xs' + name + '.p'),'rb'))
            ys = pickle.load(open(str('Data/ys' + name + '.p'),'rb'))
            capacities = pickle.load(open(str('Data/capacity_per_user' + name + '.p'),'rb'))
            satisfaction = pickle.load(open(str('Data/satisfaction' + name + '.p'),'rb'))

            main(optimal, shares, xs, ys, capacities, satisfaction, Heuristic, k, SNRHeuristic, Clustered, User_Heuristic, GreedyHeuristic, GreedyRate, Iterative)