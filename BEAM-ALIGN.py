import os
import pickle

import progressbar

import find_data
import functions as f
import get_data
from parameters import *

def find_highest_snr(bs, x_user, y_user):
    snr = []
    for user in range(number_of_users):
        snr.append(-f.find_snr(user, bs, x_user, y_user))
    return np.argsort(snr), sorted(snr)


def find_highest_sinr(bs, x_user, y_user):
    opt_x = np.ones((number_of_users, number_of_bs))
    sinr = []
    for user in range(number_of_users):
        sinr.append(-f.find_sinr(opt_x, user, bs, x_user, y_user))
    return np.argsort(sinr), sorted(sinr)


def find_highest_snr_user(user, x_user, y_user):
    snr = []
    for bs in range(number_of_bs):
        snr.append(-f.find_snr(user, bs, x_user, y_user))
    return np.argsort(snr), sorted(snr)


def find_distance(user, bs):
    x = np.minimum((user[0] - bs[0]) % xDelta, (bs[0] - user[0]) % xDelta)
    y = np.minimum((user[1] - bs[1]) % yDelta, (bs[1] - user[1]) % yDelta)
    return x ** 2 + y ** 2


def find_initial_association():
    opt_x = np.zeros((number_of_users, number_of_bs))
    occupied_beams = np.zeros((number_of_bs, len(directions_bs)))
    active_beams = {b: set() for b in range(number_of_bs)}
    connections = np.zeros(number_of_users)

    for bs in range(number_of_bs):
        users, snrs = find_highest_snr(bs, x_user, y_user)
        for user in users:
            snr = -snrs.pop(0)
            user_coords = f.user_coords(user, x_user, y_user)
            if snr > SINR_min:
                bs_coords = f.bs_coords(bs)
                geo = f.find_geo(bs_coords, user_coords)
                beam_number = f.find_beam_number(geo, beamwidth_b)
                if (connections[user] < max_connections and len(active_beams[bs] | {beam_number}) <= number_of_active_beams
                        and abs(f.find_misalignment(bs_coords, user_coords, beamwidth_b)) <= mis_threshold):
                    opt_x[user, bs] = 1
                    active_beams[bs].add(beam_number)
                    occupied_beams[bs, beam_number] += 1
                    connections[user] += 1
    return opt_x, occupied_beams


def find_shares(opt_x, occupied_beams):
    share = np.zeros((number_of_users, number_of_bs))

    for user in range(number_of_users):
        for bs in range(number_of_bs):
            if opt_x[user, bs] == 1:
                bs_coords = f.bs_coords(bs)
                user_coords = f.user_coords(user, x_user, y_user)
                share[user, bs] = 1 / occupied_beams[
                    bs, f.find_beam_number(f.find_geo(bs_coords, user_coords), beamwidth_b)]
    return share


def find_occupied_beams(opt_x):
    occupied_beams = np.zeros((number_of_bs, len(directions_bs)))
    for bs in range(number_of_bs):
        for user in range(number_of_users):
            if opt_x[user, bs] > 0:
                user_coords = f.user_coords(user, x_user, y_user)
                bs_coords = f.bs_coords(bs)
                geo = f.find_geo(bs_coords, user_coords)
                beam_number = f.find_beam_number(geo, beamwidth_b)
                occupied_beams[bs, beam_number] += 1
    return occupied_beams


for number_of_users in users:
    iteration_min, iteration_max = 0, iterations[number_of_users]

    name = str('beamwidth_heuristic' + str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(
        beamwidth_b) + 'M=' + str(M) + 'k=' + str(max_connections) + 'active_beams=' + str(number_of_active_beams))

    if Clustered:
        name = str(name + '_clustered')

    if os.path.exists(str('Data/assignment' + name + '.p')):
        print('Data is already there')
        optimal = pickle.load(open(str('Data/assignment' + name + '.p'), 'rb'))
        shares = pickle.load(open(str('Data/shares' + name + '.p'), 'rb'))
        xs = pickle.load(open(str('Data/xs' + name + '.p'), 'rb'))
        ys = pickle.load(open(str('Data/ys' + name + '.p'), 'rb'))
        user_capacities = pickle.load(open(str('Data/capacity_per_user' + name + '.p'), 'rb'))
        satisfaction = pickle.load(open(str('Data/satisfaction' + name + '.p'), 'rb'))
        total_links_per_user = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))

    else:
        mis_threshold = misalignment[number_of_users]
        user_threshold = misalignment_user[number_of_users]

        optimal = []
        xs = []
        ys = []
        shares = []
        user_capacities = []
        satisfaction = []
        total_links_per_user = []

        bar = progressbar.ProgressBar(maxval=iteration_max, widgets=[
            progressbar.Bar('=', f'Scenario: {scenario}, #users: {number_of_users} [', ']'), ' ',
            progressbar.Percentage(), ' ', progressbar.ETA()])
        bar.start()

        for iteration in range(iteration_min, iteration_max):
            bar.update(iteration)
            np.random.seed(iteration)

            x_user, y_user = f.find_coordinates(number_of_users, Clustered)

            opt_x, occupied_beams = find_initial_association()
            share = find_shares(opt_x, occupied_beams)

            capacities = f.find_capacity_per_user(share, x_user, y_user)
            satisfied = np.ones(number_of_users)

            for u in range(number_of_users):
                if capacities[u] < user_rate:
                    satisfied[u] = capacities[u] / user_rate

            links_per_user = sum(np.transpose(opt_x))

            optimal.append(opt_x)
            xs.append(x_user)
            ys.append(y_user)
            satisfaction.append(satisfied)
            shares.append(share)
            user_capacities.append(capacities)
            total_links_per_user.append(links_per_user)

        bar.finish()

    pickle.dump(optimal, open(str('Data/assignment' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(shares, open(str('Data/shares' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(xs, open(str('Data/xs' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(ys, open(str('Data/ys' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(user_capacities, open(str('Data/capacity_per_user' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(satisfaction, open(str('Data/satisfaction' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(total_links_per_user, open(str('Data/total_links_per_user' + name + '.p'), 'wb'), protocol=4)

    find_data.main(optimal, shares, xs, ys, satisfaction, Heuristic=True)

get_data.get_data(scenario, Heuristic=True)
