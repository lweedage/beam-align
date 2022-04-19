import math
import functions as f
import numpy as np
import matplotlib.pyplot as plt

radius = 50  # for triangular grid

xmin, xmax = 0, 400
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 5

xDelta = xmax - xmin
yDelta = ymax - ymin

def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3 / 4) * radius
    for i in range(0, int(xDelta / radius) + 1):
        for j in range(0, int(yDelta / dy) + 1):
            if i * radius + 0.5 * (j % 2) * radius < xmax and j * dy < ymax:
                xbs.append(i * radius + 0.5 * (j % 2) * radius)
                ybs.append(j * dy)
    return xbs, ybs

def find_closest_bs(user, x_bs, y_bs):
    # on a torus
    x = np.minimum((x_bs - user[0]) % xDelta, (user[0] - x_bs) % xDelta)
    y = np.minimum((y_bs - user[1]) % yDelta, (user[1] - y_bs) % yDelta)
    return np.argsort(x ** 2 + y ** 2)[0]

def find_closest_bs_distance(user, x_bs, y_bs):
    # on a torus
    x = np.minimum((x_bs - user[0]) % xDelta, (user[0] - x_bs) % xDelta)
    y = np.minimum((y_bs - user[1]) % yDelta, (user[1] - y_bs) % yDelta)
    return np.sort(np.sqrt(x ** 2 + y ** 2))[0]

def find_gain(alpha, beamwidth_ml):
    if alpha > 180:
        alpha = alpha - 360
    w = beamwidth_ml / 2.58
    G0 = 20 * math.log10(1.6162 / math.sin(math.radians(w / 2)))
    if 0 <= abs(alpha) <= beamwidth_ml / 2:
        return G0 - 3.01 * (2 * alpha / w) ** 2
    else:
        return -0.4111 * math.log(np.radians(w)) - 10.579

x_bs, y_bs = initialise_graph_triangular(radius, xDelta, yDelta)
number_of_bs = len(x_bs)

number_of_users = 10000
lambda_u = number_of_users/(xDelta * yDelta)
x_user, y_user = f.find_coordinates(number_of_users)

distance = []
misalignment = []
gains = []

beamwidth = 5
theta_3db = beamwidth / 2.58

for u in range(len(x_user)):
    bs = find_closest_bs((x_user[u], y_user[u]), x_bs, y_bs)
    distance.append(find_closest_bs_distance((x_user[u], y_user[u]), x_bs, y_bs))
    # misalignment.append(f.find_misalignment((x_user[u], y_user[u]), (x_bs[bs], y_bs[bs]), beamwidth=np.radians(5)))
    # misalignment.append(f.find_misalignment((x_bs[bs], y_bs[bs]), (x_user[u], y_user[u]), beamwidth=np.radians(15)))
    coords_i = (x_user[u], y_user[u])
    coords_j = (x_bs[bs], y_bs[bs])

    alpha = f.find_misalignment(coords_j, coords_i, beamwidth)
    gains.append(find_gain(alpha, beamwidth))

misalignments = np.arange(-2*beamwidth, 2*beamwidth, 0.01)
x = np.arange(0, 40, 1)

def pdf(x, beamwidth, theta_3db):
    y = []
    for i in x:
        z = math.sqrt((20 * math.log10(1.6162/(math.sin(np.radians(theta_3db/2)))) - i)/3.01) * theta_3db/2
        # y.append(1 - (z+beamwidth/2)/beamwidth)
        if z <= beamwidth/2:
            y.append(1 - (2*z)/beamwidth)
        else:
            y.append(0)
    return y

def distance_cdf(r, radius):
    tanshit = math.atanh(math.sqrt(2*math.pi) * (2/math.sqrt(3)) / 3**(3/4)) - math.atanh(math.sqrt(2*math.pi)  / 3**(3/4))
    z = radius**2 /2 + (3**(1/4) * (math.pi - 2*math.sqrt(3)))/(2*math.sqrt(2*math.pi)) * radius * tanshit
    return r**2 / 2 * 1/z


xx = np.arange(0, 30, 1)

fig, ax = plt.subplots()
plt.hist(distance, bins = 25, density = True, cumulative= True)
plt.plot(xx, [(i/25)**2 for i in xx]) #on a circle
plt.plot(xx, [distance_cdf(i, radius = 25) for i in xx]) #on a circle

# plt.hist(misalignment, bins = 25, density = True)
# plt.hist(gains, bins = 25, density = True, cumulative=True)
# plt.plot(x, pdf(x, beamwidth, theta_3db))
# plt.xlim((0,1))
# plt.plot()

# plt.plot(x, [math.exp(-lambda_u * math.pi * i**2)/(math.pi * i**2) for i in x])
plt.show()

