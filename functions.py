import numpy as np
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn
from parameters import *
import networkx as nx

np.random.seed(seed)

pi = math.pi

def user_coords(i):
    return (x_user[i], y_user[i])

def bs_coords(j):
    return (x_bs[j], y_bs[j])

def find_distance_list(user, xbs, ybs):
    x = np.minimum((user[0] - np.array(xbs)) % xDelta, (np.array(xbs) - user[0]) % xDelta)
    y = np.minimum((user[1] - np.array(ybs)) % yDelta, (np.array(ybs) - user[1]) % yDelta)
    return np.sqrt(x ** 2 + y ** 2)

def find_closest_bs(i):
    indices = find_distance_list(user_coords(i), x_bs, y_bs).argsort()
    return indices[0]

def find_gain(bore_1, bore_2, geo_1, geo_2, beamwidth):
    bore = find_bore(bore_1, bore_2, beamwidth)
    geo = find_geo(geo_1, geo_2)
    alpha = abs(bore - geo)
    if beamwidth/2 < alpha < 2*pi - beamwidth/2:
        return 10**((-0.4111 * np.log(beamwidth/pi * 180) - 10.579)/10)
    else:
        return 10**((20 * math.log10(1.6162/(math.sin(beamwidth/2))) - (3.01 * (2*alpha/beamwidth)**2))/10)

def find_beam(radians, beamwidth):
    angles = [beamwidth * i for i in range(int(-pi/beamwidth), int(pi/beamwidth))]
    min = math.inf
    for angle in angles:
        if abs(radians - angle) < min:
            min = abs(radians - angle)      # NOTE THAT WE NOW JUST CHOOSE THE FIRST ONE IF TWO ARE EVEN CLOSE
            preferred_angle = angle
    return preferred_angle

def find_bore(coord_1, coord_2, beamwidth):
    radians = find_geo(coord_1, coord_2)
    if Sectorized_Antennnas:
        angle = find_beam(radians, beamwidth)
        return angle
    else:
        return radians

def find_geo(coord_1, coord_2):
    dy = coord_2[1] - coord_1[1]
    dx = coord_2[0] - coord_1[0]
    radians = math.atan2(dy, dx)
    return radians

def find_interference(coords_i, coords_j, x):
    interference = 0
    for m in range(number_of_bs):
        coords_m = bs_coords(m)
        for k in range(number_of_users):
            coords_k = user_coords(k)
            if x[k, m] > 0.5:
                if not (coords_k == coords_i and coords_m == coords_j):
                    gain_bs = find_gain(coords_m, coords_k, coords_m, coords_i, beamwidth_b)
                    gain_user = find_gain(coords_i, coords_j, coords_i, coords_m, beamwidth_u)
                    path_los = path_loss(coords_i, coords_m)
                    interference += x[k, m] * gain_bs * gain_user * path_los
    return interference

def path_loss(user, bs):
    r = find_distance(user, bs)
    if r <= critical_distance:
        p_los = 1
    else:
        p_los = 0

    p_nlos = 1 - p_los
    if r > d0:
        l_los =  k * (r/d0) ** (-alpha_los)
        l_nlos = k * (r/d0)**(-alpha_nlos)
    else:
        l_los = k
        l_nlos = k
    return p_los * l_los + p_nlos * l_nlos

def find_distance(user, bs):
        return math.sqrt((user[0] - bs[0]) ** 2 + (user[1] - bs[1]) ** 2)

def find_C(i, x):
    for j in range(number_of_bs):
        if x[i,j] == 1:
            coords_i = user_coords(i)
            coords_j = bs_coords(j)
            power = find_gain(coords_i, coords_j, coords_j, coords_i, beamwidth_b) * find_gain(coords_i, coords_j, coords_i, coords_j, beamwidth_u) * path_loss(coords_i, coords_j)
            interference = find_interference(coords_i, coords_j, x)
            print(i, j, interference)
    return W * math.log(1 + power/(sigma + interference))

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
        colorlist.append('w')
        nodesize.append(20)
        labels[node] = f'BS{node}'
    for node in range(len(xu)):
        G.add_node(node + number_of_bs, x =xu[node], y = yu[node])
        colorlist.append('g')
        nodesize.append(1)
        labels[node + number_of_bs] = f'U{node}'
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