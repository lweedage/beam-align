import math
import os
import pickle

import matplotlib
import numpy as np
from cycler import cycler

Greedy = False



def find_name(iteration_max, number_of_users, Heuristic, SNRHeuristic, beamwidth_b, max_connections, Clustered, M,
              Greedy, Harris):
    name = str(
        str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(
            M) + 'k=' + str(max_connections) + 'active_beams=' + str(10))

    if Heuristic:
        name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str(name + '_SNRheuristic')

    elif Harris:
        name = str('HHO' + name)

    if Clustered:
        name = str(name + '_clustered')

    if Greedy and Heuristic:
        name = str(name + '_greedy')

    return name


def find_name_data(Heuristic, SNRHeuristic, beamwidth_deg, max_connections, Clustered, M, Greedy, Harris):
    name = str(str(beamwidth_deg) + str(M) + str(max_connections))
    if Heuristic:
        name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str(name + '_SNRheuristic')

    elif Harris:
        name = str('HHO' + name)

    if Clustered:
        name = str(name + '_clustered')

    return name


matplotlib.rcParams['axes.prop_cycle'] = cycler('color',
                                                ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen',
                                                 'OrangeRed'])
colors = ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed', 'grey'] * 10


def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3 / 4) * radius
    for i in range(0, int(xDelta / radius) + 1):
        for j in range(0, int(yDelta / dy) + 1):
            if i * radius + 0.5 * (j % 2) * radius < xmax and j * dy < ymax:
                xbs.append(i * radius + 0.5 * (j % 2) * radius)
                ybs.append(j * dy)
    return xbs, ybs


# iterations = {120: 1000, 300: 400, 600: 200, 900: 134, 1200: 100}
# iterations = {120: 100, 300: 40, 600: 20, 900: 14, 1200: 10}
# iterations = {30: 2, 60: 2, 120: 2, 300: 2, 600: 2, 900: 2, 1200: 2, 10: 2, 15: 2, 20: 2}
iterations = {21: 477, 41: 244, 104: 97, 208: 48, 312: 32, 10: 200, 15: 134, 20: 100}

Torus = True

pi = math.pi
bs_of_interest = 0
radius = 200  # for triangular grid

xmin, xmax = 0, 600
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 2

# xmin, xmax = 0, 400
# ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 1

xDelta = xmax - xmin
yDelta = ymax - ymin

area = xDelta * yDelta / (1000 * 1000)

users = [21, 41, 104, 208, 312]
# users = [10, 15, 20]
# users = [208]
x_bs, y_bs = initialise_graph_triangular(radius, xDelta, yDelta)
number_of_bs = len(x_bs)


def find_scenario(scenario):
    if scenario in [1, 11, 21, 31]:
        beamwidth_deg = 5
    elif scenario in [2, 12, 22, 32, 4]:
        beamwidth_deg = 10
    elif scenario in [3, 13, 23, 33]:
        beamwidth_deg = 15

    if scenario in [1, 2, 3, 4]:
        k = 25
    elif scenario in [21, 22, 23]:
        k = 2
    elif scenario in [31, 32, 33]:
        k = 1

    if scenario in [4]:
        Clustered = True
    else:
        Clustered = False
    M = 750
    # M = 10000
    # if scenario in [21, 22, 23]:
    #     Clustered = True
    # else:
    #     Clustered = False
    #
    # if scenario in [11, 12, 13]:
    #     M = 0
    # else:
    #     M = 10000
    # M = 10

    return beamwidth_deg, Clustered, M, k


def fairness(x):
    teller = sum(x) ** 2
    noemer = len(x) * sum([i ** 2 for i in x])
    return teller / noemer


def load_file(name):
    if os.path.exists(name):
        return pickle.load(open(str(name), 'rb'))
    else:
        return None


