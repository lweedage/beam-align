import math
import numpy as np

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
          '#17becf']

pi = math.pi

OneConnection = True
Closest = True

Beamforming = True
Sectorized_Antennnas = False
Hexagonal = True

Plot_Interference = False
bs_of_interest = 2

xmin, xmax = 0, 100
ymin, ymax = 0, 100

xDelta = xmax - xmin
yDelta = ymax - ymin

number_of_bs = 3
number_of_users = 4
print(number_of_users)

alpha = 1   #alpha-fair utility - alpha = 0 is sum, alpha = 1 is log, alpha = 2 is fair

def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3/4) * radius
    for i in range(0, int(xDelta/radius) + 1):
        for j in range(0, int(yDelta/dy) + 1):
            xbs.append(i*radius + 0.5*(j%2) * radius)
            ybs.append(j*dy)
    return xbs, ybs

def find_coordinates(seed):
    np.random.seed(seed)
    if Hexagonal:
        x_bs, y_bs = initialise_graph_triangular(radius, xmax, ymax)
    else:
        x_bs, y_bs = np.random.uniform(xmin, xmax, number_of_bs), np.random.uniform(xmin, xmax, number_of_bs)
    x_user, y_user = np.random.uniform(xmin, xmax, number_of_users), np.random.uniform(ymin, ymax, number_of_users)
    return x_bs, y_bs, x_user, y_user

seed = 3
np.random.seed(seed)

radius = 75  # for triangular grid

N_bs = 72        # number of connections per BS
N_user = 72      # number of connections per user

beamwidth_u = 2 * pi / N_user
beamwidth_b = 2 * pi / N_bs

x_bs, y_bs, x_user, y_user = find_coordinates(seed)
x_bs, y_bs = [25, 75, 50], [25, 25, 25 + math.sqrt(1875)]
number_of_bs = len(x_bs)

critical_distance = 100

transmission_power = 10 ** 2.8  #28 dB
noise = 10 ** 0.7  #7 db
sigma = noise / transmission_power

W = 28e9        # bandwidth (Either 28 GHz or 73 GHz)

d0 = 5
wavelength = 10.71 * 10*(-3)
k = (4 * pi * d0/ wavelength)**2
alpha_nlos = 5.7
alpha_los = 2

SINR_min = 0