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
import initialization

def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3/4) * radius
    for i in range(0, int(xDelta/radius) + 1):
        for j in range(0, int(yDelta/dy) + 1):
            xbs.append(i*radius + 0.5*(j%2) * radius)
            ybs.append(j*dy)
    return xbs, ybs

for simulation_number in [19]:

    hexagonal, ppp, number_of_users_1, number_of_users_2, number_of_users_3, OBJECTIVE, number_of_iterations, penalty_importantness = initialization.initialization(simulation_number)

    LOG_CHANNEL = 0
    SUM_CHANNEL = 1
    MIN_CHANNEL = 2
    SOFT_SUM_CHANNEL = 3
    UPF = 4

    radius = 15
    number_of_bs = 16

    max_distance = 2000

    number_of_users = number_of_users_1 + number_of_users_2 + number_of_users_3

    min_cap_type1 = 2
    min_cap_type2 = 20
    min_cap_type3 = 100
    minimum_channel_capacity = np.concatenate((np.ones(number_of_users_1) * min_cap_type1, np.ones(number_of_users_2) * min_cap_type2, np.ones(number_of_users_3) * min_cap_type3), axis=None)

    total_bandwidth = 50

    xMin, xMax = 0, 59 #in the case of hexagonal grid
    yMin, yMax = 0, 51 #in the case of hexagonal grid

    # ------------------------------- Initialisation --------------------------------------------
    def find_distance_matrix(xu, yu, xbs, ybs):
        distance = np.zeros((len(xu), len(xbs)))
        for i in range(len(xu)):
            for j in range(len(xbs)):
                x = np.minimum((xu[i] - xbs[j]) % xMax, (xbs[j] - xu[i]) % xMax)
                y = np.minimum((yu[i] - ybs[j]) % yMax, (ybs[j] - yu[i]) % yMax)
                # x = xu[i] - xbs[j]
                # y = yu[i] - ybs[j]
                distance[i, j] = np.sqrt(x ** 2 + y ** 2)
        return distance

    power = 1000
    noise = 1
    c = power/noise
    path_loss = 2

    total_connections, total_visits, two_connections, three_connections, fourplus_connections, channel_total_grid = np.zeros((xMax, yMax)), np.zeros((xMax, yMax)), np.zeros((xMax, yMax)), np.zeros((xMax, yMax)), np.zeros((xMax, yMax)), np.zeros((xMax, yMax))
    total_connections1, total_visits1, two_connections1, three_connections1, fourplus_connections1, channel_type1_grid = np.zeros((xMax, yMax)), np.zeros((xMax, yMax)), np.zeros((xMax, yMax)), np.zeros((xMax, yMax)), np.zeros((xMax, yMax)), np.zeros((xMax, yMax))
    total_connections2, total_visits2, two_connections2, three_connections2, fourplus_connections2, channel_type2_grid = np.zeros((xMax, yMax)), np.zeros((xMax, yMax)), np.zeros((xMax, yMax)), np.zeros((xMax, yMax)), np.zeros((xMax, yMax)), np.zeros((xMax, yMax))
    total_connections3, total_visits3, two_connections3, three_connections3, fourplus_connections3, channel_type3_grid = np.zeros((xMax, yMax)), np.zeros((xMax, yMax)), np.zeros((xMax, yMax)), np.zeros((xMax, yMax)), np.zeros((xMax, yMax)), np.zeros((xMax, yMax))

    penalty1, penalty2, penalty3 = [], [], []

    channel_type1, channel_type2, channel_type3 = [], [], []

    seed = 5

    if OBJECTIVE == 0:
        obj = 'log'
    elif OBJECTIVE == 1:
        obj = 'sum'

    snr_sinr = 'SNR'



    name = 'Simulations/simulation_' + str(simulation_number) + 'seed' + str(seed)
    print(name)
    for iteration in range(100):
        print('Iteration', iteration, 'Simulation', simulation_number)
        np.random.seed(iteration)

        xu = np.random.uniform(xMin, xMax, number_of_users)
        yu = np.random.uniform(yMin, yMax, number_of_users)

        np.random.seed(seed)
        if hexagonal:
            xbs, ybs = initialise_graph_triangular(radius, xMax, yMax)
        elif ppp:
            xbs = np.random.uniform(xMin, xMax, number_of_bs)
            ybs = np.random.uniform(yMin, yMax, number_of_bs)
        number_of_bs = len(xbs)

        distances = find_distance_matrix(xu, yu, xbs, ybs)
        logSNR = np.log2(1 + c * np.power(distances, -path_loss))

        users = range(number_of_users)
        base_stations = range(number_of_bs)

        # ---------------------- Checking if model is feasible
        if max_distance < max([min(distances[i, :]) for i in users]):
            print('Maximum user distance is too close')
            sys.exit()


        def find_angle(user, bs1, bs2):
            slope1 = (ybs[bs1] - yu[user])/(xbs[bs1] - yu[user])
            slope2 = (ybs[bs2] - yu[user])/(xbs[bs2] - yu[user])
            angle = math.atan(abs((slope2-slope1)/(1+slope1*slope2)))
            return angle


        # ------------------------ Start of optimization program ------------------------------------
        try:
            m = gp.Model("Model 1")
            m.Params.LogToConsole = 0

            # -------------- VARIABLES -----------------------------------
            channel_capacity = m.addMVar(shape=(number_of_users, number_of_bs), vtype=GRB.CONTINUOUS)
            bandwidth = m.addMVar(shape=(number_of_users, number_of_bs), vtype=GRB.CONTINUOUS)

            channel_capacity_per_user = m.addMVar(shape=(number_of_users,), vtype=GRB.CONTINUOUS)
            channel_capacity_per_user_var = channel_capacity_per_user.tolist()

            angle_soft_constraint = m.addVar(vtype=GRB.CONTINUOUS)

            alpha = m.addMVar(shape=(number_of_users, number_of_bs), vtype=GRB.BINARY)

            if OBJECTIVE == LOG_CHANNEL:
                logarithm_objective = m.addMVar(shape=(number_of_users,))
                logarithm_objective_var = logarithm_objective.tolist()
            if OBJECTIVE == MIN_CHANNEL:
                minimum_objective = m.addVar()

            penalty = m.addMVar(shape=(3,), vtype=GRB.CONTINUOUS, lb=0)


            # ----------------- OBJECTIVE ----------------------------------
            if OBJECTIVE == SUM_CHANNEL:
                m.setObjective(sum(channel_capacity_per_user) - penalty_importantness * sum(penalty), GRB.MAXIMIZE)
            elif OBJECTIVE == LOG_CHANNEL:
                m.setObjective(sum(logarithm_objective) - penalty_importantness * sum(penalty), GRB.MAXIMIZE)

            # --------------- CONSTRAINTS -----------------------------
            # Per-user channel capacity
            m.addConstrs(sum(channel_capacity[i, :]) == channel_capacity_per_user[i] for i in users)

            # Bandwidth constraint
            for j in base_stations:
                m.addConstr(sum(channel_capacity[i, j] / logSNR[i, j] for i in users) <= total_bandwidth,
                            name="total_bandwidth")

            for i in users:
                for j in base_stations:
                    m.addConstr(channel_capacity[i, j] <= alpha[i, j] * total_bandwidth * logSNR[i,j], name = 'capalpha1')
                    m.addConstr(channel_capacity[i, j] >= alpha[i, j] * 0.01, name = 'capalpha2')
                    m.addConstr(bandwidth[i,j] == channel_capacity[i,j]/logSNR[i,j], name = 'bandwidth')


            # Capacity constraint
            for i in users:
                if i < number_of_users_1:
                    m.addConstr(sum(channel_capacity[i, :]) >= minimum_channel_capacity[i] * (1 - penalty[0]),
                            name="Minimum capacity - relaxed")
                elif i < number_of_users_1 + number_of_users_2:
                    m.addConstr(sum(channel_capacity[i, :]) >= minimum_channel_capacity[i] * (1 - penalty[1]),
                            name="Minimum capacity - relaxed")
                elif i < number_of_users:
                    m.addConstr(sum(channel_capacity[i, :]) >= minimum_channel_capacity[i] * (1 - penalty[2]),
                            name="Minimum capacity - relaxed")

            # Distance constraint
            for i in users:
                for j in base_stations:
                    if distances[i, j] > max_distance:
                        m.addConstr(channel_capacity[i, j] == 0, name = "Distance constraint")

            # Logarithmic objective constraint
            if OBJECTIVE == LOG_CHANNEL:
                for i in users:
                    m.addGenConstrLog(channel_capacity_per_user_var[i], logarithm_objective_var[i], name='log_constraint')


            # --------------------- OPTIMIZE MODEL -------------------------
            m.optimize()

            m.getObjective()
            # print('Objective value: %g' % m.objVal)

        except gp.GurobiError as e:
            print('Error code ' + str(e.errno) + ': ' + str(e))
            # sys.exit()

        except AttributeError:
            print('Encountered an attribute error')
            # sys.exit()


        # -------------------------- Plotting the solution --------------------------------------
        def make_graph(xbs, ybs, xpop, ypop, bandwidth):
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
                G.add_node(node + number_of_bs, x =xpop[node], y = ypop[node])
                if node < number_of_users_1:
                    colorlist.append('g')
                    nodesize.append(10)
                elif node < number_of_users_1 + number_of_users_2:
                    colorlist.append('b')
                    nodesize.append(15)
                else:
                    colorlist.append('r')
                    nodesize.append(20)
            for bs in range(number_of_bs):
                for user in range(len(xu)):
                    if bandwidth[user, bs] > 0:
                        G.add_edge(user + number_of_bs, bs, bw = bandwidth[user, bs])
                        edgesize.append(1)#bandwidth[user, bs] / np.max(bandwidth) * 10)
            return G, colorlist, nodesize, edgesize, labels


        def draw_graph(G, colorlist, nodesize, edgesize, labels):
            fig, ax = plt.subplots()
            pos = dict()
            for node in G.nodes():
                pos[node] = (nx.get_node_attributes(G, 'x')[node], nx.get_node_attributes(G, 'y')[node])
            nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_size=nodesize,
                                   node_color=colorlist, ax=ax)
            nx.draw_networkx_edges(G, pos, edge_color='black', alpha=0.5, width=edgesize)
            ax.set_xlim([xMin, xMax]), ax.set_ylim([yMin, yMax])
            nx.draw_networkx_labels(G, pos, labels, font_size=10)

        def number_of_connections(channel_capacity):
            connections = channel_capacity > 0
            connections = connections.astype(int)
            connections_per_bs = sum(connections)
            connections_per_user = sum(connections.transpose())
            return connections, connections_per_bs, connections_per_user

        # G, colorlist, nodesize, edgesize, labels = make_graph(xbs, ybs, xu, yu, channel_capacity.X)
        # draw_graph(G, colorlist, nodesize, edgesize, labels)
        # plt.savefig('temp.png')

        connections, connections_per_bs, connections_per_user = number_of_connections(channel_capacity.X)

        def find_distance(xu, yu, xbs, ybs):
            xx = xu - xbs
            yy = yu - ybs
            return np.sqrt(xx ** 2 + yy ** 2)

        def find_bs(x, y, xbs, ybs):
            indices = find_distance(x, y, xbs, ybs).argsort()
            return indices[0]

        bandwidth_per_user = sum(bandwidth.X.transpose())

        def add_grid(connections, xu, yu, total_connections, total_visits, two_connections ,three_connections, fourplus_connections, user_range, channel_grid):
            for u in user_range:
                x, y = math.floor(xu[u]), math.floor(yu[u])
                total_visits[x, y] += 1
                channel_grid[x,y] += bandwidth_per_user[u]
                if connections[u] > 1:
                    total_connections[x, y] += 1
                if connections[u] == 2:
                    two_connections[x, y] += 1
                elif connections[u] == 3:
                    three_connections[x, y] += 1
                elif connections[u] > 3:
                    fourplus_connections[x, y] += 1

            return total_connections, total_visits, two_connections, three_connections, fourplus_connections, channel_grid

        total_connections, total_visits, two_connections, three_connections, fourplus_connections, channel_total_grid = add_grid(connections_per_user, xu, yu, total_connections, total_visits, two_connections ,three_connections, fourplus_connections, [i for i in range(number_of_users)], channel_total_grid)
        total_connections1, total_visits1, two_connections1, three_connections1, fourplus_connections1, channel_type1_grid = add_grid(connections_per_user, xu, yu, total_connections1, total_visits1, two_connections1 ,three_connections1, fourplus_connections1, [i for i in range(0, number_of_users_1)], channel_type1_grid)
        total_connections2, total_visits2, two_connections2, three_connections2, fourplus_connections2, channel_type2_grid = add_grid(connections_per_user, xu, yu, total_connections2, total_visits2, two_connections2 ,three_connections2, fourplus_connections2, [i for i in range(number_of_users_1, number_of_users_1 + number_of_users_2)], channel_type2_grid)
        total_connections3, total_visits3, two_connections3, three_connections3, fourplus_connections3, channel_type3_grid = add_grid(connections_per_user, xu, yu, total_connections3, total_visits3, two_connections3 ,three_connections3, fourplus_connections3, [i for i in range(number_of_users_2 + number_of_users_1, number_of_users)], channel_type3_grid)
        # penalty1.append(penalty.X[0])
        # penalty2.append(penalty.X[1])
        # penalty3.append(penalty.X[2])
        #
        # channel_type1.extend(channel_capacity_per_user.X[0:number_of_users_1])
        # channel_type2.extend(channel_capacity_per_user.X[number_of_users_1:(number_of_users_1 + number_of_users_2)])
        # channel_type3.extend(channel_capacity_per_user.X[(number_of_users_1 + number_of_users_2):number_of_users])

    # np.savetxt(name + 'totalconnections' + obj + snr_sinr + str(iteration) + '.txt', total_connections)
    # np.savetxt(name + 'totalvisits' + obj + snr_sinr + str(iteration) + '.txt', total_visits)
    # np.savetxt(name + 'two_connections' + obj + snr_sinr + str(iteration) + '.txt', two_connections)
    # np.savetxt(name + 'three_connections' + obj + snr_sinr + str(iteration) + '.txt', three_connections)
    # np.savetxt(name + 'fourplus_connections' + obj + snr_sinr + str(iteration) + '.txt', fourplus_connections)
    #
    # np.savetxt(name + 'totalconnections_type1' + obj + snr_sinr + str(iteration) + '.txt', total_connections1)
    # np.savetxt(name + 'totalvisits_type1' + obj + snr_sinr + str(iteration) + '.txt', total_visits1)
    # np.savetxt(name + 'two_connections_type1' + obj + snr_sinr + str(iteration) + '.txt', two_connections1)
    # np.savetxt(name + 'three_connections_type1' + obj + snr_sinr + str(iteration) + '.txt', three_connections1)
    # np.savetxt(name + 'fourplus_connections_type1' + obj + snr_sinr + str(iteration) + '.txt', fourplus_connections1)
    #
    # np.savetxt(name + 'totalconnections_type2' + obj + snr_sinr + str(iteration) + '.txt', total_connections2)
    # np.savetxt(name + 'totalvisits_type2' + obj + snr_sinr + str(iteration) + '.txt', total_visits2)
    # np.savetxt(name + 'two_connections_type2' + obj + snr_sinr + str(iteration) + '.txt', two_connections2)
    # np.savetxt(name + 'three_connections_type2' + obj + snr_sinr + str(iteration) + '.txt', three_connections2)
    # np.savetxt(name + 'fourplus_connections_type2' + obj + snr_sinr + str(iteration) + '.txt', fourplus_connections2)
    #
    # np.savetxt(name + 'totalconnections_type3' + obj + snr_sinr + str(iteration) + '.txt', total_connections3)
    # np.savetxt(name + 'totalvisits_type3' + obj + snr_sinr + str(iteration) + '.txt', total_visits3)
    # np.savetxt(name + 'two_connections_type3' + obj + snr_sinr + str(iteration) + '.txt', two_connections3)
    # np.savetxt(name + 'three_connections_type3' + obj + snr_sinr + str(iteration) + '.txt', three_connections3)
    # np.savetxt(name + 'fourplus_connections_type3' + obj + snr_sinr + str(iteration) + '.txt', fourplus_connections3)
    #
    # np.savetxt(name + 'penalty1' + obj + snr_sinr + str(iteration) + '.txt', penalty1)
    # np.savetxt(name + 'penalty2' + obj + snr_sinr + str(iteration) + '.txt', penalty2)
    # np.savetxt(name + 'penalty3' + obj + snr_sinr + str(iteration) + '.txt', penalty3)
    #
    # np.savetxt(name + 'channel_type1' + obj + snr_sinr + str(iteration) + '.txt', channel_type1)
    # np.savetxt(name + 'channel_type2' + obj + snr_sinr + str(iteration) + '.txt', channel_type2)
    # np.savetxt(name + 'channel_type3' + obj + snr_sinr + str(iteration) + '.txt', channel_type3)

    np.savetxt(name + 'bandwidth_type1_grid' + obj + snr_sinr + str(iteration) + '.txt', channel_type1_grid)
    np.savetxt(name + 'bandwidth_type2_grid' + obj + snr_sinr + str(iteration) + '.txt', channel_type2_grid)
    np.savetxt(name + 'bandwidth_type3_grid' + obj + snr_sinr + str(iteration) + '.txt', channel_type3_grid)
    np.savetxt(name + 'bandwidth_total_grid' + obj + snr_sinr + str(iteration) + '.txt', channel_total_grid)