def get_data(scenario, Heuristic=False, SNRHeuristic=False, Greedy=False, Harris=False):
    print('Getting data...')
    beamwidth_deg, Clustered, M, max_connections = find_scenario(scenario)
    if Harris:
        M = 300
    beamwidth_b = beamwidth_deg
    mis = dict()
    mis_user = dict()

    deg = dict()

    cap = dict()
    sat = dict()
    fair = dict()
    capSINR = dict()
    satSINR = dict()
    cap_blocked = dict()
    sat_blocked = dict()
    fair_blocked = dict()

    cap2_5 = dict()
    sat2_5 = dict()
    cap25 = dict()
    sat25 = dict()
    cap150 = dict()
    sat150 = dict()

    fair2_5 = dict()
    fair25 = dict()
    fair150 = dict()

    dis = dict()

    sigmaBS = dict()
    sigmaU = dict()

    energy_use = dict()

    for number_of_users in users:
        iteration_max = iterations[number_of_users]
        name = find_name(iteration_max, number_of_users, Heuristic, SNRHeuristic, beamwidth_b, max_connections,
                         Clustered, M, Greedy, Harris)
        print(name)
        degrees = load_file('Data/total_links_per_user' + name + '.p')
        misalignment_bs = load_file('Data/grid_misalignment_bs' + name + '.p')
        misalignment_user = load_file('Data/grid_misalignment_user' + name + '.p')

        capacity_blocked = load_file('Data/capacity_blocked' + name + '.p')
        satisfaction_blocked = load_file('Data/satisfaction_blocked' + name + '.p')

        capacity_per_user = load_file('Data/capacity_per_user' + name + '.p')
        satisfaction = load_file('Data/satisfaction' + name + '.p')

        capacity_per_user2_5 = load_file('Data/capacity_2_5' + name + '.p')
        satisfaction2_5 = load_file('Data/satisfaction_2_5' + name + '.p')

        capacity_per_user25 = load_file('Data/capacity_25' + name + '.p')
        satisfaction25 = load_file('Data/satisfaction_25' + name + '.p')

        capacity_per_user150 = load_file('Data/capacity_150' + name + '.p')
        satisfaction150 = load_file('Data/satisfaction_150' + name + '.p')

        capacity_SINR = load_file('Data/channel_capacity_SINR' + name + '.p')




        user_rate = 500
        if 10 in users:
            shares = load_file('Data/shares' + name + '.p')
            sigma_user = []
            sigma_bs = []
            for i, j in enumerate(capacity_SINR):
                sigma_user.append(math.sqrt(np.sum(np.subtract(j, sum(j) / number_of_users) ** 2) / number_of_users))
                bs_rate = np.matmul(np.transpose(j), shares[i])
                sigma_bs.append(
                    math.sqrt(np.sum(np.subtract(bs_rate, sum(bs_rate) / number_of_bs) ** 2) / number_of_bs))
            sigmaBS[number_of_users] = sum(sigma_bs) / len(sigma_bs)
            sigmaU[number_of_users] = sum(sigma_user) / len(sigma_user)

        satisfaction_SINR = []
        for j in capacity_SINR:
            for i in range(len(j)):
                if j[i] >= user_rate:
                    satisfaction_SINR.append(1)
                else:
                    satisfaction_SINR.append(0)

        energy = load_file('Data/energy' + name + '.p')
        energy = [i for i in energy if i > 0]


        fair[number_of_users] = fairness(capacity_per_user)
        fair_blocked[number_of_users] = fairness(capacity_blocked)
        fair2_5[number_of_users] = fairness(capacity_per_user2_5)
        fair25[number_of_users] = fairness(capacity_per_user25)
        fair150[number_of_users] = fairness(capacity_per_user150)
        dis[number_of_users] = sum([1 for sublist in degrees for item in sublist if item == 0])/(len(degrees)*len(degrees[0]))
        deg[number_of_users] = sum(degrees) / len(degrees)
        mis[number_of_users] = np.std(misalignment_bs) * 2
        mis_user[number_of_users] = np.std(misalignment_user) * 2
        sat[number_of_users] = np.sum(satisfaction) / (len(satisfaction) * len(satisfaction[0]))
        cap[number_of_users] = np.sum(capacity_per_user) / (len(capacity_per_user) * len(capacity_per_user[0]))
        capSINR[number_of_users] = np.sum(capacity_SINR) / (len(capacity_SINR) * len(capacity_SINR[0]))
        satSINR[number_of_users] = np.sum(satisfaction_SINR) / (len(satisfaction_SINR))

        cap_blocked[number_of_users] = np.sum(capacity_blocked) / len(capacity_blocked)
        sat_blocked[number_of_users] = np.sum(satisfaction_blocked) / (len(satisfaction_blocked) * len(satisfaction[0]))

        sat2_5[number_of_users] = np.sum(satisfaction2_5) / (len(satisfaction2_5) * len(satisfaction2_5[0]))
        cap2_5[number_of_users] = np.sum(capacity_per_user2_5) / len(capacity_per_user2_5)
        sat25[number_of_users] = np.sum(satisfaction25) / (len(satisfaction25) * len(satisfaction25[0]))
        cap25[number_of_users] = np.sum(capacity_per_user25) / len(capacity_per_user25)
        sat150[number_of_users] = np.sum(satisfaction150) / (len(satisfaction150) * len(satisfaction150[0]))
        cap150[number_of_users] = np.sum(capacity_per_user150) / len(capacity_per_user150)

    print(mis)
    print(mis_user)
    print(satSINR)


    name = find_name_data(Heuristic, SNRHeuristic, beamwidth_deg, max_connections, Clustered, M, Greedy, Harris)
    if users[0] == 10:
        name = str(name + str(10))
        pickle.dump(sigmaBS, open(str('Data/Processed/sigmaBS' + name + '.p'), 'wb'), protocol=4)
        pickle.dump(sigmaU, open(str('Data/Processed/sigmaU' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(energy_use, open(str('Data/Processed/energy' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(deg, open(str('Data/Processed/deg' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(mis, open(str('Data/Processed/mis' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(dis, open(str('Data/Processed/dis' + name + '.p'), 'wb'), protocol=4)

    pickle.dump(sat, open(str('Data/Processed/sat' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(cap, open(str('Data/Processed/cap' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(capSINR, open(str('Data/Processed/capSINR' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(satSINR, open(str('Data/Processed/satSINR' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(fair, open(str('Data/Processed/fair' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(cap_blocked, open(str('Data/Processed/cap_blocked' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(sat_blocked, open(str('Data/Processed/sat_blocked' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(fair_blocked, open(str('Data/Processed/fair_blocked' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(cap2_5, open(str('Data/Processed/cap2_5' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(sat2_5, open(str('Data/Processed/sat2_5' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(fair2_5, open(str('Data/Processed/fair2_5' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(cap25, open(str('Data/Processed/cap25' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(sat25, open(str('Data/Processed/sat25' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(fair25, open(str('Data/Processed/fair25' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(cap150, open(str('Data/Processed/cap150' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(sat150, open(str('Data/Processed/sat150' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(fair150, open(str('Data/Processed/fair150' + name + '.p'), 'wb'), protocol=4)
