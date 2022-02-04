import matplotlib.pyplot as plt
import numpy as np

import find_data
from parameters import *
import new_optimization
import functions as f
import time
import pickle

bandwidth_sharing = False

for number_of_users in [100, 300, 500, 750, 1000]:
    for User_Beamforming in [True]:
        name = str('beamwidth_heuristic_users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)))

        # number_of_bs = 1
        # x_bs, y_bs = [10], [10]

        # bandwidth_sharing = True

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

        optimal = []
        xs = []
        ys = []

        for iteration in range(iteration_min, iteration_max):
            opt_x = np.zeros((number_of_users, number_of_bs))
            print('Iteration ', iteration)
            x_user, y_user = f.find_coordinates(number_of_users)

            occupied_beams = np.zeros((number_of_bs, len(directions_bs)))
            candidate_user_beams = [dict() for i in range(number_of_users)]
            for bs in range(number_of_bs):
                bs_coords = f.bs_coords(bs)
                candidate = dict()
                for user in range(number_of_users):
                    user_coords = f.user_coords(user, x_user, y_user)

                    geo = f.find_geo(bs_coords, user_coords)
                    beam = f.find_beam(geo, beamwidth_b)
                    beam_number = f.find_beam_number(geo, beamwidth_b)

                    geo_user = f.find_geo(user_coords, bs_coords)
                    user_beam = f.find_beam(geo_user, beamwidth_u)
                    beam_number_user = f.find_beam_number(geo_user, beamwidth_u)

                    if np.degrees(abs(geo - beam)) <= misalignment[number_of_users]:
                        snr = f.find_snr(user, bs, x_user, y_user)
                        if snr >= SINR_min:
                            if beam_number in candidate.keys():
                                if find_distance(bs_coords, user_coords) < find_distance(bs_coords, f.user_coords(candidate[beam_number], x_user, y_user)):
                                     candidate[beam_number] = user
                                     if User_Beamforming:
                                        if  beam_number_user in candidate_user_beams[user].keys():
                                            if find_distance(bs_coords, user_coords) < find_distance(f.bs_coords(candidate_user_beams[user][beam_number_user]), user_coords):
                                                candidate[beam_number] = user
                                                candidate_user_beams[user][beam_number_user] = bs
                            else:
                                candidate[beam_number] = user
                                candidate_user_beams[user][beam_number_user] = bs
                for beam_number in candidate.keys():
                    occupied_beams[bs, beam_number] = 1
                    opt_x[candidate[beam_number], bs] = 1

            for user in range(number_of_users):
                possible_links_snr = []
                possible_links_bs = []
                if sum(opt_x[user, :]) == 0:
                    for bs in range(number_of_bs):
                        snr = f.find_snr(user, bs, x_user, y_user)
                        if snr > SINR_min:
                            possible_links_snr.append(snr)
                            possible_links_bs.append(bs)
                    zipje = zip(possible_links_snr, possible_links_bs)
                    zipje = sorted(zipje, reverse = True)
                    possible_bs = [y for x, y in zipje]

                    if len(possible_bs) > 0:
                        i = 0
                        while sum(opt_x[user, :]) == 0 and i < len(possible_bs):
                            bs = possible_bs[i]
                            bs_coords = f.bs_coords(bs)
                            user_coords = f.user_coords(user, x_user, y_user)
                            geo = f.find_geo(bs_coords, user_coords)
                            beam_number = f.find_beam_number(geo, beamwidth_b)
                            if occupied_beams[possible_bs[i], beam_number] == 0:
                                opt_x[user, bs] = 1
                                occupied_beams[possible_bs[i], beam_number] = 1
                            i += 1

                        if sum(opt_x[user,:]) == 0 and bandwidth_sharing:
                            opt_x[user, possible_bs[0]] = 1


            disconnected_user = 0
            sinr_constraint_fails = 0
            links_per_user = sum(np.transpose(opt_x))

            for u in range(number_of_users):
                if links_per_user[u] == 0:
                    disconnected_user += 1

            # pickle.dump(opt_x, open(str('Data/opt_x_heuristics/iteration_' + str(iteration) + name + '.p'), 'wb'), protocol=4)
            failed_link_constraints.append(disconnected_user)
            print(f.find_capacity(opt_x, x_user, y_user))
            optimal.append(opt_x)
            xs.append(x_user)
            ys.append(y_user)

        # pickle.dump(failed_link_constraints, open(str('Data/disconnected_users_iteration_' + str(iteration_max) + name + '.p'), 'wb'), protocol=4)

        # fig, ax = plt.subplots()
        # G, colorlist, nodesize, edgesize, labels, edgecolor = f.make_graph(x_bs, y_bs, x_user, y_user, opt_x, number_of_users)
        # f.draw_graph(G, colorlist, nodesize, edgesize, labels, ax, color = 'black', edgecolor = edgecolor)
        # plt.show()
        #
        # links_per_user = sum(np.transpose(opt_x))

        # fig, ax = plt.subplots()
        # plt.hist(links_per_user, density=True)
        # plt.show()

        # print(x_bs, y_bs)
        # print(x_user, y_user)

        find_data.main(optimal, xs, ys, Heuristic=True, bandwidth_sharing=bandwidth_sharing, user_beamforming = User_Beamforming)

