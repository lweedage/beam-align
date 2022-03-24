import math
from cycler import cycler
import matplotlib
import numpy as np
import pickle

matplotlib.rcParams['axes.prop_cycle'] = cycler('color', ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed'])
colors =  ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed', 'grey'] * 10

def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3 / 4) * radius
    for i in range(0, int(xDelta / radius) + 1):
        for j in range(0, int(yDelta / dy) + 1):
            if i * radius + 0.5 * (j % 2) * radius < xmax and j * dy < ymax:
                xbs.append(i * radius + 0.5 * (j % 2) * radius)
                ybs.append(j * dy)
    return xbs, ybs



iterations = {50: 1, 100: 5000, 300: 1667, 500: 1000, 750: 667, 1000: 500}
iterations = {50: 1, 100: 1250, 300: 417, 500: 250, 750: 167, 1000: 125}

Torus = True

pi = math.pi
bs_of_interest = 0
radius = 50  # for triangular grid

xmin, xmax = 0, 200
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

xDelta = xmax - xmin
yDelta = ymax - ymin

beamwidth_u = math.radians(5)
W = 1  # bandwidth

transmission_power = 10 ** 3.0  # 30 dB
noise_figure = 7.8
noise_power_db = -174 + 10 * math.log10(W * 10 ** 9) + noise_figure
noise = 10 ** (noise_power_db / 10)

BS_height = 10
user_height = 1.5
centre_frequency = 28e9
propagation_velocity = 3e8

SINR_min = 10 ** (-5 / 10)

x_bs, y_bs = initialise_graph_triangular(radius, xDelta, yDelta)
number_of_bs = len(x_bs)


def find_scenario(scenario):
    if scenario in [1, 4, 7, 10, 13, 16, 19, 22, 25, 28]:
        beamwidth_deg = 5
    elif scenario in [2, 5, 8, 11, 14, 17, 20, 23, 26, 29]:
        beamwidth_deg = 10
    else:
        beamwidth_deg = 15

    if scenario in [1, 2, 3, 4, 5, 6]:
        users_per_beam = 1
    elif scenario in [7, 8, 9, 10, 11, 12]:
        users_per_beam = 2
    elif scenario in [13, 14, 15, 16, 17, 18, 25, 26, 27, 28, 29, 30]:
        users_per_beam = 5
    elif scenario in [19, 20, 21, 22, 23, 24]:
        users_per_beam = 10
    else:
        users_per_beam = False

    if scenario in [1, 2, 3, 7, 8, 9, 13, 14, 15, 19, 20, 21, 25, 26, 27]:
        Penalty = True
    else:
        Penalty = False

    if scenario in [25, 26, 27, 28, 29, 30]:
        Clustered = True
    else:
        Clustered = False

    return beamwidth_deg, users_per_beam, Penalty, Clustered

def fairness(x):
    teller = sum(x)**2
    noemer = len(x) * sum([i**2 for i in x])
    return teller/noemer

for scenario in [7, 8, 9]: #range(25, 31):
    print(f'Scenario {scenario}')
    beamwidth_deg, users_per_beam, Penalty, Clustered = find_scenario(scenario)
    beamwidth_b = math.radians(int(beamwidth_deg))
    Heuristic = True

    if Penalty:
        M = 100  # penalty on having disconnected users
    else:
        M = 0

    directions_bs = range(int(2 * pi / beamwidth_b))
    directions_u = range(int(2 * pi / beamwidth_u))

    user = [100, 300, 500, 750, 1000]

    mis = dict()
    mis_user = dict()

    dis = dict()
    deg = dict()
    cap = dict()
    fair = dict()
    cap_blocked = dict()
    dis_blocked = dict()
    fair_blocked = dict()



    for number_of_users in user:
        iteration_min = 0
        iteration_max = iterations[number_of_users]

        # print(iteration_max)
        name = str(str(iteration_max) +
            'users=' + str(number_of_users) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)) + 'M=' + str(
                M) + 's=' + str(users_per_beam))


        if Clustered:
            name = str(name + '_clustered')

        if Heuristic:
            name = str('beamwidth_heuristic' + name)

        degrees = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
        disconnected = pickle.load(open(str('Data/disconnected_users' + name + '.p'), 'rb'))
        misalignment_bs = pickle.load(open(str('Data/grid_misalignment_bs' + name + '.p'), 'rb'))
        misalignment_user = pickle.load(open(str('Data/grid_misalignment_user' + name + '.p'), 'rb'))
        capacity = pickle.load(open(str('Data/channel_capacity' + name + '.p'), 'rb'))
        blocked_capacity = pickle.load(open(str('Data/blocked_capacity' + name + '.p'), 'rb' ))
        disconnected_blocked = pickle.load( open(str('Data/disconnected_blocked_users' + name + '.p'), 'rb'))
        capacity_per_user = pickle.load(open(str('Data/channel_capacity_per_user' + name + '.p'), 'rb'))
        capacity_per_user_blocked = pickle.load(open(str('Data/blocked_capacity_per_user' + name + '.p'), 'rb'))

        fair[number_of_users] = fairness(capacity_per_user)
        fair_blocked[number_of_users] = fairness(capacity_per_user_blocked)
        deg[number_of_users] = sum(degrees) / len(degrees)
        mis[number_of_users] = np.degrees(np.std(misalignment_bs) * 2)
        mis_user[number_of_users] = np.degrees(np.std(misalignment_user)*2)
        dis[number_of_users] = np.sum(disconnected) / len(disconnected)
        cap[number_of_users] = np.sum(capacity)/len(capacity)
        cap_blocked[number_of_users] = np.sum(blocked_capacity)/len(blocked_capacity)
        dis_blocked[number_of_users] = np.sum(disconnected_blocked)/len(disconnected_blocked)

    name = str(str(beamwidth_deg) + str(M) + str(users_per_beam))
    if Clustered:
        name = str(name + '_clustered')

    if Heuristic:
        name = str(name + '_heuristic')

    print(name)
    print(mis)
    print(mis_user)

    pickle.dump(deg, open(str('Data/Processed/deg' + name + '.p'),'wb'), protocol=4)
    pickle.dump(mis, open(str('Data/Processed/mis' + name + '.p'),'wb'), protocol=4)
    pickle.dump(dis, open(str('Data/Processed/dis' + name + '.p'),'wb'), protocol=4)
    pickle.dump(cap, open(str('Data/Processed/cap' + name + '.p'),'wb'), protocol=4)
    pickle.dump(fair, open(str('Data/Processed/fair' + name + '.p'),'wb'), protocol=4)
    pickle.dump(cap_blocked, open(str('Data/Processed/cap_blocked' + name + '.p'),'wb'), protocol=4)
    pickle.dump(dis_blocked, open(str('Data/Processed/dis_blocked' + name + '.p'),'wb'), protocol=4)
    pickle.dump(fair_blocked, open(str('Data/Processed/fair_blocked' + name + '.p'),'wb'), protocol=4)
