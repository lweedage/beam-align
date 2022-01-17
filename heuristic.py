import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import functions as f
import time
import pickle

if Interference:
    name = str('beamwidth_heuristic_with_interference_users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)))
else:
    name = str('beamwidth_heuristic_users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)))


misalignment = {3: 1.8, 100: 1.78, 300: 1.60, 500: 1.47}

def find_sorted_users(bs, x_user, y_user):
    xx = x_user - bs[0]
    yy = y_user - bs[1]
    return np.argsort(np.sqrt(xx ** 2 + yy ** 2))


def find_closest(bs):
    users = []
    possible_directions = list(directions_bs)
    bs_coords = f.bs_coords(bs)
    sorted_users = find_sorted_users(bs_coords, x_user, y_user)
    for u in sorted_users:
        user_coord = f.user_coords(u, x_user, y_user)
        beam_number = f.find_beam_number(f.find_beam(f.find_geo(bs_coords, user_coord), beamwidth_b), beamwidth_b)
        if abs(np.degrees(f.find_misalignment(bs_coords, user_coord, beamwidth_b))) <= misalignment[
            number_of_users] and beam_number in possible_directions:
            possible_directions.remove(beam_number)
            users.append(u)
    return users

start = time.time()
iteration_min, iteration_max = 0, 5000

for iteration in range(iteration_min, iteration_max):
    opt_x = np.zeros((number_of_users, number_of_bs))
    print('Iteration ', iteration)
    np.random.seed(iteration)
    x_user, y_user = f.find_coordinates()

    for bs in range(number_of_bs):
        u = find_closest(bs)
        if u is not None:
            for user in u:
                opt_x[user, bs] = 1

    pickle.dump(opt_x, open(str('Data/opt_x_heuristics/iteration_' + str(iteration) + name + '.p'), 'wb'), protocol=4)

    # print('one iteration takes', time.time() - start, 'seconds')
    # start = time.time()

# fig, ax = plt.subplots()
# G, colorlist, nodesize, edgesize, labels, edgecolor = f.make_graph(x_bs, y_bs, x_user, y_user, opt_x, number_of_users)
# f.draw_graph(G, colorlist, nodesize, edgesize, labels, ax, color = 'black', edgecolor = edgecolor)
#
# plt.show()
#
# links_per_user = sum(np.transpose(opt_x))
#
# fig, ax = plt.subplots()
# plt.hist(links_per_user, density=True)
# plt.show()