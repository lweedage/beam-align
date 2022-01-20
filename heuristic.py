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

# number_of_bs = 1
# x_bs, y_bs = [10], [10]

misalignment = {100: 1.78, 300: 1.60, 500: 1.47, 750:1.34}

def find_sorted_users(bs, x_user, y_user):
    # on a torus
    x = np.minimum((x_user - bs[0]) % xDelta, (bs[0] - x_user) % xDelta)
    y = np.minimum((y_user - bs[1]) % yDelta, (bs[1] - y_user) % yDelta)
    return np.argsort(np.sqrt(x ** 2 + y ** 2))

def find_distance(user, bs):
    x = np.minimum((user[0] - bs[0]) % xDelta, (bs[0] - user[0]) % xDelta)
    y = np.minimum((user[1] - bs[1]) % yDelta, (bs[1] - user[1]) % yDelta)
    return x ** 2 + y ** 2

def find_closest(bs):
    users = []
    possible_directions = list(directions_bs)
    bs_coords = f.bs_coords(bs)
    sorted_users = find_sorted_users(bs_coords, x_user, y_user)
    for u in sorted_users:
        user_coord = f.user_coords(u, x_user, y_user)
        geo = f.find_geo(bs_coords, user_coord)
        beam = f.find_beam(geo, beamwidth_b)
        beam_number = f.find_beam_number(beam, beamwidth_b)
        if abs(np.degrees(beam - geo)) <= misalignment[number_of_users] and beam_number in possible_directions:
            possible_directions.remove(beam_number)
            users.append(u)
    return users

start = time.time()
iteration_min, iteration_max = 0, iterations[number_of_users]
failed_link_constraints = []
failed_sinr_constraints = []

for iteration in range(iteration_min, iteration_max):
    opt_x = np.zeros((number_of_users, number_of_bs))
    print('Iteration ', iteration)
    np.random.seed(iteration)
    x_user, y_user = f.find_coordinates()


    for bs in range(number_of_bs):
        bs_coords = f.bs_coords(bs)
        candidate = dict()
        for user in range(number_of_users):
            user_coords = f.user_coords(user, x_user, y_user)
            geo = f.find_geo(bs_coords, user_coords)
            beam = f.find_beam(geo, beamwidth_b)
            if np.degrees(abs(geo - beam)) <= misalignment[number_of_users]:
                if beam in candidate.keys():
                    if find_distance(bs_coords, user_coords) < find_distance(bs_coords, f.user_coords(candidate[beam], x_user, y_user)):
                        candidate[beam] = user
                else:
                    candidate[beam] = user
        for user in candidate.values():
            opt_x[user, bs] = 1

    link_constraint_fails = 0
    sinr_constraint_fails = 0
    links_per_user = sum(np.transpose(opt_x))

    for u in range(number_of_users):
        if links_per_user[u] == 0:
            link_constraint_fails += 1
        for bs in range(number_of_bs):
            if opt_x[u, bs] == 1:
                sinr = f.find_sinr(u, bs, opt_x, x_user, y_user)
                if sinr < SINR_min:
                    sinr_constraint_fails += 1


    pickle.dump(opt_x, open(str('Data/opt_x_heuristics/iteration_' + str(iteration) + name + '.p'), 'wb'), protocol=4)
    failed_link_constraints.append(link_constraint_fails)
    failed_sinr_constraints.append(sinr_constraint_fails)

    # print('one iteration takes', time.time() - start, 'seconds')
    # start = time.time()

pickle.dump(failed_link_constraints, open(str('Data/failed_link_constraints_iteration_' + str(iteration_max) + name + '.p'), 'wb'), protocol=4)
pickle.dump(failed_sinr_constraints, open(str('Data/failed_sinr_constraints_iteration_' + str(iteration_max) + name + '.p'), 'wb'), protocol=4)


fig, ax = plt.subplots()
G, colorlist, nodesize, edgesize, labels, edgecolor = f.make_graph(x_bs, y_bs, x_user, y_user, opt_x, number_of_users)
f.draw_graph(G, colorlist, nodesize, edgesize, labels, ax, color = 'black', edgecolor = edgecolor)
plt.show()

links_per_user = sum(np.transpose(opt_x))

# fig, ax = plt.subplots()
# plt.hist(links_per_user, density=True)
# plt.show()

# print(x_bs, y_bs)
# print(x_user, y_user)