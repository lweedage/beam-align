import numpy as np
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn
from parameters import *
import networkx as nx

pi = math.pi

def user_coords(i, x_user, y_user):
    return (x_user[i], y_user[i])

def bs_coords(j):
    return (x_bs[j], y_bs[j])

def find_distance_list(user, xbs, ybs):
    x = (user[0] - np.array(xbs))
    y = (user[1] - np.array(ybs))
    return np.sqrt(x ** 2 + y ** 2)

def find_closest_bs(i):
    indices = find_distance_list(user_coords(i), x_bs, y_bs).argsort()
    return indices[0]

def find_beam_number(radians, beamwidth):
    angles = [beamwidth * i for i in range(int(-pi/beamwidth), int(pi/beamwidth))]
    min = math.inf
    for i in range(int(2*pi/beamwidth)):
        if abs(radians - angles[i]) < min:
            min = abs(radians - angles[i])      # NOTE THAT WE NOW JUST CHOOSE THE FIRST ONE IF TWO ARE EVEN CLOSE
            preferred_angle = i
    return preferred_angle

def find_interference(coords_i, coords_j, x):
    interference = 0
    for m in range(number_of_bs):
        coords_m = bs_coords(m)
        for k in range(number_of_users):
            coords_k = user_coords(k)
            if x[k, m] > 0.5:
                if not (coords_k == coords_i and coords_m == coords_j):
                    interference += (transmission_power * gain_bs[i,k, m] * gain_user[i,j,m] / path_loss[i, m])
    return interference

def find_initial_interference(i, j, k, m):
    if not (k == i and m == j):
        gain_bs = find_gain(m, k, m, i, beamwidth_b)
        gain_user = find_gain(i, j, i, m, beamwidth_u)
        path_los = find_path_loss(i, m)
        return gain_bs * gain_user / path_los
    else:
        return 0

def find_SINR(i, j, x):
    power = transmission_power * gain_bs[i, i, j] * gain_user[i, j, j] / path_loss[i,j]
    interference = find_interference(coords_i, coords_j, x)
    return 10 * math.log10(power/(sigma + interference))

def find_SNR(i, j):
    power = transmission_power  * gain_bs[i, i, j] * gain_user[i, j, j]  / path_loss[i,j]
    return 10 * math.log10(power/(sigma))

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

def find_C(i, j, x):
    C = 0
    if x[i,j] == 1:
        coords_i = user_coords(i)
        coords_j = bs_coords(j)
        power = transmission_power * gain_bs[i, i, j] * gain_user[i, j, j]  / path_loss[i,j]
        interference = find_interference(coords_i, coords_j, x)
        C += 1e9 * math.log(1 + power/(sigma + interference))
    return C

def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3 / 4) * radius
    for i in range(0, int(xDelta / radius) + 1):
        for j in range(0, int(yDelta / dy) + 1):
            if i * radius + 0.5 * (j%2) * radius <= xmax and j * dy <= ymax:
                xbs.append(i * radius + 0.5 * (j % 2) * radius)
                ybs.append(j * dy)
    return xbs, ybs

def find_coordinates():
    x_user, y_user = np.random.uniform(xmin, xmax, number_of_users), np.random.uniform(ymin, ymax, number_of_users)
    return x_user, y_user

def make_graph(xbs, ybs, xu, yu, x, number_of_users):
    G = nx.Graph()
    colorlist = list()
    nodesize = list()
    edgesize = list()
    edgecolor = list()
    labels = {}
    number_of_bs = len(xbs)
    for node in range(number_of_bs):
        G.add_node(node, x = xbs[node], y = ybs[node])
        colorlist.append(colors[node])
        nodesize.append(30)
        labels[node] = f'BS{node}'
    for node in range(number_of_users):
        G.add_node(node + number_of_bs, x = xu[node], y = yu[node])
        colorlist.append('w')
        nodesize.append(10)
        labels[node + number_of_bs] = f'{node}'
    for bs in range(number_of_bs):
        for user in range(number_of_users):
            if x[user, bs] > 0.1:
                G.add_edge(user + number_of_bs, bs)
                edgesize.append(2)
                edgecolor.append(colors[bs])
    return G, colorlist, nodesize, edgesize, labels, edgecolor


def draw_graph(G, colorlist, nodesize, edgesize, labels, ax, color, edgecolor):
    pos = dict()
    for node in G.nodes():
        pos[node] = (nx.get_node_attributes(G, 'x')[node], nx.get_node_attributes(G, 'y')[node])
    nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_size=nodesize,
                           node_color=colorlist, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color=edgecolor, alpha=0.5, width=edgesize)
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color = color)

def fairness(x):
    return (sum(x))**2 / (len(x)* sum([i**2 for i in x]))

def plot_SINR(SINR, label, color):
    sorted_SINR = np.sort(SINR)
    # sorted_SNR = np.sort(SNR)

    plt.step(sorted_SINR[::-1], np.arange(sorted_SINR.size)/number_of_users, label = str(label), color = color)
    # plt.step(sorted_SNR[::-1], np.arange(sorted_SNR.size)/number_of_users, '--', label = str(label + ' SNR'), color = color)

    plt.xlabel('SINR threshold (dB)')
    plt.ylabel('Percentage of connected users (ecdf)')
    plt.legend()

def find_distance_allbs(user, xbs, ybs):
    xu, yu = user[0], user[1]
    xx = xu - xbs
    yy = yu - ybs
    return np.sqrt(xx ** 2 + yy ** 2)
