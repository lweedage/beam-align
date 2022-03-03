import numpy as np
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
            if i * radius + 0.5 * (j % 2) * radius <= xmax and j * dy <= ymax:
                xbs.append(i * radius + 0.5 * (j % 2) * radius)
                ybs.append(j * dy)
    return xbs, ybs


def find_coordinates(lambda_U):
    number_of_users = np.random.poisson((xmax - xmin) * (ymax - ymin) * lambda_U)
    print(number_of_users)
    x_user, y_user = np.random.uniform(xmin, xmax, number_of_users), np.random.uniform(ymin, ymax, number_of_users)
    return x_user, y_user


def make_graph(xbs, ybs, xu, yu, links):
    number_of_users = len(xu)
    G = nx.Graph()
    colorlist = list()
    nodesize = list()
    edgesize = list()
    edgecolor = list()
    labels = {}
    number_of_bs = len(xbs)
    for node in range(number_of_bs):
        G.add_node(node, x=xbs[node], y=ybs[node])
        colorlist.append(colors[node])
        nodesize.append(30)
        labels[node] = f'BS{node}'
    for node in range(number_of_users):
        G.add_node(node + number_of_bs, x=xu[node], y=yu[node])
        colorlist.append('w')
        nodesize.append(10)
        labels[node + number_of_bs] = f'{node}'
    for bs in range(number_of_bs):
        for user in range(number_of_users):
            if links[user, bs] > 0.1:
                G.add_edge(user + number_of_bs, bs)
                edgesize.append(2)
                edgecolor.append(colors[bs])
    return G, colorlist, nodesize, edgesize, labels, edgecolor


def draw_graph(xbs, ybs, xu, yu, links, ax):
    G, colorlist, nodesize, edgesize, labels, edgecolor = make_graph(xbs, ybs, xu, yu, links)
    pos = dict()
    for node in G.nodes():
        pos[node] = (nx.get_node_attributes(G, 'x')[node], nx.get_node_attributes(G, 'y')[node])
    nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_size=nodesize,
                           node_color=colorlist, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color=edgecolor, alpha=0.5, width=edgesize)
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color='k')


def fairness(x):
    return (sum(x)) ** 2 / (len(x) * sum([i ** 2 for i in x]))


def find_distance_allbs(user, xbs, ybs):
    xu, yu = user[0], user[1]
    xx = xu - xbs
    yy = yu - ybs
    return np.sqrt(xx ** 2 + yy ** 2)
