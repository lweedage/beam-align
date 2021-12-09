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

number_of_users = 15

radius = 25  # for triangular grid

N_bs = 100  # number of connections per BS
N_user = 10  # number of connections per user

beamwidth_u = math.radians(5)
beamwidth_b = math.radians(5)

def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3 / 4) * radius
    for i in range(0, int(xDelta / radius) + 1):
        for j in range(0, int(yDelta / dy) + 1):
            if i * radius + 0.5 * (j%2) * radius <= xmax and j * dy <= ymax:
                xbs.append(i * radius + 0.5 * (j % 2) * radius)
                ybs.append(j * dy)
    return xbs, ybs

def find_coordinates(seed=2):
    np.random.seed(seed)
    x_bs, y_bs = initialise_graph_triangular(radius, xmax, ymax)
    x_user, y_user = np.random.uniform(xmin, xmax, number_of_users), np.random.uniform(ymin, ymax, number_of_users)
    return x_bs, y_bs, x_user, y_user

x_bs, y_bs, x_user, y_user = find_coordinates()
# x_bs, y_bs = [0, 10], [5, 5]
number_of_bs = len(x_bs)

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

SINR_min = 0.1

directions_bs = range(int(2 * pi / beamwidth_b))
directions_u = range(int(2 * pi / beamwidth_u))

users = range(number_of_users)
base_stations = range(number_of_bs)

number_of_interferers = number_of_bs
# number_of_interferers = 0

# all necessary functions
def user_coords(i):
    return (x_user[i], y_user[i])

def bs_coords(j):
    return (x_bs[j], y_bs[j])

def find_gain(bore_1, bore_2, geo_1, geo_2, beamwidth_ml):
    bore = find_bore(bore_1, bore_2, beamwidth_ml)
    geo = find_geo(geo_1, geo_2)
    alpha = math.degrees(abs(bore-geo))
    if alpha > 180:
        alpha = alpha - 360
    beamwidth_ml = math.degrees(beamwidth_ml)
    w = beamwidth_ml / 2.58
    G0 = 20 * math.log10(1.62 / math.sin(math.radians(w / 2)))

    if 0 <= abs(alpha) <= beamwidth_ml / 2:
        return 10 ** ((G0 - 3.01 * (2 * alpha / w) ** 2)/10)
    else:
        return 10**((-0.4111 * math.log(math.degrees(w)) - 10.579)/10)

def find_bore(coord_1, coord_2, beamwidth):
    radians = find_geo(coord_1, coord_2)
    angle = find_beam(radians, beamwidth)
    return angle

def find_geo(coord_1, coord_2):
    dy = coord_2[1] - coord_1[1]
    dx = coord_2[0] - coord_1[0]
    radians = math.atan2(dy, dx)
    return radians

def find_beam(radians, beamwidth):
    angles = [beamwidth * i for i in range(int(-pi/beamwidth), int(pi/beamwidth) + 1)]
    min = math.inf
    for angle in angles:
        if abs(radians - angle) <= min:
            min = abs(radians - angle)      # NOTE THAT WE NOW JUST CHOOSE THE FIRST ONE IF TWO ARE EVEN CLOSE
            preferred_angle = angle
    return preferred_angle

def find_path_loss(user, bs):
    r = find_distance(user, bs)
    if r <= critical_distance:
        p_los = 1
    else:
        p_los = 0

    p_nlos = 1 - p_los
    if r > d0:
        l_los =  k * (r/d0) ** (alpha_los)
        l_nlos = k * (r/d0) ** (alpha_nlos)
    else:
        l_los = k
        l_nlos = k
    return p_los * l_los + p_nlos * l_nlos

def find_distance(user, bs):
    return math.sqrt((user[0] - bs[0]) ** 2 + (user[1] - bs[1]) ** 2)

gain_bs = np.zeros((number_of_users, number_of_users, number_of_bs))
gain_user = np.zeros((number_of_users, number_of_bs, number_of_bs))
power = np.zeros((number_of_users, number_of_bs))
path_loss = np.zeros((number_of_users, number_of_bs))
interference = np.zeros((number_of_users, number_of_bs, number_of_users, number_of_bs))

# calculating the gain, path_loss and interference for every user-bs pair
for i in users:
    coords_i = user_coords(i)
    for j in base_stations:
        coords_j = bs_coords(j)
        path_loss[i,j] = find_path_loss(coords_i, coords_j)

for i in users:
    coords_i = user_coords(i)
    for j in base_stations:
        coords_j = bs_coords(j)
        for m in base_stations:
            coords_m = bs_coords(m)
            for k in users:
                coords_k = user_coords(k)
                gain_bs[i, k, m] = find_gain(coords_m, coords_k, coords_m, coords_i, beamwidth_b)
                gain_user[i, j, m] = find_gain(coords_i, coords_j, coords_i, coords_m, beamwidth_u)
                if not (i == k and j == m) and number_of_interferers > 0:
                    interference[i, j, k, m] = transmission_power * gain_bs[i, k, m] * gain_user[i, j, m] / \
                                               path_loss[i, m]
        power[i, j] = transmission_power * gain_bs[i, i, j] * gain_user[i, j, j] / path_loss[i, j]

