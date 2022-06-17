import math
from cycler import cycler
import matplotlib
import numpy as np
import pickle

Greedy = False

def find_name(iteration_max, number_of_users, Heuristic, SNRHeuristic, k, beamwidth_b, users_per_beam, Clustered, M, Greedy):
    user_rate = 500
    name = str(
        str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(
            M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))

    if Heuristic:
        name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str('SNR_k=' + str(k) + name)

    if Clustered:
        name = str(name + '_clustered')

    if Greedy and Heuristic:
        name = str(name + '_greedy')

    return name

def find_name_data(Heuristic, SNRHeuristic, k, beamwidth_deg, users_per_beam, Clustered, M, Greedy):
    user_rate = 500
    name = str(str(beamwidth_deg) + str(M) + str(users_per_beam) + str(user_rate))
    if Heuristic:
        name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str('SNR_k=' + str(k) + name)

    if Clustered:
        name = str(name + '_clustered')

    if Greedy and Heuristic:
        name = str(name + '_greedy')
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


iterations = {120: 1000, 300: 400, 600: 200, 900: 134, 1200: 100}
# iterations = {120: 100, 300: 40, 600: 20, 900: 14, 1200: 10}
# iterations = {120: 2, 300: 2, 600: 2, 900: 2, 1200: 2}


users = [120, 300, 600, 900, 1200]

Torus = True

pi = math.pi
bs_of_interest = 0
radius = 200  # for triangular grid

xmin, xmax = 0, 800
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

xDelta = xmax - xmin
yDelta = ymax - ymin

x_bs, y_bs = initialise_graph_triangular(radius, xDelta, yDelta)
number_of_bs = len(x_bs)


def find_scenario(scenario):
    if scenario in [1]:
        beamwidth_deg = 5
    elif scenario in [3]:
        beamwidth_deg = 15
    else:
        beamwidth_deg = 10

    if scenario in [1, 2, 3]:
        users_per_beam = 1
    elif scenario in [4, 8, 9]:
        users_per_beam = 2
    elif scenario in [5]:
        users_per_beam = 5
    elif scenario in [6]:
        users_per_beam = 10
    elif scenario in [7]:
        users_per_beam = 1000
    else:
        users_per_beam = False

    if scenario in [8]:
        Clustered = True
    else:
        Clustered = False

    if scenario in [9]:
        M = 0
    else:
        M = 10000

    return beamwidth_deg, users_per_beam, Clustered, M


def fairness(x):
    teller = sum(x) ** 2
    noemer = len(x) * sum([i ** 2 for i in x])
    return teller / noemer


def get_data(scenario, Heuristic=False, SNRHeuristic=False, k=0, Greedy = False):
    print('Getting data...')
    beamwidth_deg, users_per_beam, Clustered, M = find_scenario(scenario)
    beamwidth_b = beamwidth_deg

    mis = dict()
    mis_user = dict()

    deg = dict()

    cap = dict()
    sat = dict()
    fair = dict()

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

    for number_of_users in users:
        iteration_max = iterations[number_of_users]
        name = find_name(iteration_max, number_of_users, Heuristic, SNRHeuristic, k, beamwidth_b, users_per_beam, Clustered, M, Greedy)
        print(name)
        degrees = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
        misalignment_bs = pickle.load(open(str('Data/grid_misalignment_bs' + name + '.p'), 'rb'))
        misalignment_user = pickle.load(open(str('Data/grid_misalignment_user' + name + '.p'), 'rb'))

        capacity_blocked = pickle.load(open(str('Data/capacity_blocked' + name + '.p'), 'rb'))
        satisfaction_blocked = pickle.load(open(str('Data/satisfaction_blocked' + name + '.p'), 'rb'))

        capacity_per_user = pickle.load(open(str('Data/capacity' + name + '.p'), 'rb'))
        satisfaction = pickle.load(open(str('Data/satisfaction' + name + '.p'), 'rb'))

        capacity_per_user2_5 = pickle.load(open(str('Data/capacity_2_5' + name + '.p'), 'rb'))
        satisfaction2_5 = pickle.load(open(str('Data/satisfaction_2_5' + name + '.p'), 'rb'))

        capacity_per_user25 = pickle.load(open(str('Data/capacity_25' + name + '.p'), 'rb'))
        satisfaction25 = pickle.load(open(str('Data/satisfaction_25' + name + '.p'), 'rb'))

        capacity_per_user150 = pickle.load(open(str('Data/capacity_150' + name + '.p'), 'rb'))
        satisfaction150 = pickle.load(open(str('Data/satisfaction_150' + name + '.p'), 'rb'))

        fair[number_of_users] = fairness(capacity_per_user)
        fair_blocked[number_of_users] = fairness(capacity_blocked)
        fair2_5[number_of_users] = fairness(capacity_per_user2_5)
        fair25[number_of_users] = fairness(capacity_per_user25)
        fair150[number_of_users] = fairness(capacity_per_user150)

        deg[number_of_users] = sum(degrees) / len(degrees)
        mis[number_of_users] = np.std(misalignment_bs) * 2
        mis_user[number_of_users] = np.std(misalignment_user) * 2
        sat[number_of_users] = np.sum(satisfaction) / (len(satisfaction) * len(satisfaction[0]))
        cap[number_of_users] = np.sum(capacity_per_user) / len(capacity_per_user)
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

    print(sat)

    name = find_name_data(Heuristic, SNRHeuristic, k, beamwidth_deg, users_per_beam, Clustered, M, Greedy)
    print(name)
    pickle.dump(deg, open(str('Data/Processed/deg' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(mis, open(str('Data/Processed/mis' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(sat, open(str('Data/Processed/sat' + name + '.p'), 'wb'), protocol=4)
    pickle.dump(cap, open(str('Data/Processed/cap' + name + '.p'), 'wb'), protocol=4)
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

