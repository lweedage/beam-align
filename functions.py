import numpy as np
import math
import matplotlib.pyplot as plt
import numpy.random
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

def find_beam_number(radians, beamwidth):
    angles = [beamwidth * i for i in range(int(-pi/beamwidth), int(pi/beamwidth))]
    min = math.inf
    for i in range(int(2*pi/beamwidth)):
        if abs(radians - angles[i]) < min:
            min = abs(radians - angles[i])      # NOTE THAT WE NOW JUST CHOOSE THE FIRST ONE IF TWO ARE EVEN CLOSE
            preferred_angle = i
    return preferred_angle

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
    if Torus:
        coord_1, coord_2 = find_modified_coords(coord_1, coord_2)

    dy = coord_2[1] - coord_1[1]
    dx = coord_2[0] - coord_1[0]
    radians = math.atan2(dy, dx)
    return radians

def find_modified_coords(coord_1, coord_2):
    (x_1, y_1) = coord_1
    (x_2, y_2) = coord_2

    if (max(coord_2[0], coord_1[0]) - min(coord_2[0], coord_1[0])) > (
            min(coord_2[0], coord_1[0]) - max(coord_2[0], coord_1[0])) % xDelta:
        if coord_2[0] > coord_1[0]:
            x_2 = coord_2[0] - xDelta
        else:
            x_1 = coord_1[0] - xDelta

    if (max(coord_2[1], coord_1[1]) - min(coord_2[1], coord_1[1])) > (
            min(coord_2[1], coord_1[1]) - max(coord_2[1], coord_1[1])) % yDelta:
        if coord_2[1] > coord_1[1]:
            y_2 = coord_2[1] - yDelta
        else:
            y_1 = coord_1[1] - yDelta

    return (x_1, y_1), (x_2, y_2)

def plot_modified_coords(coord_1, coord_2):
    (x_1, y_1) = coord_1
    (x_2, y_2) = coord_2

    (x_1e, y_1e) = coord_1
    (x_2e, y_2e) = coord_2

    if (max(coord_2[0], coord_1[0]) - min(coord_2[0], coord_1[0])) > (
            min(coord_2[0], coord_1[0]) - max(coord_2[0], coord_1[0])) % xDelta:
        if coord_2[0] > coord_1[0]:
            x_2 = coord_2[0] - xDelta
            x_1e = coord_1[0] + xDelta
        else:
            x_1 = coord_1[0] - xDelta
            x_2e = coord_2[0] + xDelta

    if (max(coord_2[1], coord_1[1]) - min(coord_2[1], coord_1[1])) > (
            min(coord_2[1], coord_1[1]) - max(coord_2[1], coord_1[1])) % yDelta:
        if coord_2[1] > coord_1[1]:
            y_2 = coord_2[1] - yDelta
            y_1e = coord_1[1] + yDelta
        else:
            y_1 = coord_1[1] - yDelta
            y_2e = coord_2[1] + yDelta

    return (x_1, y_1), (x_2, y_2), (x_1e, y_1e), (x_2e, y_2e),

def find_beam(radians, beamwidth):
    angles = [beamwidth * i for i in range(int(-pi/beamwidth), int(pi/beamwidth))]
    min = math.inf
    for angle in angles:
        if abs(radians - angle) <= min:
            min = abs(radians - angle)      # NOTE THAT WE NOW JUST CHOOSE THE FIRST ONE IF TWO ARE EVEN CLOSE
            preferred_angle = angle
    return preferred_angle

def find_misalignment(coord_1, coord_2, beamwidth):
    return find_geo(coord_1, coord_2) - find_bore(coord_1, coord_2, beamwidth)

def find_path_loss_los(user, bs, SF = 0):
    r = find_distance_3D(user, bs)
    breakpoint_distance = 4 * (BS_height - 1) * (user_height - 1) * centre_frequency / propagation_velocity
    if r <= breakpoint_distance:
        path_loss_db = 32.4 + 21 * math.log10(r) + 20 * math.log10(centre_frequency / 1e9) + SF
        path_loss = 10 ** (path_loss_db / 10)

    return path_loss

def find_path_loss(user, bs):
    p_los = probability_los(user, bs)
    p = np.random.uniform(0, 1)
    if p <= p_los:
        PL = find_path_loss_los(user, bs, SF = np.random.normal(0, 4))
    else:
        PL = find_path_loss_nlos(user, bs, SF = np.random.normal(0, 7.82))
    return PL

def probability_los(user, bs):
    dist = find_distance(user, bs)
    if dist <= 18:
        return 1
    else:
        return 18/dist + (1 - 18/dist) * math.exp(-dist/36)

