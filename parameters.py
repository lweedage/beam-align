import math
import numpy as np

pi = math.pi

Fading = False
Beamforming = True
Hexagonal = False

number_of_bs = 3
number_of_users = 5

alpha = 0

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

W = 10      # bandwidth

epsilon = 0.1


xmin, xmax = 0, 50
ymin, ymax = 0, 50

beamwidth_u = math.radians(10)
beamwidth_b = math.radians(10)


x_bs, y_bs, x_user, y_user = find_coordinates(seed)

number_of_bs = len(x_bs)

critical_distance = 10
wavelength = 10e-6

transmission_power = 10*(4)

K_los =  1 #(wavelength / 4* pi)**2
K_nlos =  K_los


alpha_los = 1.5
alpha_nlos = 1.5

if Fading:
    fading = np.random.gamma(1, 1, (number_of_users, number_of_bs))
else:
    fading = np.ones((number_of_users, number_of_bs))

sigma = 1

SINR_min = 0

N_bs = 10        # number of connections per BS
N_user = 10      # number of connections per user
