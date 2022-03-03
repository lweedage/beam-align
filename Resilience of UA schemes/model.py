import numpy as np
from parameters import *
import functions as f


def find_beam_number(radians, beamwidth):
    angles = [beamwidth * i for i in range(int(-pi / beamwidth), int(pi / beamwidth))]
    min = math.inf
    beam_number = 0
    for i in range(int(2 * pi / beamwidth)):
        if abs(radians - angles[i]) < min:
            min = abs(radians - angles[i])  # NOTE THAT WE NOW JUST CHOOSE THE FIRST ONE IF TWO ARE EVEN CLOSE
            beam_number = i
    return beam_number


def find_gain(bore_1, bore_2, geo_1, geo_2, beamwidth_ml):
    bore = find_bore(bore_1, bore_2, beamwidth_ml)
    geo = find_geo(geo_1, geo_2)
    alpha = math.degrees(abs(bore - geo))
    if alpha > 180:
        alpha = alpha - 360
    beamwidth_ml = math.degrees(beamwidth_ml)
    w = beamwidth_ml / 2.58
    G0 = 20 * math.log10(1.62 / math.sin(math.radians(w / 2)))

    if 0 <= abs(alpha) <= beamwidth_ml / 2:
        return G0 - 3.01 * (2 * alpha / w) ** 2
    else:
        return -0.4111 * math.log(math.degrees(w)) - 10.579


def find_bore(coord_1, coord_2, beamwidth):
    radians = find_geo(coord_1, coord_2)
    angle = find_beam(radians, beamwidth)
    return angle


def find_geo(coord_1, coord_2):
    if Torus:
        (x_1, y_1) = coord_1
        (x_2, y_2) = coord_2

        if (max(coord_2[0], coord_1[0]) - min(coord_2[0], coord_1[0])) > (
                min(coord_2[0], coord_1[0]) - max(coord_2[0], coord_1[0])) % xDelta:
            if coord_2[0] > coord_1[0]:
                x_2 = coord_2[0] - xDelta
            else:
                x_1 = coord_1[0] - xDelta

        if (max(coord_2[1], coord_1[1]) - min(coord_2[1], coord_1[1])) > (
                min(coord_2[1], coord_1[1]) - max(coord_2[1], coord_1[1])) % yDelta:
            if coord_2[1] > coord_1[1]:
                y_2 = coord_2[1] - yDelta
            else:
                y_1 = coord_1[1] - yDelta

        coord_2 = (x_2, y_2)
        coord_1 = (x_1, y_1)

    dy = coord_2[1] - coord_1[1]
    dx = coord_2[0] - coord_1[0]
    radians = math.atan2(dy, dx)
    return radians


def find_beam(radians, beamwidth):
    angles = [beamwidth * i for i in range(int(-pi / beamwidth), int(pi / beamwidth))]
    min = math.inf
    preferred_angle = 0
    for angle in angles:
        if abs(radians - angle) <= min:
            min = abs(radians - angle)  # NOTE THAT WE NOW JUST CHOOSE THE FIRST ONE IF TWO ARE EVEN CLOSE
            preferred_angle = angle
    return preferred_angle


def find_misalignment(coord_1, coord_2, beamwidth):
    return find_geo(coord_1, coord_2) - find_bore(coord_1, coord_2, beamwidth)


def find_path_loss(user, bs):
    r = f.find_distance_3D(user, bs)
    breakpoint_distance = 4 * (BS_height - 1) * (user_height - 1) * centre_frequency / propagation_velocity
    SF = np.random.normal(0, 4)

    if r <= breakpoint_distance:
        path_loss = 32.4 + 21 * math.log10(r) + 20 * math.log10(centre_frequency / 1e9) + SF
        return path_loss
    else:
        print('BS is too far away')


def find_path_loss_nlos(user, bs):
    distance_3D = f.find_distance_3D(user, bs)
    SF = np.random.normal(0, 7.82)

    PL_los = find_path_loss(user, bs)
    PL_nlos = 35.3 * math.log10(distance_3D) + 22.4 + 21.3 * math.log10(centre_frequency / 1e9) - 0.3 * (user_height - 1.5) + SF

    return max(PL_nlos, PL_los)


def find_capacity(opt_x, x_user, y_user, with_los=False):
    per_user_capacity = find_capacity_per_user(opt_x, x_user, y_user, with_los)
    return sum(per_user_capacity)


