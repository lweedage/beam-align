import math
import numpy as np

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

seed = 0
np.random.seed(seed)

radius = 10  # for triangular grid

W = 10      # bandwidth

epsilon = 0.1


xmin, xmax = 0, 10
ymin, ymax = 0, 10

beamwidth_u = math.radians(30)
beamwidth_b = math.radians(30)


Hexagonal = False
number_of_bs = 2
number_of_timeslots = 1
number_of_users = 2

x_bs, y_bs, x_user, y_user = find_coordinates(seed)

number_of_bs = len(x_bs)

critical_distance = 100

K_los = 1
K_nlos = 1
alpha_los = 1
alpha_nlos = 1

# fading = np.random.gamma(0.1, 1, (number_of_users, number_of_bs))
fading = np.ones((number_of_users, number_of_bs))

sigma = 1

SINR_min = 0.01

N_bs = 5        # number of connections per BS
N_user = 5      # number of connections per user

print(x_bs, y_bs)
print(x_user, y_user)