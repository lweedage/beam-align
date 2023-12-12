import pickle

import progressbar

import functions as f
import simulate_blockers
from parameters import *


def find_measures(optimal, shares, number_of_users, x_user, y_user, blocked_connections, AT, rain_rate):
    opt_x = np.zeros((number_of_users, number_of_bs))
    occupied_beams = np.zeros((number_of_bs, len(directions_bs)))

    for user in range(number_of_users):
        u = f.user_coords(user, x_user, y_user)
        for b in range(number_of_bs):
            if optimal[user, b] == 1:
                b_coords = f.bs_coords(b)
                if f.find_snr(user, b, x_user, y_user, blocked_connections[user, b], AT, rain_rate) > SINR_min:
                    opt_x[user, b] = 1
                    occupied_beams[b, f.find_beam_number(f.find_geo(b_coords, u), beamwidth_b)] += 1
    capacity = f.SINR_capacity_per_user(shares, x_user, y_user, AT, rain_rate, blocked = blocked_connections[user, b])
    satisfaction = np.ones(number_of_users)
    disconnected = 0
    for u in range(number_of_users):
        if capacity[u] < user_rate:
            satisfaction[u] = capacity[u] / user_rate
        if capacity[u] < 1:
            disconnected += 1

    return capacity, satisfaction, disconnected


def main(optimal, shares, xs, ys, satisfaction, Heuristic=False, SNRHeuristic=False, Greedy=False, Harris=False,
         power=None):
    misalignment_user = []
    misalignment_bs = []

    total_links_per_user = []
    capacity_per_user = np.array([])

    capacity_blocked = np.array([])
    satisfaction_blocked = []

    capacity_2_5 = np.array([])
    satisfaction_2_5 = []

    capacity_25 = np.array([])
    satisfaction_25 = []

    capacity_150 = np.array([])
    satisfaction_150 = []

    energy = []

    channel_capacity_SINR = []
    number_of_users = len(xs[0])

    disconnected_blocked = 0
    disconnected_2_5 = 0
    disconnected_25 = 0
    disconnected_150 = 0

    iteration_min = 0
    iteration_max = iterations[number_of_users]

    bar = progressbar.ProgressBar(maxval=iteration_max, widgets=[
        progressbar.Bar('=', f'Finding data... scenario: {scenario}, #users: {number_of_users} [', ']'), ' ',
        progressbar.Percentage(), ' ', progressbar.ETA()])
    bar.start()
    for iteration in range(iteration_min, iteration_max):
        bar.update(iteration)
        np.random.seed(iteration)
        x_user, y_user = xs[iteration], ys[iteration]

        opt_x = optimal[iteration]
        share = shares[iteration]
        links_per_user = sum(np.transpose(opt_x))
        if power is not None:
            P = power[iteration]
        else:
            P = None

        total_links_per_user.append(links_per_user)
        capacity_per_user = np.append(capacity_per_user, f.find_capacity_per_user(share, x_user, y_user, power=P))
        SINR_capacity_per_user = f.SINR_capacity_per_user(share, x_user, y_user, power=P)
        channel_capacity_SINR.append(SINR_capacity_per_user)

        beams = {b: set() for b in range(number_of_bs)}
        for user in range(number_of_users):
            u = f.user_coords(user, x_user, y_user)
            for b in range(number_of_bs):
                if opt_x[user, b] > 0:
                    b_coords = f.bs_coords(b)
                    misalignment_user.append(f.find_misalignment(u, b_coords, beamwidth_u))
                    misalignment_bs.append(f.find_misalignment(b_coords, u, beamwidth_b))
                    beam = f.find_beam_number(f.find_bore(b_coords, u, beamwidth_b), beamwidth_b)
                    beams[b].add(beam)

        active_beams = [len(beams[b]) for b in range(number_of_bs)]
        if Harris:
            energy_usage = np.sum(P)
        else:
            energy_usage = sum(active_beams) * transmission_power

        blocked_connections = simulate_blockers.find_blocked_connections(share, x_user, y_user, number_of_users)
        cap_blocked, sat_blocked, dis_blocked = find_measures(opt_x, share, number_of_users, x_user, y_user,
                                                              blocked_connections, AT=False,
                                                              rain_rate=0)
        blocked_connections = np.zeros((number_of_users, number_of_bs))
        cap_2_5, sat_2_5, dis_2_5 = find_measures(opt_x, share, number_of_users, x_user, y_user, blocked_connections,
                                                  AT=True, rain_rate=2.5)
        cap_25, sat_25, dis_25 = find_measures(opt_x, share, number_of_users, x_user, y_user, blocked_connections,
                                               AT=True, rain_rate=25)
        cap_150, sat_150, dis_150 = find_measures(opt_x, share, number_of_users, x_user, y_user, blocked_connections,
                                                  AT=True, rain_rate=150)

        capacity_blocked = np.append(capacity_blocked, cap_blocked)
        satisfaction_blocked.append(sat_blocked)
        capacity_2_5 = np.append(capacity_2_5, cap_2_5)
        satisfaction_2_5.append(sat_2_5)
        capacity_25 = np.append(capacity_25, cap_25)
        satisfaction_25.append(sat_25)
        capacity_150 = np.append(capacity_150, cap_150)
        satisfaction_150.append(sat_150)

        disconnected_blocked += dis_blocked
        disconnected_2_5 += dis_2_5
        disconnected_25 += dis_25
        disconnected_150 += dis_150

        energy.append(energy_usage)

    bar.finish()
    name = find_name(iteration_max, number_of_users, Heuristic, SNRHeuristic, Clustered, M, Greedy, Harris)
    print('find data', name)
    # print(f'Blocked:', disconnected_blocked / (iteration_max * number_of_users))
    # print(f'Rain 2.5:', disconnected_2_5 / (iteration_max * number_of_users))
    # print(f'Rain 25:', disconnected_25 / (iteration_max * number_of_users))
    # print(f'Rain 150:', disconnected_150 / (iteration_max * number_of_users))
    print(f'Energy usage:', sum(energy) / len(energy))
    print(f'Average number of connections:',
          np.sum(total_links_per_user) / iterations[number_of_users] / number_of_users)
    pickle.dump(energy, open(str('Data/energy' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(misalignment_bs, open(str('Data/grid_misalignment_bs' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(misalignment_user, open(str('Data/grid_misalignment_user' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(total_links_per_user, open(str('Data/total_links_per_user' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(channel_capacity_SINR, open(str('Data/channel_capacity_SINR' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(capacity_per_user, open(str('Data/capacity' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(satisfaction, open(str('Data/satisfaction' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(satisfaction_blocked, open(str('Data/satisfaction_blocked' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(capacity_blocked, open(str('Data/capacity_blocked' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(satisfaction_2_5, open(str('Data/satisfaction_2_5' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(capacity_2_5, open(str('Data/capacity_2_5' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(satisfaction_25, open(str('Data/satisfaction_25' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(capacity_25, open(str('Data/capacity_25' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(satisfaction_150, open(str('Data/satisfaction_150' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(capacity_150, open(str('Data/capacity_150' + name + '.p'), 'wb'), protocol=4)
