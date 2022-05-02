import math
from cycler import cycler
import matplotlib
import numpy as np

matplotlib.rcParams['axes.prop_cycle'] = cycler('color',
                                                ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen',
                                                 'OrangeRed'])
colors = ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed', 'grey'] * 100


def find_scenario(scenario):
    if scenario in [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31]:
        beamwidth_deg = 5
    elif scenario in [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32]:
        beamwidth_deg = 10
    else:
        beamwidth_deg = 15

    if scenario in [1, 2, 3, 4, 5, 6]:
        users_per_beam = 1
    elif scenario in [7, 8, 9, 10, 11, 12]:
        users_per_beam = 2
    elif scenario in [13, 14, 15, 16, 17, 18]:
        users_per_beam = 5
    elif scenario in [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]:
        users_per_beam = 10
    elif scenario in [31, 32, 33]:
        users_per_beam = 1000
    else:
        users_per_beam = False

    if scenario in [1, 2, 3, 7, 8, 9, 13, 14, 15, 19, 20, 21, 25, 26, 27, 31, 32, 33]:
        Penalty = True
    else:
        Penalty = False

    if scenario in [25, 26, 27, 28, 29, 30]:
        Clustered = True
    else:
        Clustered = False

    return beamwidth_deg, users_per_beam, Penalty, Clustered


scenario = int(input('Scenario?'))
# scenario = 1
beamwidth_deg, users_per_beam, Penalty, Clustered = find_scenario(scenario)

pi = math.pi
bs_of_interest = 10
radius = 200  # for triangular grid

xmin, xmax = 0, 800
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

xDelta = xmax - xmin
yDelta = ymax - ymin

# users = [int(i / (xDelta / 1000 * yDelta / 1000)) for i in [100, 250, 500, 750, 1000]]
users = [120, 300, 600, 900, 1200]

beamwidth_u = 5
beamwidth_b = beamwidth_deg

W = 200  # in MHz  # bandwidth

if Penalty:
    M = 10000  # penalty on having disconnected users
else:
    M = 0

transmission_power = (10 ** 2.0) / (360 / beamwidth_deg)  # 30 dB
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

iterations = {120: 10, 300: 10, 600: 10, 900: 10, 1200: 10}

if beamwidth_b == 5:
    misalignment_user = {120: 1.6954438876808926, 300: 1.5701307680072651, 600: 1.3879042182645298, 900: 1.2993768076164862, 1200: 1.3226491038698536}
    misalignment = {120: 1.6954438876808926, 300: 1.5701307680072651, 600: 1.3879042182645298, 900: 1.2993768076164862, 1200: 1.3226491038698536}



elif beamwidth_b == 10:
    misalignment_user = {120: 1.983301431779446, 300: 1.8487323553512567, 600: 1.6725556449244827, 900: 1.5969519971850155, 1200: 1.5526005066403505}
    misalignment = {120: 2.0910422029605362, 300: 1.9471764082347576, 600: 1.682219442073332, 900: 1.6078089333689214, 1200: 1.552600506640351}


elif beamwidth_b == 15:
    misalignment_user = {120: 1.886641564397087, 300: 1.7230666266682544, 600: 1.7193806593953058, 900: 1.71620737231353, 1200: 1.6750856613277922}
    misalignment = {120: 5.695593258318874, 300: 5.367271166181774, 600: 4.964976488363763, 900: 4.972467823106814, 1200: 4.3530105659089084}



RateRequirement = True
user_rate = 500  # Mbps

Torus = True

fading = np.random.normal(0, 4, (3007, number_of_bs))
