import matplotlib.pyplot as plt
import numpy as np
import find_data
from parameters import *
import new_optimization
import functions as f
import time
import pickle

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

def find_users_to_connect(bs_coords, x_user, y_user, candidate_user_beams):
    number_of_users = len(x_user)
    candidate = dict()
    for user in range(number_of_users):
        user_coords = f.user_coords(user, x_user, y_user)

        geo_bs = f.find_geo(bs_coords, user_coords)
        bs_beam = f.find_beam(geo_bs, beamwidth_b)
        beam_number_bs = f.find_beam_number(geo_bs, beamwidth_b)

        geo_user = f.find_geo(user_coords, bs_coords)
        user_beam = f.find_beam(geo_user, beamwidth_u)
        beam_number_user = f.find_beam_number(geo_user, beamwidth_u)

        if np.degrees(abs(geo_bs - bs_beam)) <= misalignment[number_of_users]:
            if not User_Misalignment or np.degrees(abs(geo_user - user_beam)) <= misalignment_user[number_of_users]:
                snr = f.find_snr(user, bs, x_user, y_user)
                if snr >= SINR_min:
                    if beam_number_bs in candidate.keys(): # for every user, check if beam is occupied and if so, if you are closer COULD ALSO BE HIGHER SNR?
                        if find_distance(bs_coords, user_coords) < find_distance(bs_coords, f.user_coords(candidate[beam_number_bs], x_user, y_user)):
                            candidate[beam_number_bs] = user
                            if beam_number_user in candidate_user_beams[user].keys():
                                if find_distance(bs_coords, user_coords) < find_distance(
                                        f.bs_coords(candidate_user_beams[user][beam_number_user]), user_coords):
                                    candidate[beam_number_bs] = user
                                    candidate_user_beams[user][beam_number_user] = bs
                    else:
                        candidate[beam_number_bs] = user
                        candidate_user_beams[user][beam_number_user] = bs
    return candidate, candidate_user_beams

for number_of_users in [100, 300, 500, 750, 1000]:
    for User_Misalignment in [False, True]:
        iteration_min, iteration_max = 0, iterations[number_of_users]

        optimal = []
        xs = []
        ys = []
        disconnected = []

        for iteration in range(iteration_min, iteration_max):
            opt_x = np.zeros((number_of_users, number_of_bs))
            print('Iteration ', iteration)
            x_user, y_user = f.find_coordinates(number_of_users)

            occupied_beams = np.zeros((number_of_bs, len(directions_bs)))
            candidate_user_beams = [dict() for i in range(number_of_users)]

            for bs in range(number_of_bs):
                bs_coords = f.bs_coords(bs)
                to_connect, candidate_user_beams = find_users_to_connect(bs_coords, x_user, y_user, candidate_user_beams)

                for beam_number in to_connect.keys():
                    occupied_beams[bs, beam_number] = 1
                    opt_x[to_connect[beam_number], bs] = 1
            for user in range(number_of_users): #check if a user is not connected yet and connect to highest snr that is in empty beam
                possible_links_snr = []
                possible_links_bs = []
                user_coords = f.user_coords(user, x_user, y_user)

                if sum(opt_x[user, :]) == 0:
                    First = True
                    bss = np.argsort(f.find_distance_all_bs(user_coords))
                    for bs in bss:
                        snr = f.find_snr(user, bs, x_user, y_user)
                        if snr > SINR_min:
                            possible_links_snr.append(snr)
                            possible_links_bs.append(bs)

                            bs_coords = f.bs_coords(bs)
                            geo = f.find_geo(bs_coords, user_coords)
                            beam_number = f.find_beam_number(geo, beamwidth_b)
                            if occupied_beams[bs, beam_number] == 0 and First:
                                opt_x[user, bs] = 1
                                occupied_beams[bs, beam_number] = 1
                                print('first in a beam that was still empty!')
                                First = False

                    if len(possible_links_bs) > 0 and sum(opt_x[user, :]) == 0: # if the user still has no connection
                        print('Still no connection')
                        zipje = zip(possible_links_snr, possible_links_bs)
                        zipje = sorted(zipje, reverse = True)
                        possible_bs = [y for x, y in zipje]
                        opt_x[user, possible_bs[0]] = 1
                    else:
                        print('No connection possible')


            disconnected_user = 0
            links_per_user = sum(np.transpose(opt_x))

            for u in range(number_of_users):
                if links_per_user[u] == 0:
                    disconnected_user += 1

            optimal.append(opt_x)
            xs.append(x_user)
            ys.append(y_user)
            disconnected.append(disconnected_user)

        find_data.main(optimal, xs, ys, disconnected, Heuristic=True, UserMisalignment = User_Misalignment)

