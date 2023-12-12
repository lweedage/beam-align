import os
import pickle

import progressbar

import find_data
import functions as f
import get_data
from parameters import *


# k = int(input('k ='))
def find_highest_snr(bs, x_user, y_user):
    snr = []
    for user in range(number_of_users):
        snr.append(-f.find_snr(user, bs, x_user, y_user))
    return np.argsort(snr), sorted(snr)


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


def find_sorted_users(bs, x_user, y_user):
    # on a torus
    x = np.minimum((x_user - bs[0]) % xDelta, (bs[0] - x_user) % xDelta)
    y = np.minimum((y_user - bs[1]) % yDelta, (bs[1] - y_user) % yDelta)
    return np.argsort(x ** 2 + y ** 2)


def find_closest(user):
    x = np.minimum((x_bs - user[0]) % xDelta, (user[0] - x_bs) % xDelta)
    y = np.minimum((y_bs - user[1]) % yDelta, (user[1] - y_bs) % yDelta)
    return np.argsort(x ** 2 + y ** 2)[:k]


def find_closest_snr(user, x_user, y_user):
    snr = []
    for bs in range(number_of_bs):
        snr.append(-f.find_snr(user, bs, x_user, y_user))
    return np.argsort(snr)


# for k in np.arange(1, 16, 1):
for number_of_users in users:
    optimal = []
    xs = []
    ys = []
    satisfaction = []
    capacities = []
    shares = []
    total_links_per_user = []

    iteration_min, iteration_max = 0, iterations[number_of_users]

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(
        beamwidth_b) + 'M=' + str(M) + 'k=' + str(max_connections) + 'active_beams=' + str(
        number_of_active_beams) + '_SNRheuristic')

    if Clustered:
        name = str(name + '_clustered')

    if os.path.exists(str('Data/capacity_per_user' + name + '.p')):
        print('Data is already there')
        optimal = pickle.load(open(str('Data/assignment' + name + '.p'), 'rb'))
        shares = pickle.load(open(str('Data/shares' + name + '.p'), 'rb'))
        xs = pickle.load(open(str('Data/xs' + name + '.p'), 'rb'))
        ys = pickle.load(open(str('Data/ys' + name + '.p'), 'rb'))
        capacities = pickle.load(open(str('Data/capacity_per_user' + name + '.p'), 'rb'))
        satisfaction = pickle.load(open(str('Data/satisfaction' + name + '.p'), 'rb'))
        total_links_per_user = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
        print(name)
    else:
        bar = progressbar.ProgressBar(maxval=iteration_max, widgets=[
            progressbar.Bar('=', f'Scenario: {scenario}, #users: {number_of_users} [', ']'), ' ',
            progressbar.Percentage(), ' ', progressbar.ETA()])
        bar.start()
        for iteration in range(iteration_min, iteration_max):
            bar.update(iteration)
            opt_x = np.zeros((number_of_users, number_of_bs))
            np.random.seed(iteration)
            x_user, y_user = f.find_coordinates(number_of_users, Clustered)

            occupied_beams = np.zeros((number_of_bs, len(directions_bs)))
            active_beams = {b: set() for b in range(number_of_bs)}
            connections = np.zeros(number_of_users)

            for user in range(number_of_users):
                bss = list(find_closest_snr(user, x_user, y_user))
                while connections[user] < max_connections and len(bss) > 0:
                    bs = bss.pop(0)
                    snr = f.find_snr(user, bs, x_user, y_user)
                    if snr > SINR_min:
                        bs_coords = f.bs_coords(bs)
                        user_coords = f.user_coords(user, x_user, y_user)
                        geo = f.find_geo(bs_coords, user_coords)
                        beam_number = f.find_beam_number(geo, beamwidth_b)
                        if connections[user] < max_connections and len(active_beams[bs] | {beam_number}) <= number_of_active_beams:
                            opt_x[user, bs] = 1
                            active_beams[bs].add(beam_number)
                            occupied_beams[bs, beam_number] += 1
                            connections[user] += 1

            share = find_shares(opt_x, occupied_beams)

            capacity = f.find_capacity_per_user(share, x_user, y_user)
            satisfied = np.ones(number_of_users)

            for u in range(number_of_users):
                if capacity[u] < user_rate:
                    satisfied[u] = capacity[u] / user_rate

            links_per_user = sum(np.transpose(opt_x))

            optimal.append(opt_x)
            xs.append(x_user)
            ys.append(y_user)
            capacities.append(capacity)
            shares.append(share)
            satisfaction.append(satisfied)
            total_links_per_user.append(links_per_user)

        bar.finish()
        pickle.dump(optimal, open(str('Data/assignment' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(shares, open(str('Data/shares' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(xs, open(str('Data/xs' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(ys, open(str('Data/ys' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(capacities, open(str('Data/capacity_per_user' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(satisfaction, open(str('Data/satisfaction' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(total_links_per_user, open(str('Data/total_links_per_user' + name + '.p'), 'wb'), protocol=4)
        print(name)
    find_data.main(optimal, shares, xs, ys, satisfaction, Heuristic=False, SNRHeuristic=True)
get_data.get_data(scenario, Heuristic=False, SNRHeuristic=True)
