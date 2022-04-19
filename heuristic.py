import numpy as np
import find_data
from parameters import *
import functions as f
import pickle
import progressbar
import os
import matplotlib.pyplot as plt

User_Heuristic = False

def find_highest_snr(bs, x_user, y_user):
    snr = []
    for user in range(number_of_users):
        snr.append(-f.find_snr(user, bs, x_user, y_user))
    return np.argsort(snr), sorted(snr)

def find_distance(user, bs):
    x = np.minimum((user[0] - bs[0]) % xDelta, (bs[0] - user[0]) % xDelta)
    y = np.minimum((user[1] - bs[1]) % yDelta, (bs[1] - user[1]) % yDelta)
    return x ** 2 + y ** 2

def find_initial_association():
    opt_x = np.zeros((number_of_users, number_of_bs))
    occupied_beams = np.zeros((number_of_bs, len(directions_bs)))

    for bs in range(number_of_bs):
        users, snrs = find_highest_snr(bs, x_user, y_user)
        for user in users:
            user_coords = f.user_coords(user, x_user, y_user)
            snr = -snrs.pop(0)
            if snr > SINR_min:
                bs_coords = f.bs_coords(bs)
                geo = f.find_geo(bs_coords, user_coords)
                beam_number = f.find_beam_number(geo, beamwidth_b)
                if occupied_beams[bs, beam_number] < users_per_beam and abs(
                        f.find_misalignment(bs_coords, user_coords, beamwidth_b)) <= mis_threshold:
                    opt_x[user, bs] = 1
                    occupied_beams[bs, beam_number] += 1
    return opt_x, occupied_beams

def find_shares(opt_x, occupied_beams):
    share = np.zeros((number_of_users, number_of_bs))

    for user in range(number_of_users):
        for bs in range(number_of_bs):
            if opt_x[user, bs] == 1:
                bs_coords = f.bs_coords(bs)
                user_coords = f.user_coords(user, x_user, y_user)
                share[user, bs] = users_per_beam / occupied_beams[
                    bs, f.find_beam_number(f.find_geo(bs_coords, user_coords), beamwidth_b)]
    return share


for number_of_users in [100, 300, 500, 750, 1000]:
    iteration_min, iteration_max = 0, iterations[number_of_users]

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(M) + 's=' + str(users_per_beam) + '_heuristic')
    if User_Heuristic:
        name = str(name + '_users')

    if os.path.exists(str('Data/assignment' + name + '.p')) and 3 == 2:
        print('Data is already there')
        optimal = pickle.load(open(str('Data/assignment' + name + '.p'), 'rb'))
        shares = pickle.load(open(str('Data/shares' + name + '.p'), 'rb'))
        xs = pickle.load(open(str('Data/xs' + name + '.p'), 'rb'))
        ys = pickle.load(open(str('Data/ys' + name + '.p'), 'rb'))
        user_capacities = pickle.load(open(str('Data/capacity_per_user' + name + '.p'), 'rb'))
        satisfaction = pickle.load(open(str('Data/satisfaction' + name + '.p'), 'rb'))

    else:
        mis_threshold = misalignment[number_of_users]

        optimal = []
        xs = []
        ys = []
        shares = []
        user_capacities = []
        satisfaction = []

        bar = progressbar.ProgressBar(maxval=iteration_max, widgets=[progressbar.Bar('=', f'Scenario: {scenario}, #users: {number_of_users} [', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()])
        bar.start()

        for iteration in range(iteration_min, iteration_max):
            bar.update(iteration)
            np.random.seed(iteration)

            x_user, y_user = f.find_coordinates(number_of_users)

            opt_x, occupied_beams = find_initial_association()
            share = find_shares(opt_x, occupied_beams)

            capacities = f.find_capacity_per_user(share, x_user, y_user)
            satisfied = np.ones(number_of_users)

            for u in range(number_of_users):
                if capacities[u] < user_rate:
                    satisfied[u] = capacities[u]/user_rate

            links_per_user = sum(np.transpose(opt_x))

            optimal.append(opt_x)
            xs.append(x_user)
            ys.append(y_user)
            satisfaction.append(satisfied)
            shares.append(share)
            user_capacities.append(capacities)

        bar.finish()

    pickle.dump(optimal, open(str('Data/assignment' + name  + '.p'),'wb'), protocol=4)
    pickle.dump(shares, open(str('Data/shares' + name  + '.p'),'wb'), protocol=4)
    pickle.dump(xs, open(str('Data/xs' + name + '.p'),'wb'), protocol=4)
    pickle.dump(ys, open(str('Data/ys' + name + '.p'),'wb'), protocol=4)
    pickle.dump(user_capacities, open(str('Data/capacity_per_user' + name + '.p'),'wb'), protocol=4)
    pickle.dump(satisfaction, open(str('Data/satisfaction' + name + '.p'),'wb'), protocol=4)

    find_data.main(optimal, shares, xs, ys, user_capacities, satisfaction, Heuristic=True, Clustered=Clustered, User_Heuristic = User_Heuristic)

