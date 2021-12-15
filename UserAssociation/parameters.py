import math
import numpy as np

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
          '#17becf'] * 10

pi = math.pi

Plot_Interference = False
bs_of_interest = 0

xmin, xmax = 0, 50
ymin, ymax = 0, 50

xDelta = xmax - xmin
yDelta = ymax - ymin

number_of_users = 50

radius = 25  # for triangular grid

N_bs = 100  # number of connections per BS
N_user = 10  # number of connections per user

beamwidth_u = math.radians(5)
beamwidth_b = math.radians(5)

critical_distance = 50

W = 28  # bandwidth (Either 28 GHz or 73 GHz)

transmission_power = 10 ** 3.0  # 30 dB
noise = 10 ** 0.7
sigma = noise


d0 = 1
wavelength = 10.71 * 10 ** (-3)
k = (4 * pi * d0 / wavelength) ** 2

alpha_nlos = 4
alpha_los = 2

SINR_min = 10**(-0.5)

Interference = True

directions_bs = range(int(2 * pi / beamwidth_b))
directions_u = range(int(2 * pi / beamwidth_u))

def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3 / 4) * radius
    for i in range(0, int(xDelta / radius) + 1):
        for j in range(0, int(yDelta / dy) + 1):
            if i * radius + 0.5 * (j%2) * radius <= xmax and j * dy <= ymax:
                xbs.append(i * radius + 0.5 * (j % 2) * radius)
                ybs.append(j * dy)
    return xbs, ybs

x_bs, y_bs = initialise_graph_triangular(radius, xDelta, yDelta)
number_of_bs = len(x_bs)
