import math
import numpy as np

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
          '#17becf'] * 10

pi = math.pi
bs_of_interest = 0
radius = 25  # for triangular grid

xmin, xmax = 0, 100
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

xDelta = xmax - xmin
yDelta = ymax - ymin


N_bs = 100  # number of connections per BS
N_user = 100  # number of connections per user

beamwidth_u = math.radians(5)
beamwidth_b = math.radians(5)

W = 1  # bandwidth

transmission_power = 10 ** 3.0  # 30 dB
noise = 10 ** 0.7

Model_3GPP = True

BS_height = 10
user_height = 1.5
centre_frequency = 28e9
propagation_velocity = 3e8

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

iterations = {50: 1, 100: 5000, 300: 1667, 500: 1000, 750: 667, 1000: 500}

if beamwidth_b == math.radians(5):
    misalignment = {10: 1.78, 100: 1.78, 300: 1.60, 500: 1.47, 750: 1.34, 1000: 1.28}

elif beamwidth_b == math.radians(10):
    misalignment = {100: 2.96, 300: 2.77, 500: 2.72, 750: 2.87, 1000: 2.87}

elif beamwidth_b == math.radians(15):
    misalignment = {100: 5.24, 300: 5.32, 500: 5.32, 750: 5.32, 1000: 5.32}

misalignment_user = {10: 1.78, 100: 1.78, 300: 1.60, 500: 1.47, 750: 1.34, 1000: 1.28}

Torus = True

