import os
import pickle
import progressbar
import MCUAPA
import find_data
import functions as f
import get_data
from parameters import *


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

    name = str('HHO' + str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(
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
        powers = pickle.load(open(str('Data/power' + name + '.p'), 'rb'))

    else:
        optimal = []
        xs = []
        ys = []
        shares = []
        user_capacities = []
        satisfaction = []
        total_links_per_user = []
        powers = []

        bar = progressbar.ProgressBar(maxval=iteration_max, widgets=[
            progressbar.Bar('=', f'MCUA-PA, scenario: {scenario}, #users: {number_of_users} [', ']'), ' ',
            progressbar.Percentage(), ' ', progressbar.ETA()])
        bar.start()

        for iteration in range(iteration_min, iteration_max):
            bar.update(iteration)
            np.random.seed(iteration)
            x_user, y_user = f.find_coordinates(number_of_users, Clustered)

            opt_x, power_allocation, capacities = MCUAPA.do_algorithm(x_user, y_user, iteration)
            occupied_beams = find_occupied_beams(opt_x)
            share = opt_x

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
            powers.append(power_allocation)

        bar.finish()
    pickle.dump(optimal, open(str('Data/assignment' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(powers, open(str('Data/power' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(shares, open(str('Data/shares' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(xs, open(str('Data/xs' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(ys, open(str('Data/ys' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(user_capacities, open(str('Data/capacity_per_user' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(satisfaction, open(str('Data/satisfaction' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(total_links_per_user, open(str('Data/total_links_per_user' + name + '.p'), 'wb'), protocol=4)

    find_data.main(optimal, shares, xs, ys, satisfaction, Harris=True, Heuristic=False, Greedy=Greedy,
                   power=powers)

get_data.get_data(scenario, Harris=True)