def find_capacity_per_user(opt_x, x_user, y_user, with_los=False):
    occupied_beams = np.zeros((number_of_bs, len(directions_bs)))
    number_of_users = len(x_user)
    for u in range(number_of_users):
        for bs in range(number_of_bs):
            if opt_x[u, bs] == 1:
                coords_i = f.user_coords(u, x_user, y_user)
                coords_j = f.bs_coords(bs)
                geo = find_geo(coords_j, coords_i)
                beam_number = find_beam_number(geo, beamwidth_b)
                occupied_beams[bs, beam_number] += 1

    capacity = np.zeros(number_of_users)
    for u in range(number_of_users):
        for bs in range(number_of_bs):
            if opt_x[u, bs] == 1:
                coords_i = f.user_coords(u, x_user, y_user)
                coords_j = f.bs_coords(bs)
                gain_user = find_gain(coords_i, coords_j, coords_i, coords_j, beamwidth_u)
                gain_bs = find_gain(coords_j, coords_i, coords_j, coords_i, beamwidth_b)
                if with_los:
                    path_loss = find_line_of_sight_pathloss(coords_i, coords_j)

                else:
                    path_loss = find_path_loss(coords_i, coords_j)

                geo = find_geo(coords_j, coords_i)
                beam_number = find_beam_number(geo, beamwidth_b)
                capacity[u] += W / occupied_beams[bs, beam_number] * math.log2(
                    1 + transmission_power * gain_bs * gain_user / (path_loss * noise))
    return capacity


def find_snr(user, bs, x_user, y_user):
    coords_i = f.user_coords(user, x_user, y_user)
    coords_j = f.bs_coords(bs)
    gain_user = find_gain(coords_i, coords_j, coords_i, coords_j, beamwidth_u)
    gain_bs = find_gain(coords_j, coords_i, coords_j, coords_i, beamwidth_b)
    path_loss = find_path_loss(coords_i, coords_j)
    return (transmission_power * gain_user * gain_bs / path_loss) / noise


def find_nlos_probability(user, bs):
    r = f.find_distance(user, bs)
    if r <= 18:
        p_los = 1
    else:
        p_los = 18 / r + math.exp(-r / 36) * (1 - 18 / r)
    return 1 - p_los


def gain_SNR_pathloss(x_user, y_user):
    number_of_users = len(x_user)

    distances = np.zeros((number_of_users, number_of_bs))
    gain_bs = np.zeros((number_of_users, number_of_bs))
    gain_user = np.zeros((number_of_users, number_of_bs))
    SNR = np.zeros((number_of_users, number_of_bs))
    SINR = np.zeros((number_of_users, number_of_bs))
    path_loss = np.zeros((number_of_users, number_of_bs))
    interference = np.zeros((number_of_users, number_of_bs, number_of_bs))
    nlos_probability = np.zeros((number_of_users, number_of_bs))


    # calculating the gain, path_loss and interference for every user-bs pair
    for i in range(number_of_users):
        coords_i = f.user_coords(i, x_user, y_user)
        for j in range(number_of_bs):
            coords_j = f.bs_coords(j)
            distances[i,j] = f.find_distance(coords_i, coords_j)
            path_loss[i, j] = find_path_loss(coords_i, coords_j)
            gain_bs[i, j] = find_gain(coords_j, coords_i, coords_j, coords_i, beamwidth_b)
            gain_user[i, j] = find_gain(coords_i, coords_j, coords_i, coords_j, beamwidth_u)
            SNR[i, j] = transmission_power + gain_bs[i, j] + gain_user[i, j] - path_loss[i, j] - noise
            nlos_probability[i,j] = find_nlos_probability(coords_i, coords_j)

    for i in range(number_of_users):
        for j in range(number_of_bs):
            for k in range(number_of_bs):
                interference[i, j, k] = 10**((transmission_power + gain_bs[i, k] + gain_user[i,j] - path_loss[i,k])/10)
            SINR[i,j] = SNR[i,j] - 10 * math.log10(sum(interference[i,j]) - interference[i,j,j])
            print(10 * math.log10(sum(interference[i,j]) - interference[i,j,j]))

    return distances, gain_bs, gain_user, path_loss, SNR, SINR, nlos_probability
