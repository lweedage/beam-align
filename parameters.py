import math

import numpy as np

colors = ['#904C77', '#E49AB0', '#ECB8A5', '#96ACB7', '#957D95'] * 100
markers = ['o', 'X', 'v', 's', '*', 'P', '1', '+']

Greedy = False


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


    Clustered = False

    if scenario == 4:
        Clustered = True
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


scenario = int(input('Scenario?'))
beamwidth_deg, Clustered, M, max_connections = find_scenario(scenario)

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



if beamwidth_b == 5:
    misalignment_user = {21: 1.7549738753991504, 41: 1.3498868618450317, 104: 1.3018097881075703,
                         208: 1.4241036107764387, 312: 1.489127280940781, 10: 2.563120432885875, 15: 2.2409077302256044,
                         20: 1.7978877443413166}
    misalignment = {21: 1.7549738753991504, 41: 1.349886861845032, 104: 1.30180978810757, 208: 1.4241036107764384,
                    312: 1.4891272809407812, 10: 2.5631204328858757, 15: 2.2409077302256044, 20: 1.7978877443413162}


elif beamwidth_b == 10:
    misalignment_user = {21: 2.4150059448465226, 41: 1.9892760337765163, 104: 1.7714483714954201,
                         208: 1.9016740063785356, 312: 1.9433035381758874, 10: 2.7420851615894266,
                         15: 2.6676412021355658, 20: 2.4290951273824812}
    misalignment = {21: 4.799873408512321, 41: 3.3608438783519925, 104: 2.847651562265974, 208: 3.1877053682954406,
                    312: 3.3428211703931043, 10: 5.590860781587715, 15: 5.367639853500857, 20: 4.84368369718824}


elif beamwidth_b == 15:
    misalignment_user = {21: 2.2333014442275716, 41: 1.9485456403938493, 104: 1.8205315447718076,
                         208: 1.8987488775015149, 312: 1.9072796966922938, 10: 2.5397884162819353, 15: 2.47813867191403,
                         20: 2.2922707604390777}
    misalignment = {21: 7.090385062983365, 41: 6.273657538946974, 104: 5.629493123214034, 208: 5.901799336475697,
                    312: 6.005133582709884, 10: 7.579408354573356, 15: 7.409566174140733, 20: 7.244576791643011}

user_rate = 500  # Mbps

Torus = True

fading = np.random.normal(0, 4, (3007, number_of_bs))

overhead_factor = 0.75


def find_name(iteration_max, number_of_users, Heuristic, SNRHeuristic, Clustered, M, Greedy=False, Harris=False):
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

    if Greedy and Heuristic:
        name = str(name + '_greedy')
    return name


def find_name_data(Heuristic, SNRHeuristic, k, Clustered, M, Greedy=False):
    name = str(str(beamwidth_deg) + str(M))
    if Heuristic:
        name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str('SNR_k=' + str(k) + name)

    if Clustered:
        name = str(name + '_clustered')

    if Greedy and Heuristic:
        name = str(name + '_greedy')

    return name
