import math
from cycler import cycler
import matplotlib
import numpy as np

matplotlib.rcParams['axes.prop_cycle'] = cycler('color',
                                                ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen',
                                                 'OrangeRed'])
colors = ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed', 'grey'] * 1000


def find_scenario(scenario):
    if scenario in [1]:
        beamwidth_deg = 5
    elif scenario in [3]:
        beamwidth_deg = 15
    else:
        beamwidth_deg = 10

    if scenario in [1, 2, 3]:
        users_per_beam = 1
    elif scenario in [4, 8, 9, 10, 11]:
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

    return beamwidth_deg, users_per_beam, Clustered


scenario = int(input('Scenario?'))
beamwidth_deg, users_per_beam, Clustered = find_scenario(scenario)

pi = math.pi
bs_of_interest = 10
radius = 200  # for triangular grid

xmin, xmax = 0, 800
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

xDelta = xmax - xmin
yDelta = ymax - ymin

users = [120, 300, 600, 900, 1200]

beamwidth_u = 5
beamwidth_b = beamwidth_deg

W = 200  # in MHz  # bandwidth
M = 10000  # penalty on having disconnected users
# M = 0

transmission_power = (10 ** 2.0) / (360 / beamwidth_deg)  # 20 dB
noise_figure = 7.8
noise_power_db = -174 + 10 * math.log10(W * 10 ** 9) + noise_figure
noise = 10 ** (noise_power_db / 10)

BS_height = 10
user_height = 1.5
centre_frequency = 28e9
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

iterations = {120: 1000, 300: 400, 600: 200, 900: 134, 1200: 100}
# iterations = {120: 100, 300: 40, 600: 20, 900: 14, 1200: 10}
# iterations = {120: 1, 300: 1, 600: 1, 900: 1, 1200: 1}


if beamwidth_b == 5:
    misalignment_user = {120: 1.7174853459795385, 300: 1.5533509411672755, 600: 1.3843984679093195, 900: 1.302217312979267, 1200: 1.286268959981136}
    misalignment = {120: 1.7174853459795385, 300: 1.5533509411672755, 600: 1.3843984679093195, 900: 1.302217312979267, 1200: 1.286268959981136}

elif beamwidth_b == 10:
    misalignment_user = {120: 2.069725379632131, 300: 1.8942287559336388, 600: 1.7859018235801447, 900: 1.7984282555607853, 1200: 1.7000609251251997}
    misalignment = {120: 3.6618244862232197, 300: 3.163133966123575, 600: 2.844711481564295, 900: 2.9766376097585443, 1200: 2.650084523533067}

elif beamwidth_b == 15:
    misalignment_user = {120: 1.9346621561117616, 300: 1.826887458419739, 600: 1.8254471763677291, 900: 1.7422006282203961, 1200: 1.712191390117882}
    misalignment = {120: 6.219147302411779, 300: 5.710565966733396, 600: 5.824994344858849, 900: 5.372455264470386, 1200: 5.315660665127901}


RateRequirement = True
user_rate = 500  # Mbps

Torus = True

fading = np.random.normal(0, 4, (3007, number_of_bs))

overhead_factor = 0.75

def find_name(iteration_max, number_of_users, Heuristic, SNRHeuristic, GreedyRate, k):
    name = str(
        str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(
            M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))

    if Heuristic:
        name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str('SNR_k=' + str(k) + name)

    elif GreedyRate:
        name = str(name + 'GreedyRate')

    if Clustered:
        name = str(name + '_clustered')

    return name

def find_name_data(Heuristic, SNRHeuristic, k, GreedyRate):
    name = str(str(beamwidth_deg) + str(M) + str(users_per_beam) + str(user_rate))
    if Heuristic:
        name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str('SNR_k=' + str(k) + name)

    elif GreedyRate:
        name = str(name + 'GreedyRate')

    if Clustered:
        name = str(name + '_clustered')

    return name