import math

import numpy as np

colors = ['#904C77', '#E49AB0', '#ECB8A5', '#96ACB7', '#957D95'] * 100
markers = ['o', 'X', 'v', 's', '*', 'P', '1', '+']

Greedy = False


def find_scenario(scenario):
    if scenario in [1, 11, 21, 31]:
        beamwidth_deg = 5
    elif scenario in [2, 12, 22, 32, 4, 5]:
        beamwidth_deg = 10
    elif scenario in [3, 13, 23, 33]:
        beamwidth_deg = 15

    if scenario in [1, 2, 3, 4, 5]:
        k = 25
    elif scenario in [21, 22, 23]:
        k = 2
    elif scenario in [31, 32, 33]:
        k = 1

    Clustered = False
    NonBlocked = False

    if scenario == 4:
        Clustered = True
    if scenario == 5:
        NonBlocked = True

    # M = 1000
    M = 1000
    # M = 1000
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

    return beamwidth_deg, Clustered, M, k, NonBlocked


scenario = int(input('Scenario?'))
beamwidth_deg, Clustered, M, max_connections, NonBlocked = find_scenario(scenario)

pi = math.pi
bs_of_interest = 10
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

number_of_active_beams = 10

beamwidth_u = 5
beamwidth_b = beamwidth_deg

W = 200  # in MHz  # bandwidth

transmission_power = (10 ** 2.0) / number_of_active_beams  # 20 dB per BS
noise_figure = 7.8
noise_power_db = -174 + 10 * math.log10(W * 10 ** 9) + noise_figure
noise = 10 ** (noise_power_db / 10)

BS_height = 10
user_height = 1.5
# centre_frequency = 28e9
[f1, f2, f3, f4, f5, f6, f7] = [28e9, 27.8e9, 28.2e9, 27.6e9, 28.4e9, 27.4e9, 28.6e9]
centre_frequencies = [f4, f3, f5, f6, f2, f1, f4, f7, f7, f6, f5, f1]
propagation_velocity = 3e8

SINR_min = 10 ** (5 / 10)

directions_bs = range(int(360 / beamwidth_b))
directions_u = range(int(360 / beamwidth_u))


def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3 / 4) * radius
    for i in range(0, int(xDelta / radius) + 1):
        for j in range(0, int(yDelta / dy) + 1):
            if i * radius + 0.5 * (j % 2) * radius < xmax and j * dy < ymax:
                xbs.append(i * radius + 0.5 * (j % 2) * radius)
                ybs.append(j * dy)
    return xbs, ybs


x_bs, y_bs = initialise_graph_triangular(radius, xDelta, yDelta)
number_of_bs = len(x_bs)

iterations = {21: 477, 41: 244, 104: 97, 208: 48, 312: 32, 10: 200, 15: 134, 20: 100}
# iterations = {21: 5, 41: 5, 104: 5, 208: 5, 312: 5, 10: 5, 15: 5, 20: 5}
# iterations = {21: 477 // 2, 41: 244 // 2, 104: 97 // 2, 208: 48 // 2, 312: 32 // 2, 10: 20, 15: 14, 20: 10}

if beamwidth_b == 5:
    misalignment_user = {21: 1.9660850429113226, 41: 1.9467978447199958, 104: 1.883847829911705,
                         208: 1.8545059850753136, 312: 1.8841182098083262}
    misalignment = {21: 1.9660850429113228, 41: 1.9444199958988384, 104: 1.8838478299117047, 208: 1.854505985075313,
                    312: 1.8841182098083267}


elif beamwidth_b == 10:
    misalignment_user = {21: 2.454426849423075, 41: 2.4344443520216004, 104: 2.413813543155066, 208: 2.417186834558454,
                         312: 2.428452303409957, 10: 2.5390330368809906, 15: 2.4840751867422366, 20: 2.4751149819842917}
    misalignment = {21: 4.791969911696629, 41: 4.835694684307278, 104: 4.765221316761182, 208: 4.7312715395019564,
                    312: 4.782898685823669,10: 4.913626861419469, 15: 4.85318334644194, 20: 5.131420718216987}


elif beamwidth_b == 15:
    misalignment_user = {21: 2.3642201919049755, 41: 2.3336101525187614, 104: 2.3229063744510032,
                         208: 2.306264630417769, 312: 2.326808146225465}
    misalignment = {21: 7.1208180184629715, 41: 7.0288037747704495, 104: 6.978981843938175, 208: 7.060181578648941,
                    312: 7.064460139528851}

user_rate = 100  # Mbps

Torus = True

fading = np.random.normal(0, 4, (3007, number_of_bs))

overhead_factor = 0.75


def find_name(iteration_max, number_of_users, Heuristic, SNRHeuristic, Clustered, M, Harris=False, NonBlocked = False):
    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(
        M) + 'k=' + str(max_connections) + 'active_beams=' + str(number_of_active_beams))

    if Heuristic:
        name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str(name + '_SNRheuristic')

    elif Harris:
        name = str('HHO' + name)

    if Clustered:
        name = str(name + '_clustered')

    if NonBlocked:
        name = str(name + '_noblockage')
    return name


def find_name_data(Heuristic, SNRHeuristic, k, Clustered, M, NonBlocked = False):
    name = str(str(beamwidth_deg) + str(M))
    if Heuristic:
        name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str('SNR_k=' + str(k) + name)

    if Clustered:
        name = str(name + '_clustered')

    if NonBlocked:
        name = str(name + '_noblockage')

    return name
