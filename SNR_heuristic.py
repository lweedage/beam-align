import numpy as np
from parameters import *
import functions as f
import find_data

# k = int(input('k ='))


def find_sorted_users(bs, x_user, y_user):
    # on a torus
    x = np.minimum((x_user - bs[0]) % xDelta, (bs[0] - x_user) % xDelta)
    y = np.minimum((y_user - bs[1]) % yDelta, (bs[1] - y_user) % yDelta)
    return np.argsort(x ** 2 + y ** 2)

def find_closest(user):
    x = np.minimum((x_bs - user[0]) % xDelta, (user[0] - x_bs) % xDelta)
    y = np.minimum((y_bs - user[1]) % yDelta, (user[1] - y_bs) % yDelta)
    return np.argsort(x**2 + y**2)[:k]

def find_closest_snr(user, x_user, y_user):
    snr = []
    for bs in range(number_of_bs):
        snr.append(f.find_snr(user, bs, x_user, y_user))
    return np.argsort(snr)

# user = int(input('Number of users?'))
for number_of_users in [100, 300, 500, 750, 1000]:
    for k in [1, 5]:
        optimal = []
        xs = []
        ys = []
        disconnected = []
        capacities = []
        shares = []

        iteration_min, iteration_max = 0, iterations[number_of_users]

        for iteration in range(iteration_min, iteration_max):
            opt_x = np.zeros((number_of_users, number_of_bs))
            print('Iteration ', iteration)
            np.random.seed(iteration)
            x_user, y_user = f.find_coordinates(number_of_users)

            occupied_beams = np.zeros((number_of_bs, len(directions_bs)))

            for u in range(number_of_users):
                user_coords = f.user_coords(u, x_user, y_user)
                bs = list(find_closest_snr(u, x_user, y_user))
                while sum(np.transpose(opt_x))[u] < k and len(bs) > 0:
                    b = bs.pop(0)
                    snr = f.find_snr(u, b,  x_user, y_user)
                    if snr > SINR_min:
                        bs_coords = f.bs_coords(b)
                        geo = f.find_geo(bs_coords, user_coords)
                        beam_number = f.find_beam_number(geo, beamwidth_b)
                        opt_x[u, bs] = 1
                        occupied_beams[bs, beam_number] += 1

            share = np.zeros((number_of_users, number_of_bs))
            for user in range(number_of_users):
                for bs in range(number_of_bs):
                    share[user, bs] = occupied_beams[bs, f.find_beam_number(f.find_geo(bs_coords, user_coords),
                                                                    beamwidth_b)] / users_per_beam

            links_per_user = sum(np.transpose(opt_x))



            capacity = f.find_capacity_per_user(opt_x, x_user, y_user, np.zeros((number_of_users, number_of_bs)))

            optimal.append(opt_x)
            xs.append(x_user)
            ys.append(y_user)
            capacities.append(capacity)
            shares.append(share)

        find_data.main(optimal, shares,  xs, ys, capacities, SNRHeuristic = True, k = k)