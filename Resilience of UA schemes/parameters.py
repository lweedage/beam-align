import math
from cycler import cycler
import matplotlib

matplotlib.rcParams['axes.prop_cycle'] = cycler('color',
                                                ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen',
                                                 'OrangeRed'])
colors = ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed'] * 10

pi = math.pi
radius = 200  # for triangular grid

xmin, xmax = 0, 600
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

xmin, xmax = 0, 250
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 2

xDelta = xmax - xmin
yDelta = ymax - ymin

lambda_U = 250e-6  # number of users per square meter

beamwidth_u = math.radians(5)

# beamwidth_deg = input('Beamwidth BS?')
beamwidth_deg = 5
beamwidth_b = math.radians(int(beamwidth_deg))

W = 1  # bandwidth

transmission_power = 30  # in dB
noise = -174 + 10 * math.log10(W * 10 ** 9)

BS_height = 10
user_height = 1.5

centre_frequency = 28e9
propagation_velocity = 3e8

min_SINR = -math.inf  # in dB
min_SNR = -math.inf  # in dB

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

Torus = False
