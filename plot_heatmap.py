import gurobipy as gp
from gurobipy import GRB
from gurobipy import quicksum
import numpy as np
import scipy.sparse as sp
import math
import matplotlib.pyplot as plt
import networkx as nx
import sys
from itertools import product
from scipy.spatial import Voronoi, voronoi_plot_2d
import initialization
from matplotlib.cm import ScalarMappable
import seaborn
from scipy.optimize import curve_fit

colors = seaborn.color_palette('rocket')
colors.reverse()


def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3/4) * radius
    for i in range(0, int(xDelta/radius) + 1):
        for j in range(0, int(yDelta/dy) + 1):
            xbs.append(i*radius + 0.5*(j%2) * radius)
            ybs.append(j*dy)
    return np.array(xbs), np.array(ybs)

def initialise_graph_hexagonal(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3/4) * radius
    for i in range(-10, int(xDelta/radius) + 11):
        for j in range(-10, int(yDelta/dy) + 11):
            if i % 3 == j % 2:
                continue
            xbs.append(i*radius + 0.5*(j%2) * radius)
            ybs.append(j*dy)
    return np.array(xbs), np.array(ybs)

number_of_bs = 16 # 16 means hexagonal, 8 means PPP
seed = 5
radius = 15

for simulation_number in [7, 10, 19, 22]:

    name = 'Simulations/simulation_' + str(simulation_number) + 'seed' + str(seed)
    hexagonal, ppp, number_of_users_1, number_of_users_2, number_of_users_3, OBJECTIVE, number_of_iterations, blub = initialization.initialization(simulation_number)


    if OBJECTIVE == 0:
        obj = 'log'
    elif OBJECTIVE == 1:
        obj = 'sum'


    total_connections = np.loadtxt(name + 'totalconnections' + obj + 'SNR' + str(number_of_iterations * 2 - 1) + '.txt')
    total_visits = np.loadtxt(name + 'totalvisits' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    two_connections = np.loadtxt(name + 'two_connections' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    three_connections = np.loadtxt(name + 'three_connections' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    four_plus_connections = np.loadtxt(name + 'fourplus_connections' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')

    total_connections1 = np.loadtxt(name + 'totalconnections_type1' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    total_visits1 = np.loadtxt(name + 'totalvisits_type1' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    two_connections1 = np.loadtxt(name + 'two_connections_type1' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    three_connections1 = np.loadtxt(name + 'three_connections_type1' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    four_plus_connections1 = np.loadtxt(name + 'fourplus_connections_type1' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    penalty1 = np.loadtxt(name + 'penalty1' + obj + 'SNR' + str(2 * number_of_iterations - 1) + '.txt')

    total_connections2 = np.loadtxt(name + 'totalconnections_type2' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    total_visits2 = np.loadtxt(name + 'totalvisits_type2' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    two_connections2 = np.loadtxt(name + 'two_connections_type2' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    three_connections2 = np.loadtxt(name + 'three_connections_type2' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    four_plus_connections2 = np.loadtxt(name + 'fourplus_connections_type2' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    penalty2 = np.loadtxt(name + 'penalty2' + obj + 'SNR' +  str(2 * number_of_iterations - 1) + '.txt')

    total_connections3 = np.loadtxt(name + 'totalconnections_type3' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    total_visits3 = np.loadtxt(name + 'totalvisits_type3' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    two_connections3 = np.loadtxt(name + 'two_connections_type3' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    three_connections3 = np.loadtxt(name + 'three_connections_type3' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    four_plus_connections3 = np.loadtxt(name + 'fourplus_connections_type3' + obj + 'SNR' + str(number_of_iterations * 2 - 1) +'.txt')
    penalty3 = np.loadtxt(name + 'penalty3' + obj + 'SNR'+ str(2 * number_of_iterations - 1) + '.txt')

    # channel_type1_grid = np.loadtxt(name + 'bandwidth_type1_grid' + obj + 'SNR' + str(99) + '.txt')
    # channel_type2_grid = np.loadtxt(name + 'bandwidth_type2_grid' + obj + 'SNR' + str(99) + '.txt')
    # channel_type3_grid = np.loadtxt(name + 'bandwidth_type3_grid' + obj + 'SNR' + str(99) + '.txt')
    # channel_total_grid = np.loadtxt(name + 'bandwidth_total_grid' + obj + 'SNR' + str(99) + '.txt')

    number_of_bs = 16
    number_of_users = number_of_users_1 + number_of_users_2 + number_of_users_3
    # ------------------------------- Initialisation --------------------------------------------
    xMin, xMax = 0, 51
    yMin, yMax = 0, 59

    np.random.seed(seed)
    if ppp:
        xbs = np.random.uniform(yMin, yMax, number_of_bs)
        ybs = np.random.uniform(xMin, xMax, number_of_bs)
    elif hexagonal:
        xbs, ybs = initialise_graph_triangular(radius, xMax, yMax)
    number_of_bs = len(xbs)
    base_stations = range(number_of_bs)

    # -------------------------- Plotting the solution --------------------------------------
    def make_graph(xbs, ybs):
        G = nx.Graph()
        colorlist = list()
        nodesize = list()
        edgesize = list()
        labels = {}
        number_of_bs = len(xbs)
        for node in range(number_of_bs):
            G.add_node(node, x=xbs[node], y=ybs[node])
            colorlist.append('w')
            nodesize.append(20)
            labels[node] = f'BS{node}'

        return G, colorlist, nodesize, edgesize, labels


    def draw_graph(G, colorlist, nodesize, edgesize, labels, ax):
        pos = dict()
        for node in G.nodes():
            pos[node] = (nx.get_node_attributes(G, 'x')[node], nx.get_node_attributes(G, 'y')[node])
        nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_size=nodesize,
                               node_color=colorlist, ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color='black', alpha=0.5, width=edgesize)
        nx.draw_networkx_labels(G, pos, labels, font_size=10)


    total_normalized, total_normalized1, total_normalized2, total_normalized3 = np.zeros((yMax, xMax)), np.zeros((yMax, xMax)), np.zeros((yMax, xMax)), np.zeros((yMax, xMax))
    two_connections_normalized, three_connections_normalized, fourplus_connections_normalized = np.zeros((yMax, xMax)), np.zeros((yMax, xMax)), np.zeros((yMax, xMax))
    two_connections_normalized1, three_connections_normalized1, fourplus_connections_normalized1 = np.zeros((yMax, xMax)), np.zeros((yMax, xMax)), np.zeros((yMax, xMax))
    two_connections_normalized2, three_connections_normalized2, fourplus_connections_normalized2 = np.zeros((yMax, xMax)), np.zeros((yMax, xMax)), np.zeros((yMax, xMax))
    two_connections_normalized3, three_connections_normalized3, fourplus_connections_normalized3 = np.zeros((yMax, xMax)), np.zeros((yMax, xMax)), np.zeros((yMax, xMax))

    for i in range(yMax):
        for j in range(xMax):
            if total_visits[i, j] > 0:
                total_normalized[i, j] = total_connections[i, j] / total_visits[i, j]
                total_normalized1[i, j] = total_connections1[i, j] / total_visits1[i, j]
                total_normalized2[i, j] = total_connections2[i, j] / total_visits2[i, j]
                total_normalized3[i, j] = total_connections3[i, j] / total_visits3[i, j]
                two_connections_normalized[i,j] = two_connections[i,j] / total_visits[i,j]
                three_connections_normalized[i, j] = three_connections[i,j]/ total_visits[i, j]
                fourplus_connections_normalized[i,j] = four_plus_connections[i,j] / total_visits[i,j]
                two_connections_normalized1[i,j] = two_connections1[i,j] / total_visits[i,j]
                three_connections_normalized1[i, j] = three_connections1[i,j]/ total_visits[i, j]
                fourplus_connections_normalized1[i,j] = four_plus_connections1[i,j] / total_visits[i,j]
                two_connections_normalized2[i,j] = two_connections2[i,j] / total_visits[i,j]
                three_connections_normalized2[i, j] = three_connections2[i,j]/ total_visits[i, j]
                fourplus_connections_normalized2[i,j] = four_plus_connections2[i,j] / total_visits[i,j]
                two_connections_normalized3[i,j] = two_connections3[i,j] / total_visits[i,j]
                three_connections_normalized3[i, j] = three_connections3[i,j]/ total_visits[i, j]
                fourplus_connections_normalized3[i,j] = four_plus_connections3[i,j] / total_visits[i,j]

    two = int(sum(sum(two_connections)))
    three = int(sum(sum(three_connections)))
    fourplus = int(sum(sum(four_plus_connections)))
    total = int(sum(sum(total_visits)))
    one = total - (two + three + fourplus)

    two1 = int(sum(sum(two_connections1)))
    three1 = int(sum(sum(three_connections1)))
    fourplus1 = int(sum(sum(four_plus_connections1)))
    total1 = int(sum(sum(total_visits1)))
    one1 = total1 - (two1 + three1 + fourplus1)

    two2 = int(sum(sum(two_connections2)))
    three2 = int(sum(sum(three_connections2)))
    fourplus2 = int(sum(sum(four_plus_connections2)))
    total2 = int(sum(sum(total_visits2)))
    one2 = total2 - (two2 + three2 + fourplus2)

    two3 = int(sum(sum(two_connections3)))
    three3 = int(sum(sum(three_connections3)))
    fourplus3 = int(sum(sum(four_plus_connections3)))
    total3 = int(sum(sum(total_visits3)))
    one3 = total3 - (two3 + three3 + fourplus3)

    lijst = [one/total, two/total, three/total, fourplus/total]
    lijst1 = [one1/total1, two1/total1, three1/total1, fourplus1/total1]
    if total2 != 0:
        lijst2 = [one2/total2, two2/total2, three2/total2, fourplus2/total2]
    else:
        lijst2 = [0, 0, 0, 0]
    lijst3 = [one3/total3, two3/total3, three3/total3, fourplus3/total3]

    fig, ax = plt.subplots()
    plt.bar([0.85, 1.85, 2.85, 3.85], lijst1, label = 'Type 1', width = 0.5)
    plt.bar([0.95, 1.95, 2.95, 3.95], lijst2, label = 'Type 2', width = 0.5)
    plt.bar([1.05, 2.05, 3.05, 4.05], lijst3, label = 'Type 3', width = 0.5)
    plt.bar([1.15, 2.15, 3.15, 4.15], lijst, label = 'Total', width = 0.5)
    plt.xlabel('Number of connections')
    plt.xticks([1, 2, 3, 4], [1, 2, 3, '4+'])
    plt.legend()
    plt.savefig('histogram_234connections_simulation_' + str(simulation_number) + str(obj) + '.png')
    plt.show()

    fig, axs = plt.subplots(2, 2)
    axs[0,0].scatter(xbs, ybs, c = 'w', s=3)
    axs[0,0].imshow(total_normalized.transpose(), cmap='turbo', vmin=0, vmax=1)
    axs[0,0].set_title('All types')

    axs[0,1].scatter(xbs, ybs, c = 'w', s = 3)
    axs[0,1].imshow(total_normalized1.transpose(), cmap='turbo', vmin=0, vmax=1)
    axs[0,1].set_title('Type 1')

    axs[1,0].scatter(xbs, ybs, c = 'w', s = 3)
    axs[1,0].imshow(total_normalized2.transpose(), cmap='turbo', vmin=0, vmax=1)
    axs[1,0].set_title('Type 2')

    axs[1,1].scatter(xbs, ybs, c = 'w', s = 3)
    axs[1,1].imshow(total_normalized3.transpose(), cmap='turbo', vmin=0, vmax=1)
    axs[1,1].set_title('Type 3')

    plt.suptitle('Probability of MC')
    for ax in axs.flat:
        ax.set(xlabel='$x$', ylabel='$y$')
    for ax in axs.flat:
        ax.label_outer()

    scales = np.linspace(0, 1, 7)
    cmap = plt.get_cmap("turbo")
    norm = plt.Normalize(scales.min(), scales.max())
    sm =  ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=axs[:,1])
    plt.savefig('MC_prob_types_simulation_' + str(simulation_number) + str(obj) + '.png')
    plt.show()

    fig, axs = plt.subplots(2, 2)
    axs[0,0].scatter(xbs, ybs, c = 'w', s = 3)
    axs[0,0].imshow(total_normalized.transpose(), cmap='turbo', vmin=0, vmax=1)
    axs[0,0].set_title('Total')

    axs[0, 1].scatter(xbs, ybs, c = 'w', s=3)
    axs[0, 1].imshow(two_connections_normalized.transpose(), cmap='turbo', vmin=0, vmax=1)
    axs[0, 1].set_title('2 connections')

    axs[1, 0].scatter(xbs, ybs, c = 'w', s = 3)
    axs[1, 0].imshow(three_connections_normalized.transpose(), cmap='turbo', vmin=0, vmax=1)
    axs[1, 0].set_title('3 connections')

    axs[1,1].scatter(xbs, ybs, c = 'w', s = 3)
    axs[1,1].imshow(fourplus_connections_normalized.transpose(), cmap='turbo', vmin=0, vmax=1)
    axs[1,1].set_title('4+ connections')



    plt.suptitle('Probability of MC')
    for ax in axs.flat:
        ax.set(xlabel='$x$', ylabel='$y$')
    for ax in axs.flat:
        ax.label_outer()

    scales = np.linspace(0, 1, 7)
    cmap = plt.get_cmap("turbo")
    norm = plt.Normalize(scales.min(), scales.max())
    sm =  ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=axs[:,1])
    plt.savefig('MC_prob_234connections_simulation_' + str(simulation_number) + str(obj) + '.png')
    plt.show()

    def find_distance(xu, yu, xbs, ybs):
        # xx = xu - xbs
        # yy = yu - ybs
        xx = np.minimum((xu - xbs) % xMax, (xbs - xu) % xMax)
        yy = np.minimum((yu - ybs) % yMax, (ybs - yu) % yMax)
        return np.sqrt(xx ** 2 + yy ** 2)

    def find_bs(x, y, xbs, ybs):
        indices = find_distance(x, y, xbs, ybs).argsort()
        return indices[:2]

    probabilities = np.zeros((yMax, xMax))
    probabilities_3 = np.zeros((yMax, xMax))

    labdaU = number_of_users/(xMax * yMax)

    def find_area_3_circles(x, y):
        bs1, bs2, bs3 = find_distance(x, y, xbs, ybs).argsort()[:3]
        r1, r2, r3 = sorted(find_distance(x, y, xbs, ybs))[:3]
        x1, x2, x3 = xbs[bs1], xbs[bs2], xbs[bs3]
        y1, y2, y3 = ybs[bs1], ybs[bs2], ybs[bs3]
        d12 = find_distance(x1, y1, x2, y2)
        d13 = find_distance(x1, y1, x3, y3)
        d23 = find_distance(x2, y2, x3, y3)

        if r1 + r2 > d12:
            area1 = r1 ** 2 * math.acos((d12 ** 2 + r1 ** 2 - r2 ** 2) / (2 * d12 * r1)) + r2 ** 2 * math.acos(min(1,
            (d12 ** 2 + r2 ** 2 - r1 ** 2) / (2 * d12 * r2))) - 0.5 * math.sqrt(
            (-d12 + r1 + r2) * (d12 + r1 - r2) * (d12 - r1 + r2) * (d12 + r1 + r2))
        else:
            area1 = 0
        if r1 + r3 > d13:
            area2 = r1 ** 2 * math.acos((d13 ** 2 + r1 ** 2 - r3 ** 2) / (2 * d13 * r1)) + r3 ** 2 * math.acos(min(1,
             (d13 ** 2 + r3 ** 2 - r1 ** 2) / (2 * d13 * r3))) - 0.5 * math.sqrt((-d13 + r1 + r3) * (d13 + r1 - r3) * (d13 - r1 + r3) * (d13 + r1 + r3))
        else:
            area2 = 0
        if r2 + r3 > d23:
            area3 = r2 ** 2 * math.acos((d23 ** 2 + r2 ** 2 - r3 ** 2) / (2 * d23 * r2)) + r3 ** 2 * math.acos(min(1, (d23 ** 2 + r3 ** 2 - r2 ** 2) / (2 * d23 * r3))) - 0.5 * math.sqrt((-d23 + r2 + r3) * (d23 + r2 - r3) * (d23 - r2 + r3) * (d23 + r2 + r3))
        else:
            area3 = 0
        return area1 + area2 + area3

    if obj == 'sum' and 3 == 2:
        for x in range(yMax):
            for y in range(xMax):
                bs0, bs1 = find_bs(y, x, xbs, ybs)
                r0, r1, r2 = sorted(find_distance(y, x, xbs, ybs))[:3]
                d = find_distance(xbs[bs0], ybs[bs0], xbs[bs1], ybs[bs1])
                area = r0**2 * math.acos((d**2 + r0**2 - r1**2)/(2*d*r0)) + r1**2 * math.acos(min(1,(d**2 + r1**2 - r0**2)/(2*d*r1))) - 0.5*math.sqrt((-d + r0 + r1) * (d + r0 - r1) * (d - r0 + r1) * (d + r0 + r1))
                probabilities[x, y] = math.exp(-labdaU * (math.pi * (r0**2 + r1**2) - area))

                area_3 = find_area_3_circles(x,y)
                probabilities_3[x, y] = probabilities[x, y] + math.exp(-labdaU * (math.pi * (r0**2 + r1**2 + r2**2) - area_3))

        fig, ax = plt.subplots()
        plt.scatter(ybs, xbs, c = 'w')
        for i in base_stations:
            ax.annotate(i, (ybs[i], xbs[i]), color = 'w')
        plt.imshow(probabilities_3, cmap='turbo', vmin=0, vmax=1)
        plt.colorbar()
        plt.show()

    power = 1000
    noise = 10
    c = power/noise
    path_loss = 2


    def find_SNR():
        snr = np.zeros((xMax, xMax))
        for i in range(xMax):
            for j in range(xMax):
                bs = find_bs(i, j, xbs, ybs)[0]
                if 0 < find_distance(i, j, xbs[bs], ybs[bs]) <= 1:
                    snr[i, j] = power / (noise)
                elif find_distance(i,j, xbs[bs], ybs[bs]) > 0:
                    snr[i, j] = power * find_distance(i, j, xbs[bs], ybs[bs])**(-path_loss) / (noise)
                else:
                    snr[i, j] = 0
        return snr

    def find_distance_difference(xbs, ybs):
        d = np.zeros((yMax, xMax))
        for i in range(yMax):
            for j in range(xMax):
                r0, r1 = sorted(find_distance(j, i, xbs, ybs))[:2]
                d[i, j] = r1 - r0
        return d

    def find_distance_difference2(xbs, ybs):
        d = np.zeros((yMax, xMax))
        r = np.zeros((yMax, xMax))
        r2 = np.zeros((yMax, xMax))

        for i in range(yMax):
            for j in range(xMax):
                r0, r1 = sorted(find_distance(j, i, xbs, ybs))[:2]
                d[i, j] = (r1 - r0)
                r[i, j] = r0
                r2[i, j] = r1
        return d, r, r2

    distance_difference = find_distance_difference(ybs, xbs)
    distance_difference2, r, r2 = find_distance_difference2(ybs, xbs)

    def func(x, a, b, c):
        return a * np.exp(np.multiply(x, b)) + c

    def func_quadratic(x, a):
        snr = c * x**(-path_loss)
        return np.divide(a, snr)

    def func_linear(x, a, b):
        return np.multiply(a, x) + b

    if obj == 'log':

        popt, pcov = curve_fit(func, r.flatten()[::2], total_normalized.flatten()[::2], bounds = ([0, 0, 0], [10, 10, 10]))
        popt_quad, pcov2 = curve_fit(func_quadratic, r.flatten()[::2], total_normalized.flatten()[::2], bounds = ([-10], [10]))

        popt1, pcov1 = curve_fit(func, r.flatten()[::2], total_normalized1.flatten()[::2], bounds = ([0, 0, 0], [10, 10, 10]))
        popt_quad1, pcov2 = curve_fit(func_quadratic, r.flatten()[::2], total_normalized1.flatten()[::2], bounds = ([-10], [10]))
        popt_lin1, pcov3 = curve_fit(func_linear, r.flatten()[::2], total_normalized1.flatten()[::2], bounds = ([-10, -10], [10, 10]))
        popt2, pcov = curve_fit(func, r.flatten()[::2], total_normalized2.flatten()[::2], bounds = ([0, 0, 0], [10, 10, 10]))
        popt_quad2, pcov2 = curve_fit(func_quadratic, r.flatten()[::2], total_normalized2.flatten()[::2], bounds = ([-10], [10]))

        popt3, pcov = curve_fit(func, r.flatten()[::2], total_normalized3.flatten()[::2], bounds = ([0, 0, 0], [10, 10, 10]))
        popt_quad3, pcov2 = curve_fit(func_quadratic, r.flatten()[::2], total_normalized3.flatten()[::2], bounds = ([-10], [10]))



        fig, axs = plt.subplots(2, 2)
        fig.suptitle('Distance and MC probability')
        axs[0,0].scatter(r.flatten(), total_normalized.flatten(), color = colors[0] )
        axs[0,0].plot(r.flatten(), func_quadratic(r.flatten(), *popt_quad), label = f"$y = {popt_quad[0]:.2f}/SNR$", color = colors[4])
        axs[0,0].legend()
        axs[0,0].set_title("All types")
        axs[0,1].scatter(r.flatten(), total_normalized1.flatten(), color = colors[1])
        axs[0,1].plot(r.flatten(), func_quadratic(r.flatten(), *popt_quad1), label = f"$y = {popt_quad1[0]:.2f}/SNR$", color = colors[4])
        axs[0,1].legend()
        axs[0,1].set_title('Type 1')
        axs[1,0].scatter(r.flatten(), total_normalized2.flatten(), color = colors[2])
        axs[1,0].plot(r.flatten(), func_quadratic(r.flatten(), *popt_quad2), label = f"$y = {popt_quad2[0]:.2f}/SNR$", color = colors[4])
        axs[1,0].legend()
        axs[1,0].set_title('Type 2')
        axs[1,1].scatter(r.flatten(), total_normalized3.flatten(), color = colors[3])
        axs[1,1].plot(r.flatten(), func_quadratic(r.flatten(), *popt_quad3), label = f"$y = {popt_quad3[0]:.2f}/SNR$", color = colors[4])
        axs[1,1].legend()
        axs[1,1].set_title('Type 3')
        for ax in axs.flat:
            ax.set(xlabel='$R_1$', ylabel='MC probability')
        for ax in axs.flat:
            ax.label_outer()
            ax.set_ylim([0, 1])

        plt.savefig('scatter_types_simulation_' + str(simulation_number) + str(obj) + '.png')
        plt.show()

    # fig, axs = plt.subplots(2, 2, sharex = True, sharey= True)
    # fig.suptitle('Distance and MC probability')
    # axs[0,0].scatter(r.flatten(), total_normalized.flatten(), color = colors[0])
    # axs[0,0].set_title("Total")
    # axs[0,1].scatter(r.flatten(), two_connections_normalized.flatten(), color = colors[1])
    # axs[0,1].set_title('2 connections')
    # axs[1,0].scatter(r.flatten(), three_connections_normalized.flatten(), color = colors[2])
    # axs[1,0].set_title('3 connections')
    # axs[1,1].scatter(r.flatten(), fourplus_connections_normalized.flatten(), color = colors[3])
    # axs[1,1].set_title('4+ connections')
    # for ax in axs.flat:
    #     ax.set(xlabel='$R_1$', ylabel='MC probability')
    # for ax in axs.flat:
    #     ax.label_outer()
    #
    # plt.savefig('scatter_234connections_simulation_' + str(simulation_number) + str(obj) + '.png')
    # plt.show()
    #
    # penalty_data = [penalty1, penalty2, penalty3]
    # fig, ax = plt.subplots()
    # plt.boxplot(penalty_data)
    # plt.ylabel('Penalty')
    # plt.xlabel('Type')
    # plt.savefig('penalty_boxplot_simulation_' + str(simulation_number) + str(obj) + '.png')
    # plt.show()

    # fig, axs = plt.subplots(2, 2, sharex = True, sharey = True)
    # fig.suptitle('Distance difference')
    # axs[0,0].scatter(distance_difference2.flatten(), total_normalized.flatten(), c = total_normalized.flatten(), marker = '.', cmap = 'turbo', vmin=0, vmax=1)
    # axs[0,0].set_title("All types")
    # axs[0,1].scatter(distance_difference2.flatten(), total_normalized1.flatten(), c = total_normalized1.flatten(), marker = '.', cmap = 'turbo', vmin=0, vmax=1)
    # axs[0,1].set_title('Type 1')
    # axs[1,0].scatter(distance_difference2.flatten(), total_normalized2.flatten(), c = total_normalized2.flatten(), marker = '.', cmap = 'turbo', vmin=0, vmax=1)
    # axs[1,0].set_title('Type 2')
    # axs[1,1].scatter(distance_difference2.flatten(), total_normalized3.flatten(), c = total_normalized3.flatten(), marker = '.', cmap = 'turbo', vmin=0, vmax=1)
    # axs[1,1].set_title('Type 3')
    # for ax in axs.flat:
    #     ax.set(xlabel='$R_2 - R_1$', ylabel='MC probability')
    # for ax in axs.flat:
    #     ax.label_outer()
    #
    # scales = np.linspace(0, 1, 7)
    # cmap = plt.get_cmap("turbo")
    # norm = plt.Normalize(scales.min(), scales.max())
    # sm =  ScalarMappable(norm=norm, cmap=cmap)
    # sm.set_array([])
    # cbar = fig.colorbar(sm, ax=axs[:,1])
    # plt.savefig('scatter_types_distance_difference_simulation_' + str(simulation_number) + str(obj) + '.png')
    # plt.show()
