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


def find_measures(optimal, number_of_users, x_user, y_user, blocked_connections, AT, rain_rate):
    opt_x = np.zeros((number_of_users, number_of_bs))
    occupied_beams = np.zeros((number_of_bs, len(directions_bs)))
    share = np.zeros((number_of_users, number_of_bs))

    for user in range(number_of_users):
        u = f.user_coords(user, x_user, y_user)
        for b in range(number_of_bs):
            if optimal[user, b] == 1:
                b_coords = f.bs_coords(b)
                if f.find_snr(user, b, x_user, y_user, blocked_connections[user, b], AT, rain_rate) > SINR_min:
                    opt_x[user, b] = 1
                    occupied_beams[b, f.find_beam_number(f.find_geo(b_coords, u), beamwidth_b)] += 1

    for user in range(number_of_users):
        user_coords = f.user_coords(user, x_user, y_user)
        for bs in range(number_of_bs):
            if opt_x[user, bs] == 1:
                bs_coords = f.bs_coords(bs)
                share[user, bs] = users_per_beam / occupied_beams[
                    bs, f.find_beam_number(f.find_geo(bs_coords, user_coords), beamwidth_b)]

    capacity = f.find_capacity_per_user(share, x_user, y_user, blocked_connections, AT, rain_rate)
    satisfaction = np.ones(number_of_users)

    for u in range(number_of_users):
        if capacity[u] < user_rate:
            satisfaction[u] = capacity[u] / user_rate

    return capacity, satisfaction


def main(optimal, shares, xs, ys, satisfaction, Heuristic=False, k=1, SNRHeuristic=False, GreedyRate=False):
    misalignment_user = []
    misalignment_bs = []

    total_links_per_user = np.array([])
    capacity_per_user = np.array([])

    capacity_blocked = np.array([])
    satisfaction_blocked = []

    capacity_2_5 = np.array([])
    satisfaction_2_5 = []

    capacity_25 = np.array([])
    satisfaction_25 = []

    capacity_150 = np.array([])
    satisfaction_150 = []

    # channel_capacity_SINR = []
    number_of_users = len(xs[0])

    iteration_min = 0
    iteration_max = iterations[number_of_users]

    bar = progressbar.ProgressBar(maxval=iteration_max, widgets=[
        progressbar.Bar('=', f'Finding data... scenario: {scenario}, #users: {number_of_users} [', ']'), ' ',
        progressbar.Percentage(), ' ', progressbar.ETA()])
    bar.start()
    for iteration in range(iteration_min, iteration_max):
        bar.update(iteration)
        np.random.seed(iteration)
        x_user, y_user = xs[iteration], ys[iteration]

        opt_x = optimal[iteration]
        share = shares[iteration]
        links_per_user = sum(np.transpose(opt_x))

        total_links_per_user = np.append(total_links_per_user, links_per_user)
        capacity_per_user = np.append(capacity_per_user, f.find_capacity_per_user(share, x_user, y_user))
        # SINR_capacity_per_user = f.SINR_capacity_per_user(share, x_user, y_user)
        # channel_capacity_SINR.append(SINR_capacity_per_user)
        for user in range(number_of_users):
            u = f.user_coords(user, x_user, y_user)
            for b in range(number_of_bs):
                if opt_x[user, b] == 1:
                    b_coords = f.bs_coords(b)
                    misalignment_user.append(f.find_misalignment(u, b_coords, beamwidth_u))
                    misalignment_bs.append(f.find_misalignment(b_coords, u, beamwidth_b))

        blocked_connections = simulate_blockers.find_blocked_connections(opt_x, x_user, y_user, number_of_users)
        cap_blocked, sat_blocked = find_measures(opt_x, number_of_users, x_user, y_user, blocked_connections, AT=False,
                                                 rain_rate=0)
        blocked_connections = np.zeros((number_of_users, number_of_bs))
        cap_2_5, sat_2_5 = find_measures(opt_x, number_of_users, x_user, y_user, blocked_connections, AT=True,
                                         rain_rate=2.5)
        cap_25, sat_25 = find_measures(opt_x, number_of_users, x_user, y_user, blocked_connections, AT=True,
                                       rain_rate=25)
        cap_150, sat_150 = find_measures(opt_x, number_of_users, x_user, y_user, blocked_connections, AT=True,
                                         rain_rate=150)

        capacity_blocked = np.append(capacity_blocked, cap_blocked)
        satisfaction_blocked.append(sat_blocked)
        capacity_2_5 = np.append(capacity_2_5, cap_2_5)
        satisfaction_2_5.append(sat_2_5)
        capacity_25 = np.append(capacity_25, cap_25)
        satisfaction_25.append(sat_25)
        capacity_150 = np.append(capacity_150, cap_150)
        satisfaction_150.append(sat_150)

    bar.finish()
    name = find_name(iteration_max, number_of_users, Heuristic, SNRHeuristic, GreedyRate, k)

    pickle.dump(misalignment_bs, open(str('Data/grid_misalignment_bs' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(misalignment_user, open(str('Data/grid_misalignment_user' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(total_links_per_user, open(str('Data/total_links_per_user' + name + '.p'), 'wb'), protocol=4)
    # pickle.dump(channel_capacity_SINR, open(str('Data/channel_capacity_SINR' + name + '.p'),'wb'), protocol=4)

    pickle.dump(capacity_per_user, open(str('Data/capacity' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(satisfaction, open(str('Data/satisfaction' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(satisfaction_blocked, open(str('Data/satisfaction_blocked' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(capacity_blocked, open(str('Data/capacity_blocked' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(satisfaction_2_5, open(str('Data/satisfaction_2_5' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(capacity_2_5, open(str('Data/capacity_2_5' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(satisfaction_25, open(str('Data/satisfaction_25' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(capacity_25, open(str('Data/capacity_25' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(satisfaction_150, open(str('Data/satisfaction_150' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(capacity_150, open(str('Data/capacity_150' + name + '.p'), 'wb'), protocol=4)