def find_path_loss_nlos(user, bs, SF):
    distance_3D = find_distance_3D(user, bs)
    PL_nlos = 35.3 * math.log10(distance_3D) + 22.4 + 21.3*math.log10(centre_frequency/1e9) - 0.3*(user_height - 1.5) + SF
    PL_nlos = 10 **(PL_nlos/10)
    return PL_nlos

def find_distance(user, bs):
    if Torus:
        # on a torus
        x = np.minimum((bs[0] - user[0]) % xDelta, (user[0] - bs[0]) % xDelta)
        y = np.minimum((bs[1] - user[1]) % yDelta, (user[1] - bs[1]) % yDelta)
    else:
        x = bs[0] - user[0]
        y = bs[1] - user[1]
    return np.sqrt(x ** 2 + y ** 2)

def find_distance_3D(user, bs):
    r = find_distance(user, bs)
    user_height = 1.5
    BS_height = 10
    return np.sqrt(r ** 2 + (BS_height - user_height) ** 2)

def find_distance_all_bs(user):
    if Torus:
        # on a torus
        x = np.minimum((x_bs - user[0]) % xDelta, (user[0] - x_bs) % xDelta)
        y = np.minimum((y_bs - user[1]) % yDelta, (user[1] - y_bs) % yDelta)
    else:
        x = x_bs - user[0]
        y = y_bs - user[1]
    return np.sqrt(x ** 2 + y ** 2)

def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3 / 4) * radius
    for i in range(0, int(xDelta / radius) + 1):
        for j in range(0, int(yDelta / dy) + 1):
            if i * radius + 0.5 * (j%2) * radius <= xmax and j * dy <= ymax:
                xbs.append(i * radius + 0.5 * (j % 2) * radius)
                ybs.append(j * dy)
    return xbs, ybs

def find_coordinates(number_of_users):
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

def find_distance_allbs(user, xbs, ybs):
    xu, yu = user[0], user[1]
    xx = xu - xbs
    yy = yu - ybs
    return np.sqrt(xx ** 2 + yy ** 2)

def find_capacity(opt_x, x_user, y_user):
    per_user_capacity = find_capacity_per_user(opt_x, x_user ,y_user)
    return sum(per_user_capacity)

def find_capacity_per_user(opt_x, x_user, y_user):
    number_of_users = len(x_user)
    capacity = np.zeros(number_of_users)
    for u in range(number_of_users):
        for bs in range(number_of_bs):
            if opt_x[u, bs] >= 1:
                coords_i = user_coords(u, x_user, y_user)
                coords_j = bs_coords(bs)
                gain_user = find_gain(coords_i, coords_j, coords_i, coords_j, beamwidth_u)
                gain_bs = find_gain(coords_j, coords_i, coords_j, coords_i, beamwidth_b)
                path_loss = find_path_loss(coords_i, coords_j)
                capacity[u] += W / users_per_beam * opt_x[u,bs] * math.log2(1 + transmission_power * gain_bs * gain_user / (path_loss * noise))
    return capacity

def find_snr(user, bs, x_user, y_user):
    coords_i = user_coords(user, x_user, y_user)
    coords_j = bs_coords(bs)
    gain_user = find_gain(coords_i, coords_j, coords_i, coords_j, beamwidth_u)
    gain_bs = find_gain(coords_j, coords_i, coords_j, coords_i, beamwidth_b)
    path_loss = find_path_loss(coords_i, coords_j)
    return (transmission_power * gain_user * gain_bs / path_loss ) / (noise)

def plot_BSs(x_user, y_user, opt_x):
    fig, ax = plt.subplots()
    for i in range(len(x_user)):
        for j in range(len(x_bs)):
            if opt_x[i,j] == 1:
                user = (x_user[i], y_user[i])
                bs = (x_bs[j], y_bs[j])
                user, bs, user2, bs2 = plot_modified_coords(user, bs)

                if user != user2 or bs != bs2:
                    plt.plot([user2[0], bs2[0]], [user2[1], bs2[1]], '--', color = colors[j], linewidth = 0.5)
                    plt.plot([user[0], bs[0]], [user[1], bs[1]], '--', color=colors[j], linewidth =0.5)
                else:
                    plt.plot([user[0], bs[0]], [user[1], bs[1]], color=colors[j], linewidth = 0.5)

    plt.scatter(x_user, y_user, marker = '.', color = 'k', s = 1)

    plt.scatter(x_bs, y_bs, marker = 'o', color = 'k', s = 25)
    for b in range(len(x_bs)):
        plt.text(x_bs[b] + 2, y_bs[b] - 3, b, fontsize = 9)

    bound = 0.1 * xDelta
    plt.xlim((xmin - bound, xmax + bound))
    plt.ylim((ymin - bound, ymax + bound))
    plt.show()
