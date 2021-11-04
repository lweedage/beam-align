import math
import numpy as np

pi = math.pi

Fading = False
Beamforming = True
Sectorized_Antennnas = True
Hexagonal = False
Plot_Interference = False
bs_of_interest = 1

number_of_bs = 2
number_of_users = 3

alpha = 1

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

radius = 60  # for triangular grid

xmin, xmax = 0, 100
ymin, ymax = 0, 100

N_bs = 10        # number of connections per BS
N_user = 10      # number of connections per user

beamwidth_u = 2 * pi / N_user
beamwidth_b = 2 * pi / N_bs

x_bs, y_bs, x_user, y_user = find_coordinates(seed)
number_of_bs = len(x_bs)


critical_distance = 10000
wavelength = 10e-5

transmission_power = 10 ** 2.8  #28 dB
noise = 10 ** 0.7  #7 db
sigma = noise / transmission_power

W = 73e9      # bandwidth (Either 28 GHz or 73 GHz)

if W == 28e9:
    alpha_los = 61.4    #in dB
    beta_los = 2
    alpha_nlos = 72     # in dB
    beta_nlos = 2.92
elif W == 73e9:
    alpha_los = 69.8
    beta_los = 2
    alpha_nlos = 82.7
    beta_nlos = 2.69

k_los =  10**(alpha_los/(10 * beta_los))
k_nlos = 10**(alpha_nlos/(10 * beta_nlos))

if Fading:
    fading = np.random.gamma(1, 1, (number_of_users, number_of_bs))
else:
    fading = np.ones((number_of_users, number_of_bs))

SINR_min = 0


