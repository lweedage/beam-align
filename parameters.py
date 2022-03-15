import math
from cycler import cycler
import matplotlib

matplotlib.rcParams['axes.prop_cycle'] = cycler('color', ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed'])
colors =  ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed', 'grey'] * 10

scenario = int(input('Scenario?'))
if scenario in [1, 4, 7, 10, 13, 16, 19, 22]:
    beamwidth_deg = 5
elif scenario in [2, 5, 8, 11, 14, 17, 20, 23]:
    beamwidth_deg = 10
else:
    beamwidth_deg = 15

if scenario in [1, 2, 3, 4, 5, 6]:
    users_per_beam = 1
elif scenario in [7, 8, 9, 10, 11, 12]:
    users_per_beam = 2
elif scenario in [13, 14, 15, 16, 17, 18]:
    users_per_beam = 5
elif scenario in [19, 20, 21, 22, 23, 24]:
    users_per_beam = 10

if scenario in [1, 2, 3, 7, 8, 9, 13, 14, 15, 19, 20, 21]:
    Penalty = True
else:
    Penalty = False

pi = math.pi
bs_of_interest = 0
radius = 50  # for triangular grid

xmin, xmax = 0, 200
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

xDelta = xmax - xmin
yDelta = ymax - ymin

beamwidth_u = math.radians(5)

beamwidth_b = math.radians(int(beamwidth_deg))

W = 1  # bandwidth

if Penalty:
    M = 100  # penalty on having disconnected users
else:
    M = 0

# users_per_beam = 2  # amount of users in a beam
# users_per_beam = int(input("Users per beam?"))

transmission_power = 10 ** 3.0  # 30 dB
noise_figure = 7.8
noise_power_db = -174 + 10 * math.log10(W * 10 ** 9) + noise_figure
noise = 10 ** (noise_power_db / 10)

BS_height = 10
user_height = 1.5
centre_frequency = 28e9
propagation_velocity = 3e8

SINR_min = 10 ** (-5 / 10)

directions_bs = range(int(2 * pi / beamwidth_b))
directions_u = range(int(2 * pi / beamwidth_u))


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

iterations = {50: 1, 100: 5000, 300: 1667, 500: 1000, 750: 667, 1000: 500}
# iterations = {50: 1, 100: 2500, 300: 834, 500: 500, 750: 334, 1000: 250}

if beamwidth_b == math.radians(5):
    if users_per_beam == 1:
        misalignment = {50: 1.78, 100: 5, 300: 2.14, 500: 1.87, 750: 1.69, 1000: 1.58}
    elif users_per_beam == 2:
        misalignment = {50: 1.78, 100: 5, 300: 1.77, 500: 1.43, 750: 1.26, 1000: 1.20} #updated
    elif users_per_beam == 5:
        misalignment = {50: 1.78, 100: 5, 300: 2.14, 500: 1.87, 750: 1.69, 1000: 1.58}
    elif users_per_beam == 10:
        misalignment = {50: 1.78, 100: 5, 300: 2.14, 500: 1.87, 750: 1.69, 1000: 1.58}

elif beamwidth_b == math.radians(10):
    if users_per_beam == 1:
        misalignment = {50: 1.78, 100: 5, 300: 2.14, 500: 1.87, 750: 1.69, 1000: 1.58}
    elif users_per_beam == 2:
        misalignment = {50: 1.78, 100: 5, 300: 1.77, 500: 1.43, 750: 1.26, 1000: 1.20}
    elif users_per_beam == 5:
        misalignment = {50: 1.78, 100: 5, 300: 2.14, 500: 1.87, 750: 1.69, 1000: 1.58}
    elif users_per_beam == 10:
        misalignment = {50: 1.78, 100: 5, 300: 2.14, 500: 1.87, 750: 1.69, 1000: 1.58}

elif beamwidth_b == math.radians(15):
    if users_per_beam == 1:
        misalignment = {50: 1.78, 100: 5, 300: 2.14, 500: 1.87, 750: 1.69, 1000: 1.58}
    elif users_per_beam == 2:
        misalignment = {50: 1.78, 100: 5, 300: 1.77, 500: 1.43, 750: 1.26, 1000: 1.20}
    elif users_per_beam == 5:
        misalignment = {50: 1.78, 100: 5, 300: 2.14, 500: 1.87, 750: 1.69, 1000: 1.58}
    elif users_per_beam == 10:
        misalignment = {50: 1.78, 100: 5, 300: 2.14, 500: 1.87, 750: 1.69, 1000: 1.58}


misalignment_user = {50: 1.78, 100: 2.47, 300: 1.75, 500: 1.40, 750: 1.21, 1000: 1.13}

Torus = True