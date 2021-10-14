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

ONE_CONNECTION = False
CLOSEST_CONNECTION = False
PROBABILITY_POLICY = False
THRESHOLD_POLICY = False

# np.random.seed(49)
LOG_CHANNEL = 0
SUM_CHANNEL = 1
MIN_CHANNEL = 2
SOFT_SUM_CHANNEL = 3
UPF = 4

OBJECTIVE = SUM_CHANNEL
ANGLECONSTRAINT = False
SINR = False

# ONE_CONNECTION = True
CLOSEST_CONNECTION = True
PROBABILITY_POLICY = True
# THRESHOLD_POLICY = True
p = 0.5

for p in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
# for p in [0.2, 0.4, 0.6, 0.8, 1, 1.5, 2, 5, 10, 25, 100]:
# for p in [1]:
    number_of_bs = 8
    number_of_users = 50

    number_of_iterations = 1000
    log_obj = []
    sum_obj = []

    if OBJECTIVE == LOG_CHANNEL:
        obj = 'log'
    elif OBJECTIVE == SUM_CHANNEL:
        obj = 'sum'
    elif OBJECTIVE == MIN_CHANNEL:
        obj = 'min'

    if SINR:
        snr_sinr = 'SINR'
    else:
        snr_sinr = 'SNR'

    if ONE_CONNECTION:
        method = 'one_connection'
    elif PROBABILITY_POLICY and CLOSEST_CONNECTION or THRESHOLD_POLICY and CLOSEST_CONNECTION:
        method = 'probability_and_closest_connection' + str(p)
    elif CLOSEST_CONNECTION:
        method = 'closest_connection'
    elif PROBABILITY_POLICY or THRESHOLD_POLICY:
        method = 'probability_policy' + str(p)
    else:
        method = 'optimal'

    seed = 5

    radius = 150
    power = 10000
    noise = 10
    c = power / noise
    path_loss = 2

    xMin, xMax = 0, 300
    yMin, yMax = 0, 300

    def initialise_graph_triangular(radius, xDelta, yDelta):
        xbs, ybs = list(), list()
        dy = math.sqrt(3/4) * radius
        for i in range(0, int(xDelta/radius) + 1):
            for j in range(0, int(yDelta/dy) + 1):
                xbs.append(i*radius + 0.5*(j%2) * radius)
                ybs.append(j*dy)
        return xbs, ybs


    xbs, ybs = initialise_graph_triangular(radius, xMax, yMax)
    number_of_bs = len(xbs)
    print(number_of_bs)
    name = 'Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + method + str(number_of_iterations)



    for user_seed in range(number_of_iterations):
        print('Users:', number_of_users, 'Iterations:', user_seed)
        type_1 = number_of_users  # int(math.floor(number_of_users/2))
        type_2 = number_of_users - type_1

        max_distance = 500000

        min_cap_type1 = 10
        min_cap_type2 = 10

        total_bandwidth = 10000

        minimum_angle = 45
        minimum_angle = minimum_angle / 180 * math.pi


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


        def find_SINR():
            sinr = np.zeros((len(xu), len(xbs)))
            for i in range(len(xu)):
                for j in range(len(xbs)):
                    sinr[i, j] = min(1, power * distances[i, j] ** (-path_loss) / (
                                noise + power * sum(distances[i, k] ** (-path_loss) for k in range(len(xbs)) if k != j)))
            return np.log2(1 + sinr)

        def find_SNR():
            snr = np.zeros((len(xu), len(xbs)))
            for i in range(len(xu)):
                for j in range(len(xbs)):
                    snr[i, j] = min(1, power * distances[i, j] ** (-path_loss) / (
                                noise ))
            return np.log2(1 + snr)



        minimum_channel_capacity = np.concatenate((np.ones(type_1) * min_cap_type1, np.ones(type_2) * min_cap_type2), axis=None)


        np.random.seed(user_seed)
        xu = np.random.uniform(xMin, xMax, number_of_users)
        yu = np.random.uniform(yMin, yMax, number_of_users)

        np.random.seed(seed)
        # ybs = np.random.uniform(yMin, yMax, number_of_bs)
        # xbs = np.random.uniform(xMin, xMax, number_of_bs)

        xbs, ybs = initialise_graph_triangular(radius, xMax, yMax)
        number_of_bs = len(xbs)

        distances = find_distance_matrix(xu, yu, xbs, ybs)
        logSNR = find_SNR()
        logSINR = find_SINR()

        users = range(number_of_users)
        base_stations = range(number_of_bs)

        # ---------------------- Checking if model is feasible
        if max_distance < max([min(distances[i, :]) for i in users]):
            print('Maximum user distance is too close')
            sys.exit()


        def find_angle(user, bs1, bs2):
            slope1 = (ybs[bs1] - yu[user]) / (xbs[bs1] - yu[user])
            slope2 = (ybs[bs2] - yu[user]) / (xbs[bs2] - yu[user])
            angle = math.atan(abs((slope2 - slope1) / (1 + slope1 * slope2)))
            return angle

        def find_distance(xu, yu, xbs, ybs):
            xx = xu - xbs
            yy = yu - ybs
            return np.sqrt(xx ** 2 + yy ** 2)

        def find_bs(x, y, xbs, ybs):
            indices = find_distance(x, y, xbs, ybs).argsort()
            return indices[:2]

        def snr_sum_probability(x, y):
            bs0, bs1 = find_bs(x, y, xbs, ybs)
            r0 = find_distance(x, y, xbs[bs0], ybs[bs0])
            r1 = find_distance(x, y, xbs[bs1], ybs[bs1])
            d = find_distance(xbs[bs0], ybs[bs0], xbs[bs1], ybs[bs1])
            area = r0 ** 2 * math.acos((d ** 2 + r0 ** 2 - r1 ** 2) / (2 * d * r0)) + r1 ** 2 * math.acos((d ** 2 + r1 ** 2 - r0 ** 2) / (2 * d * r1)) - 0.5 * math.sqrt(
                (-d + r0 + r1) * (d + r0 - r1) * (d - r0 + r1) * (d + r0 + r1))
            return math.exp(-number_of_users/(xMax * yMax) * (math.pi * (r0 ** 2 + r1 ** 2) - area))


        def sinr_probability(x, y):
            bs0, bs1 = find_bs(x, y, xbs, ybs)
            SINR = power * find_distance(x, y, xbs[bs0], ybs[bs0]) ** (-path_loss) / (noise + power * sum(
                find_distance(x, y, xbs[k], ybs[k]) ** (-path_loss) for k in range(len(xbs)) if k != bs0))
            return SINR

        def snr_probability(x, y):
            bs0, bs1 = find_bs(x, y, xbs, ybs)
            SNR = power * find_distance(x, y, xbs[bs0], ybs[bs0]) ** (-path_loss) / (noise)
            if find_distance(x,y, xbs[bs0], ybs[bs0]) <= 1:
                return power/noise
            else:
                return SNR

        # ------------------------ Start of optimization program ------------------------------------
        try:
            m = gp.Model("Model 1")
            m.Params.LogToConsole = 0

            # -------------- VARIABLES -----------------------------------
            channel_capacity = m.addMVar(shape=(number_of_users, number_of_bs), vtype=GRB.CONTINUOUS)

            channel_capacity_per_user = m.addMVar(shape=(number_of_users,), vtype=GRB.CONTINUOUS)
            channel_capacity_per_user_var = channel_capacity_per_user.tolist()

            angle_soft_constraint = m.addVar(vtype=GRB.CONTINUOUS)

            alpha = m.addMVar(shape=(number_of_users, number_of_bs), vtype=GRB.BINARY)

            if OBJECTIVE == LOG_CHANNEL:
                logarithm_objective = m.addMVar(shape=(number_of_users,))
                logarithm_objective_var = logarithm_objective.tolist()
            if OBJECTIVE == MIN_CHANNEL:
                minimum_objective = m.addVar()

            penalty = m.addMVar(shape=(number_of_users,), lb=0)

            penalty_importantness = 100
            # ----------------- OBJECTIVE ----------------------------------
            if OBJECTIVE == SUM_CHANNEL:
                m.setObjective(sum(channel_capacity_per_user) - penalty_importantness * sum(penalty), GRB.MAXIMIZE)
            elif OBJECTIVE == LOG_CHANNEL:
                m.setObjective(sum(logarithm_objective) - penalty_importantness * sum(penalty), GRB.MAXIMIZE)
            elif OBJECTIVE == MIN_CHANNEL:
                m.setObjective(minimum_objective, GRB.MAXIMIZE)
            elif OBJECTIVE == SOFT_SUM_CHANNEL:
                m.setObjectiveN(penalty, 0)
                # m.setObjectiveN(-sum(channel_capacity_per_user) + penalty[0]*5 + penalty[1]*5, 0)
            # m.setObjectiveN(angle_soft_constraint, 1)

            # --------------- CONSTRAINTS -----------------------------
            # Per-user channel capacity
            m.addConstrs(sum(channel_capacity[i, :]) == channel_capacity_per_user[i] for i in users)

            # Bandwidth constraint
            for j in base_stations:
                if SINR:
                    m.addConstr(sum(channel_capacity[i, j] / logSINR[i, j] for i in users) <= total_bandwidth,
                                name="total_bandwidth")
                else:
                    m.addConstr(sum(channel_capacity[i, j] / logSNR[i, j] for i in users) <= total_bandwidth,
                                name="total_bandwidth")

            for i in users:
                for j in base_stations:
                    m.addConstr(channel_capacity[i, j] <= alpha[i, j] * total_bandwidth * logSNR[i, j], name='capalpha1')
                    m.addConstr(channel_capacity[i, j] >= alpha[i, j] * 0.01, name='capalpha2')

            # Capacity constraint
            for i in users:
                m.addConstr(sum(channel_capacity[i, :]) >= minimum_channel_capacity[i] * (1 - penalty[i]),
                            name="Minimum capacity - relaxed")

            # Distance constraint
            for i in users:
                for j in base_stations:
                    if distances[i, j] > max_distance:
                        m.addConstr(channel_capacity[i, j] == 0, name="Distance constraint")

            if ANGLECONSTRAINT:
                for i in users:
                    for j in base_stations:
                        for l in base_stations:
                            if j != l:
                                m.addConstr((alpha[i, j] + alpha[i, l] - 1) * minimum_angle <= find_angle(i, j, l), 'Angle')
                                # m.addConstr((alpha[i, j] + alpha[i, l] - 1) * angle_soft_constraint <= find_angle(i, j, l) , 'Angle')

            # Logarithmic objective constraint
            if OBJECTIVE == LOG_CHANNEL:
                for i in users:
                    m.addGenConstrLog(channel_capacity_per_user_var[i], logarithm_objective_var[i], name='log_constraint')

            # Minimum channel_per_user constraint
            if OBJECTIVE == MIN_CHANNEL:
                m.addGenConstrMin(minimum_objective, channel_capacity_per_user_var, name="min_constraint")

            # One connection per user
            if ONE_CONNECTION:
                for i in users:
                    m.addConstr(sum(alpha[i, j] for j in base_stations) <= 1, name = 'one_connection')

            if PROBABILITY_POLICY and CLOSEST_CONNECTION:
                for i in users:
                    if snr_sum_probability(xu[i], yu[i]) < p:
                        m.addConstr(sum(alpha[i, j] for j in base_stations) >= 2, name= 'new_policy')
                        m.addConstr(alpha[i, distances[i, :].argsort()[0]] >= 1, name='connect_to_closest')
                        m.addConstr(alpha[i, distances[i, :].argsort()[1]] >= 1, name='connect_to_2nd_closest')

                    else:
                        m.addConstr(sum(alpha[i, j] for j in base_stations) <= 1, name = 'one_connection')
                        m.addConstr(alpha[i, distances[i, :].argsort()[0]] >= 1, name='connect_to_closest')

            elif PROBABILITY_POLICY:
                for i in users:
                    if snr_sum_probability(xu[i], yu[i]) > p:
                        m.addConstr(sum(alpha[i, j] for j in base_stations) >= 2, name='new_policy')
                    else:
                        m.addConstr(sum(alpha[i, j] for j in base_stations) <= 1, name='one_connection')
            elif CLOSEST_CONNECTION:
                for i in users:
                    m.addConstr(sum(alpha[i, j] for j in base_stations) <= 1, name='one_connection')
                    m.addConstr(alpha[i, distances[i, :].argsort()[0]] >= 1, name='connect_to_closest')


            # if THRESHOLD_POLICY and CLOSEST_CONNECTION:
            #     for i in users:
            #         if snr_probability(xu[i], yu[i]) < p:
            #             m.addConstr(sum(alpha[i, j] for j in base_stations) >= 2, name= 'new_policy')
            #             m.addConstr(alpha[i, distances[i, :].argsort()[0]] >= 1, name='connect_to_closest')
            #             m.addConstr(alpha[i, distances[i, :].argsort()[1]] >= 1, name='connect_to_2nd_closest')
            #
            #         else:
            #             m.addConstr(sum(alpha[i, j] for j in base_stations) <= 1, name='one_connection')
            #             m.addConstr(alpha[i, distances[i, :].argsort()[0]] >= 1, name='connect_to_closest')
            #
            # elif THRESHOLD_POLICY:
            #     for i in users:
            #         if snr_probability(xu[i], yu[i]) < p:
            #             m.addConstr(sum(alpha[i, j] for j in base_stations) >= 2, name= 'new_policy')
            #         else:
            #             m.addConstr(sum(alpha[i, j] for j in base_stations) <= 1, name = 'one_connection')
            #
            # elif CLOSEST_CONNECTION:
            #     for i in users:
            #         m.addConstr(sum(alpha[i, j] for j in base_stations) <= 1, name='one_connection')
            #         m.addConstr(alpha[i, distances[i, :].argsort()[0]] >= 1, name='connect_to_closest')
            # --------------------- OPTIMIZE MODEL -------------------------
            m.optimize()

            m.getObjective()
            print('Objective value: %g' % m.objVal)

        except gp.GurobiError as e:
           print('Error code ' + str(e.errno) + ': ' + str(e))
           # sys.exit()

        except AttributeError:
           print('Encountered an attribute error')
           # sys.exit()

        # -------------------------- Plotting the solution --------------------------------------
        def make_graph(xbs, ybs, xpop, ypop, connections, bandwidth):
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
            for node in range(len(xu)):
                G.add_node(node + number_of_bs, x=xpop[node], y=ypop[node])
                if node < type_1:
                    colorlist.append('g')
                else:
                    colorlist.append('r')
                nodesize.append(10)
                # labels[node + number_of_bs] = f'U{node}'
            for bs in range(number_of_bs):
                for user in range(len(xu)):
                    if connections[user, bs] == 1:
                        G.add_edge(user + number_of_bs, bs, bw=bandwidth[user, bs])
                        # edgesize.append(bandwidth[user, bs] / np.max(bandwidth) * 10)
                        edgesize.append(1)
            for user in range(len(xu)):
                if G.degree(user + number_of_bs) > 1:
                    nodesize[user + number_of_bs] = 30
                    colorlist[user + number_of_bs] = ('r')
            return G, colorlist, nodesize, edgesize, labels


        def draw_graph(G, colorlist, nodesize, edgesize, labels, ax):
            pos = dict()
            for node in G.nodes():
                pos[node] = (nx.get_node_attributes(G, 'x')[node], nx.get_node_attributes(G, 'y')[node])
            nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_size=nodesize,
                                   node_color=colorlist, ax=ax)
            nx.draw_networkx_edges(G, pos, edge_color='black', alpha=0.5, width=edgesize)
            ax.set_xlim([xMin, xMax]), ax.set_ylim([yMin, yMax])
            nx.draw_networkx_labels(G, pos, labels, font_size=10)


        def number_of_connections(alpha):
            connections = alpha
            connections_per_bs = sum(alpha)
            connections_per_user = sum(alpha.transpose())
            return connections, connections_per_bs, connections_per_user

        connections, connections_per_bs, connections_per_user = number_of_connections(alpha.X)
        # print("Connections:", connections_per_bs, connections_per_user)
        # print('Channel capacity per user:', channel_capacity_per_user.X)
        # print('Bandwidth per base station:', sum(channel_capacity.X / logSNR))
        # print('Total channel capacity:', channel_capacity.X.sum())
        # print(penalty.X)
        # #
        # fig, ax = plt.subplots()
        #
        # G, colorlist, nodesize, edgesize, labels = make_graph(xbs, ybs, xu, yu, connections, channel_capacity.X)
        # draw_graph(G, colorlist, nodesize, edgesize, labels, ax)
        #
        # plt.text(1, xMax + 2, '$\sum_{i,j}C_{ij} = $' + str(sum(channel_capacity_per_user.X)))
        # plt.show()
        blub = channel_capacity_per_user.X

        log_obj.append(sum([math.log(blub[i]) for i in range(number_of_users)]))
        sum_obj.append(sum(channel_capacity_per_user.X))

    np.savetxt(name + 'log_obj.txt', log_obj)
    np.savetxt(name + 'sum_obj.txt', sum_obj)