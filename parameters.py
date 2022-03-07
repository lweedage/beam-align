import math
from cycler import cycler
import matplotlib

matplotlib.rcParams['axes.prop_cycle'] = cycler('color', ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed'])
colors =  ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed'] * 10

pi = math.pi
bs_of_interest = 0
radius = 50  # for triangular grid

xmin, xmax = 0, 200
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

xDelta = xmax - xmin
yDelta = ymax - ymin

beamwidth_u = math.radians(5)

# beamwidth_deg = input('Beamwidth BS?')
beamwidth_deg = 10
beamwidth_b = math.radians(int(beamwidth_deg))

W = 1  # bandwidth

M = 100  # penalty on having disconnected users
users_per_beam = 2  # amount of users in a beam

transmission_power = 10 ** 3.0  # 30 dB
noise_power_db = -174 + 10 * math.log10(W * 10 ** 9)
noise = 10 ** (noise_power_db / 10)

Model_3GPP = True

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
iterations = {50: 1, 100: 500, 300: 500, 500: 500, 750: 250, 1000: 250}

if beamwidth_b == math.radians(5):
    misalignment = {50: 1.78, 100: 2.47, 300: 1.75, 500: 1.40, 750: 1.21, 1000: 1.13}
    average_connections = {100: 12.49, 300: 5.58, 500: 3.43, 750: 2.30, 1000: 1.73}
    no_succes = {100: 0, 300: 0, 500: 0, 750: 0, 1000: 0}
    disconnected = {100: 0.0, 300: 0.0, 500: 0.0, 750: 0.0, 1000: 0.0}  # average disconnected users per simulation

elif beamwidth_b == math.radians(10):
    misalignment = {100: 4.74, 300: 2.92, 500: 2.22, 750: 2.03, 1000: 1.80}
    average_connections = {100: 7.89, 300: 2.87, 500: 1.73, 750: 1.15, 1000: 1.00}
    no_succes = {100: 0, 300: 0, 500: 0, 750: 0, 1000: 0}
    disconnected = {100: 0.0, 300: 0.0, 500: 0.0, 750: 0.0, 1000: 136.012}  # average disconnected users per simulation

elif beamwidth_b == math.radians(15):
    misalignment = {100: 6.74, 300: 5.18, 500: 5.03, 750: 4.78, 1000: 4.38}
    average_connections = {100: 5.57, 300: 1.92, 500: 1.15, 750: 1.0, 1000: 1.0}
    disconnected = {100: 0, 300: 0, 500: 0, 750: 174.00, 1000: 424.0}  # average disconnected users per simulation

misalignment_user = {50: 1.78, 100: 2.47, 300: 1.75, 500: 1.40, 750: 1.21, 1000: 1.13}

Torus = True
