import math

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

if beamwidth_b == math.radians(5):
    misalignment = {10: 1.78, 100: 1.53, 300: 1.37, 500: 1.25, 750: 1.16, 1000: 1.12}
    average_connections = {100: 8.65, 300: 4.98, 500: 3.31, 750: 2.27, 1000: 1.72}
    no_succes = {100: 0, 300: 0, 500: 0, 750: 0, 1000: 0}
    disconnected = {100: 0.0, 300: 0.0, 500: 0.0, 750: 0.0, 1000:0.0} # average disconnected users per simulation

elif beamwidth_b == math.radians(10):
    misalignment = {100: 2.05, 300: 1.88, 500: 1.79, 750: 1.83, 1000: 1.70}
    average_connections = {100: 3.77, 300: 2.35, 500: 1.62, 750: 1.13, 1000:1.00}
    no_succes = {100: 0, 300: 0, 500: 0, 750: 0, 1000: 0}
    disconnected = {100: 0.0596, 300: 0.20, 500: 0.316, 750: 0.57, 1000:  143.014} # average disconnected users per simulation

elif beamwidth_b == math.radians(15):
    misalignment = {100: 4.55, 300: 4.59, 500: 4.73, 750: 4.60, 1000: 4.32}
    average_connections = {100: 2.08, 300: 1.48, 500: 1.14, 750: 1.02, 1000:0.999}
    no_succes = {100: 0, 300: 0, 500: 0, 750: 0, 1000: 0}
    disconnected = {100: 6.15, 300: 23.67, 500: 59.07, 750: 209.08, 1000:  433.12} # average disconnected users per simulation

misalignment_user = {10: 1.78, 100: 1.53, 300: 1.37, 500: 1.25, 750: 1.16, 1000: 1.12}

Torus = True
