import math
import numpy as np

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
          '#17becf'] * 10

pi = math.pi

OneConnection = False
Closest = False

Hexagonal = True

Plot_Interference = False
bs_of_interest = 0

xmin, xmax = 0, 25
ymin, ymax = 0, 25

xDelta = xmax - xmin
yDelta = ymax - ymin


number_of_users = 10


def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3 / 4) * radius
    for i in range(0, int(xDelta / radius) + 1):
        for j in range(0, int(yDelta / dy) + 1):
            xbs.append(i * radius + 0.5 * (j % 2) * radius)
            ybs.append(j * dy)
    return xbs, ybs


def find_coordinates(seed=2):
    np.random.seed(seed)
    if Hexagonal:
        x_bs, y_bs = initialise_graph_triangular(radius, xmax, ymax)
    else:
        x_bs, y_bs = np.random.uniform(xmin, xmax, number_of_bs), np.random.uniform(xmin, xmax, number_of_bs)
    x_user, y_user = np.random.uniform(xmin, xmax, number_of_users), np.random.uniform(ymin, ymax, number_of_users)
    return x_bs, y_bs, x_user, y_user


radius = 25  # for triangular grid

N_bs = 100  # number of connections per BS
N_user = 100  # number of connections per user

beamwidth_u = math.radians(5)
beamwidth_b = math.radians(5)

x_bs, y_bs, x_user, y_user = find_coordinates()
# x_bs, y_bs = [10], [10]

number_of_bs = len(x_bs)

critical_distance = 50

transmission_power = 10 ** 3.5  # 35 dB
noise = 10 #28e9 * 10**(-16.4)  # from Elshaer,2016
print(noise)
sigma = noise

W = 28  # bandwidth (Either 28 GHz or 73 GHz)

d0 = 1
wavelength = 10.71 * 10 ** (-3)

k = (4 * pi * d0 / wavelength) ** 2

alpha_nlos = 4
alpha_los = 2

SINR_min = 10**(0.1)

directions_bs = range(int(2 * pi / beamwidth_b))
directions_u = range(int(2 * pi / beamwidth_u))
