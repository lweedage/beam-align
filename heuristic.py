import numpy as np
import find_data
from parameters import *
import functions as f
import pickle
import progressbar
from time import sleep
import os

User_Heuristic = True

def find_sorted_users(bs, x_user, y_user):
    # on a torus
    x = np.minimum((x_user - bs[0]) % xDelta, (bs[0] - x_user) % xDelta)
    y = np.minimum((y_user - bs[1]) % yDelta, (bs[1] - y_user) % yDelta)
    return np.argsort(np.sqrt(x ** 2 + y ** 2))


def find_distance(user, bs):
    x = np.minimum((user[0] - bs[0]) % xDelta, (bs[0] - user[0]) % xDelta)
    y = np.minimum((user[1] - bs[1]) % yDelta, (bs[1] - user[1]) % yDelta)
    return x ** 2 + y ** 2

for number_of_users in [100, 300, 500, 750, 1000]:
    iteration_min, iteration_max = 0, iterations[number_of_users]

    name = str('users=' + str(number_of_users) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)) + 'M=' + str(M) + 's=' + str(users_per_beam) + '_heuristic')
    if User_Heuristic:
        name = str(name + '_users')


    if os.path.exists(str('Data/assignment' + name + '.p')):
        optimal = pickle.load(open(str('Data/assignment' + name + '.p'), 'rb'))
        shares = pickle.load(open(str('Data/shares' + name + '.p'), 'rb'))
        xs = pickle.load(open(str('Data/xs' + name + '.p'), 'rb'))
        ys = pickle.load(open(str('Data/ys' + name + '.p'), 'rb'))
        user_capacities = pickle.load(open(str('Data/capacity_per_user' + name + '.p'), 'rb'))
    else:
        if User_Heuristic:
            mis_threshold = user_misalignment[number_of_users]
        else:
            mis_threshold = misalignment[number_of_users]

        optimal = []
        xs = []
        ys = []
        disconnected = []
        shares = []
        user_capacities = []

        bar = progressbar.ProgressBar(maxval=iteration_max, widgets=[progressbar.Bar('=', f'Scenario: {scenario}, #users: {number_of_users} [', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()])
        bar.start()
        for iteration in range(iteration_min, iteration_max):
            bar.update(iteration)
            np.random.seed(iteration)
            opt_x = np.zeros((number_of_users, number_of_bs))
            # print('Iteration ', iteration)
            x_user, y_user = f.find_coordinates(number_of_users)

            occupied_beams = np.zeros((number_of_bs, len(directions_bs)))

            for bs in range(number_of_bs):
                bs_coords = f.bs_coords(bs)
                users = np.argsort(find_sorted_users(bs_coords, x_user, y_user)) # or maybe sort users by highest SNR?
                for user in users:
                    user_coords = f.user_coords(user, x_user, y_user)
                    snr = f.find_snr(user, bs, x_user, y_user)
                    if snr > SINR_min:
                        geo = f.find_geo(bs_coords, user_coords)
                        beam_number = f.find_beam_number(geo, beamwidth_b)
                        if occupied_beams[bs, beam_number] < users_per_beam and f.find_misalignment(bs_coords, user_coords, beamwidth_b) <= mis_threshold:
                            opt_x[user, bs] = 1
                            occupied_beams[bs, beam_number] += 1

            disconnected_user = 0
            links_per_user = sum(np.transpose(opt_x))

            share = np.zeros((number_of_users, number_of_bs))

            for user in range(number_of_users):
                for bs in range(number_of_bs):
                    if opt_x[user, bs] == 1:
                        bs_coords = f.bs_coords(bs)
                        user_coords = f.user_coords(user, x_user, y_user)
                        share[user, bs] = occupied_beams[bs, f.find_beam_number(f.find_geo(bs_coords, user_coords), beamwidth_b)] / users_per_beam

            for u in range(number_of_users):
                if links_per_user[u] == 0:
                    disconnected_user += 1

            optimal.append(opt_x)
            xs.append(x_user)
            ys.append(y_user)
            disconnected.append(disconnected_user)
            shares.append(share)
            user_capacities.append(f.find_capacity_per_user(opt_x, x_user, y_user, np.zeros((number_of_users, number_of_bs))))
        bar.finish()


    pickle.dump(optimal, open(str('Data/assignment' + name  + '.p'),'wb'), protocol=4)
    pickle.dump(shares, open(str('Data/shares' + name  + '.p'),'wb'), protocol=4)
    pickle.dump(xs, open(str('Data/xs' + name + '.p'),'wb'), protocol=4)
    pickle.dump(ys, open(str('Data/ys' + name + '.p'),'wb'), protocol=4)
    pickle.dump(user_capacities, open(str('Data/capacity_per_user' + name + '.p'),'wb'), protocol=4)

    find_data.main(optimal, shares, xs, ys, user_capacities, Heuristic=True, Clustered=Clustered, User_Heuristic = User_Heuristic)

