import numpy as np
from parameters import *
import functions as f
import find_data
import progressbar
import os
import pickle
import get_data


def find_sorted_users(bs, x_user, y_user):
    # on a torus
    x = np.minimum((x_user - bs[0]) % xDelta, (bs[0] - x_user) % xDelta)
    y = np.minimum((y_user - bs[1]) % yDelta, (bs[1] - y_user) % yDelta)
    return np.argsort(x ** 2 + y ** 2)


def find_closest_snr(user, x_user, y_user):
    snr = []
    for bs in range(number_of_bs):
        snr.append(-f.find_snr(user, bs, x_user, y_user))
    return np.argsort(snr)


# user = int(input('Number of users?'))
for number_of_users in users:
    optimal = []
    xs = []
    ys = []
    satisfaction = []
    capacities = []
    shares = []

    iteration_min, iteration_max = 0, iterations[number_of_users]
    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(
        M) + 's=' + str(users_per_beam) + '_GreedyRate')

    if Clustered:
        name = str(name + '_clustered')
    if AT:
        name = str(name + 'rate' + str(rain_rate))

    if os.path.exists(str('Data/assignment' + name + '.p')):
        optimal = pickle.load(open(str('Data/assignment' + name + '.p'), 'rb'))
        shares = pickle.load(open(str('Data/shares' + name + '.p'), 'rb'))
        xs = pickle.load(open(str('Data/xs' + name + '.p'), 'rb'))
        ys = pickle.load(open(str('Data/ys' + name + '.p'), 'rb'))
        capacities = pickle.load(open(str('Data/capacity_per_user' + name + '.p'), 'rb'))
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

            for u in range(number_of_users):
                user_coords = f.user_coords(u, x_user, y_user)
                bs = list(find_closest_snr(u, x_user, y_user))
                rate = 0
                while rate <= user_rate and len(bs) > 0:
                    b = bs.pop(0)
                    snr = f.find_snr(u, b, x_user, y_user)
                    if snr > SINR_min:
                        bs_coords = f.bs_coords(b)
                        geo = f.find_geo(bs_coords, user_coords)
                        beam_number = f.find_beam_number(geo, beamwidth_b)
                        if occupied_beams[b, beam_number] < users_per_beam:
                            opt_x[u, bs] = 1
                            occupied_beams[bs, beam_number] += 1
                            rate += W / users_per_beam * math.log2(1 + snr)

            share = np.zeros((number_of_users, number_of_bs))
            for user in range(number_of_users):
                user_coords = f.user_coords(user, x_user, y_user)
                for bs in range(number_of_bs):
                    if opt_x[user, bs] == 1:
                        bs_coords = f.bs_coords(bs)
                        share[user, bs] = users_per_beam / occupied_beams[
                            bs, f.find_beam_number(f.find_geo(bs_coords, user_coords),
                                                   beamwidth_b)]

            links_per_user = sum(np.transpose(opt_x))
            capacity = f.find_capacity_per_user(share, x_user, y_user)

            satisfied = np.ones(number_of_users)

            for u in range(number_of_users):
                if capacity[u] < user_rate:
                    satisfied[u] = capacity[u] / user_rate

            optimal.append(opt_x)
            xs.append(x_user)
            ys.append(y_user)
            capacities.append(capacity)
            shares.append(share)
            satisfaction.append(satisfied)

        bar.finish()

        pickle.dump(optimal, open(str('Data/assignment' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(shares, open(str('Data/shares' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(xs, open(str('Data/xs' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(ys, open(str('Data/ys' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(capacities, open(str('Data/capacity_per_user' + name + '.p'), 'wb'), protocol=4)

    find_data.main(optimal, shares, xs, ys, capacities, satisfaction, GreedyRate=True, Clustered=Clustered, AT=AT,
                   rain_rate=rain_rate)
get_data.get_data(scenario, user_rate, GreedyRate=True)
