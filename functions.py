import numpy as np
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn
from parameters import *
import networkx as nx

np.random.seed(seed)

pi = math.pi


def bore_b(user, bs):
    return geo_b(user, bs)

def bore_u(user, bs):
    return geo_u(user, bs)

def geo_b(user, bs):
    dy = user[1] - bs[1]
    dx = user[0] - bs[0]
    radians = math.atan2(dy, dx)
    if radians < 0:
        radians = radians + 2 * pi
    return radians

def geo_u(user, bs):
    dy = bs[1] - user[1]
    dx = bs[0] - user[0]
    radians = math.atan2(dy, dx)
    if radians < 0:
        radians = radians + 2 * pi
    return radians

def gain_bs(j, i, m, k):
    bs = (x_bs[j], y_bs[j])
    bs_2 = (x_bs[k], y_bs[k])
    user = (x_user[i], y_user[i])
    user_2 = (x_user[m], y_user[m])
    if beamwidth_b/2 < abs(bore_b(user, bs) - geo_b(user_2, bs_2)) < 2 * pi - beamwidth_b/2:
        return epsilon
    else:
        return (2 * pi - (2 * pi - beamwidth_b)*epsilon)/beamwidth_b

def gain_bs_coords(bs, user, user_2, bs_2):
    # bs = (x_bs[j], y_bs[j])
    # bs_2 = (x_bs[k], y_bs[k])
    # user = (x_user[i], y_user[i])
    # user_2 = (x_user[m], y_user[m])
    if beamwidth_b/2 < abs(bore_b(user_2, bs_2) - geo_b(user, bs_2)) < 2 * pi - beamwidth_b/2:
        return epsilon
    else:
        return (2 * pi - (2 * pi - beamwidth_b)*epsilon)/beamwidth_b


def gain_user(i, j, k, m):
    bs = (x_bs[j], y_bs[j])
    bs_2 = (x_bs[k], y_bs[k])
    user = (x_user[i], y_user[i])
    user_2 = (x_user[m], y_user[m])
    if beamwidth_u/2 < abs(bore_u(user, bs) - geo_u(user_2, bs_2)) < 2 * pi - beamwidth_u/2:
        return epsilon
    else:
        return (2 * pi - (2 * pi - beamwidth_u)*epsilon)/beamwidth_u

def gain_user_coords(user, bs, bs_2, user_2):
    # bs = (x_bs[j], y_bs[j])
    # bs_2 = (x_bs[k], y_bs[k])
    # user = (x_user[i], y_user[i])
    # user_2 = (x_user[m], y_user[m])
    if beamwidth_u/2 < abs(bore_u(user, bs) - geo_u(user, bs_2)) < 2 * pi - beamwidth_u/2:
        return epsilon
    else:
        return (2 * pi - (2 * pi - beamwidth_u)*epsilon)/beamwidth_u


def path_loss(i, j):
    user = (x_user[i], y_user[i])
    bs = (x_bs[j], y_bs[j])
    r = find_distance(user, bs)
    if r <= critical_distance:
        p_los = 1
    else:
        p_los = 0
    p_nlos = 1 - p_los
    l_los = K_los * max(1,r)**(-alpha_los)
    l_nlos = K_nlos * max(1,r)**(-alpha_nlos)
    return p_los * l_los + p_nlos * l_nlos

def path_loss_coords(user, bs):
    # user = (x_user[i], y_user[i])
    # bs = (x_bs[j], y_bs[j])
    r = find_distance(user, bs)
    if r <= critical_distance:
        p_los = 1
    else:
        p_los = 0
    p_nlos = 1 - p_los
    l_los = K_los * max(1,r)**(-alpha_los)
    l_nlos = K_nlos * max(1,r)**(-alpha_nlos)
    return p_los * l_los + p_nlos * l_nlos

def find_interference(user, bs, alpha, t):
    interference = 0
    for k in range(number_of_users):
        for m in range(number_of_bs):
            if alpha[k, m, t] == 1:
                bs_i = (x_bs[m], y_bs[m])
                user_i = (x_user[k], y_user[k])
                interference += fading[k, m] * gain_bs_coords(bs, user, user_i, bs_i) * gain_user_coords(user, bs, bs_i, user_i) * path_loss_coords(user, bs_i)
    return interference

def find_distance(user, bs):
    return math.sqrt((user[0] - bs[0])**2 + (user[1] - bs[1])**2)

def find_SINR(i, j, alpha, t):
    return find_power(i,j) / (find_interference(i, j, alpha, t) + sigma**2)

def find_power(i, j):
    user = (x_user[i], y_user[i])
    bs = (x_bs[j], y_bs[j])
    return fading[i, j] * gain_bs(bs, user, user, bs) * gain_user(user, bs, bs, user) * path_loss(user, bs)

def channel_capacity(i, j):
    return W * math.log2(1 + find_SINR(i, j))

def make_graph(xbs, ybs, xu, yu, alpha, number_of_users):
    G = nx.Graph()
    colorlist = list()
    nodesize = list()
    edgesize = list()
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
        nodesize.append(10)
        # labels[node + number_of_bs] = f'U{node}'
    for bs in range(number_of_bs):
        for user in range(number_of_users):
            if alpha[user, bs] > 0:
                G.add_edge(user + number_of_bs, bs)
                edgesize.append(1)
    # for user in range(len(xu)):
    #     if G.degree(user + number_of_bs) > 1:
    #         nodesize[user + number_of_bs] = 30
    #         colorlist[user + number_of_bs] = ('r')
    return G, colorlist, nodesize, edgesize, labels


def draw_graph(G, colorlist, nodesize, edgesize, labels, ax):
    pos = dict()
    for node in G.nodes():
        pos[node] = (nx.get_node_attributes(G, 'x')[node], nx.get_node_attributes(G, 'y')[node])
    nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_size=nodesize,
                           node_color=colorlist, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='black', alpha=0.5, width=edgesize)
    ax.set_xlim([xmin, xmax]), ax.set_ylim([ymin, ymax])
    nx.draw_networkx_labels(G, pos, labels, font_size=10)

if __name__ == "__main__":
    delta = 100
    grid_size = xmax/delta

    x_grid = np.arange(xmin, xmax, grid_size)
    y_grid = np.arange(ymin, ymax, grid_size)

    x_mesh,y_mesh = np.meshgrid(x_grid,y_grid)

    xc, yc = x_mesh + grid_size/2, y_mesh + grid_size/2


    interference = np.zeros((delta, delta))

    user1 = (x_user[0], y_user[0])
    bs = (x_bs[1], y_bs[1])
    for x in range(delta):
        print(x)
        for y in range(delta):
            user = (xc[0, x], yc[y, 0])
            interference[y, x] = find_interference((xc[0, x], yc[y, 0]), bs, 50, 1)


    contour_z1 = plt.contourf(x_mesh, y_mesh, interference, cmap='turbo')
    plt.colorbar(contour_z1)
    plt.scatter(x_user, y_user)
    plt.scatter(x_bs, y_bs)
    plt.xlim((xmin, xmax))
    plt.ylim((ymin, ymax))
    plt.show()