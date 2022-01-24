import math
import numpy as np

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
          '#17becf'] * 10

Interference = False

pi = math.pi
bs_of_interest = 0
radius = 25  # for triangular grid

xmin, xmax = 0, 100
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

if Interference:
    xmax = 50
    ymax = math.sqrt(3 / 4) * 2 * radius

# print(math.sqrt(3 / 4) * 2 * radius * 3)

xDelta = xmax - xmin
yDelta = ymax - ymin

number_of_users = int(input('Number of users?'))

if Interference:
    number_of_users = number_of_users/(100 * math.sqrt(3 / 4) * 2 * radius * 3) * xDelta * yDelta
    number_of_users = int(math.ceil(number_of_users))
    print(number_of_users)

N_bs = 100  # number of connections per BS
N_user = 100  # number of connections per user

beamwidth_u = math.radians(5)
beamwidth_b = math.radians(5)

critical_distance = 50

W = 1  # bandwidth (Either 28 GHz or 73 GHz)

transmission_power = 10 ** 3.0  # 30 dB
noise = 10 ** 0.7
sigma = noise


d0 = 1
wavelength = 10.71 * 10 ** (-3)
k = (4 * pi * d0 / wavelength) ** 2

alpha_nlos = 4
alpha_los = 2

SINR_min = 10**(-0.5)


directions_bs = range(int(2 * pi / beamwidth_b))
directions_u = range(int(2 * pi / beamwidth_u))

def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3 / 4) * radius
    for i in range(0, int(xDelta / radius) + 1):
        for j in range(0, int(yDelta / dy) + 1):
            if i * radius + 0.5 * (j%2) * radius < xmax and j * dy < ymax:
                xbs.append(i * radius + 0.5 * (j % 2) * radius)
                ybs.append(j * dy)
    return xbs, ybs

x_bs, y_bs = initialise_graph_triangular(radius, xDelta, yDelta)
number_of_bs = len(x_bs)

iterations = {100:5000, 300:1667, 500:1000, 750:667, 1000:500}
if Interference:
    iterations = {17: 5000, 51: 1667, 84: 1000, 126: 667}

misalignment = {100: 1.78, 300: 1.60, 500: 1.47, 750:1.34}

