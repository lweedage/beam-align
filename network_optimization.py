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

def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3/4) * radius
    for i in range(0, int(xDelta/radius) + 1):
        for j in range(0, int(yDelta/dy) + 1):
            xbs.append(i*radius + 0.5*(j%2) * radius)
            ybs.append(j*dy)
    return xbs, ybs

# np.random.seed(49)
LOG_CHANNEL = 0
SUM_CHANNEL = 1
MIN_CHANNEL = 2
SOFT_SUM_CHANNEL = 3
UPF = 4

OBJECTIVE = SUM_CHANNEL
ANGLECONSTRAINT = False
SINR = False

radius = 15

number_of_bs = 20
number_of_users_1 = 10
number_of_users_2 = 10
number_of_users_3 = 10
number_of_users = number_of_users_1 + number_of_users_2 + number_of_users_3


max_distance = 2000

min_cap_type1 = 2
min_cap_type2 = 20
min_cap_type3 = 100

total_bandwidth = 10

minimum_angle = 45
minimum_angle = minimum_angle/180 * math.pi

# ------------------------------- Initialisation --------------------------------------------
def find_distance_matrix(xu, yu, xbs, ybs):
    distance = np.zeros((len(xu), len(xbs)))
    for i in range(len(xu)):
        for j in range(len(xbs)):
            # x = np.minimum((xu[i] - xbs[j]) % xMax, (xbs[j] - xu[i]) % xMax)
            # y = np.minimum((yu[i] - ybs[j]) % yMax, (ybs[j] - yu[i]) % yMax)
            x = xu[i] - xbs[j]
            y = yu[i] - ybs[j]
            distance[i, j] = np.sqrt(x ** 2 + y ** 2)
    return distance

def find_SINR():
    sinr = np.zeros((len(xu), len(xbs)))
    for i in range(len(xu)):
        for j in range(len(xbs)):
            sinr[i, j] = power * distances[i, j]**(-path_loss) / (noise + power * sum(distances[i, k]**(-path_loss) for k in range(len(xbs)) if k != j))
    return np.log2(1 + sinr)

power = 10000
noise = 10
c = power/noise
path_loss = 2

xMin, xMax = 0, 59
yMin, yMax = 0, 51

minimum_channel_capacity = np.concatenate((np.ones(number_of_users_1) * min_cap_type1, np.ones(number_of_users_2) * min_cap_type2, np.ones(number_of_users_3) * min_cap_type3), axis=None)

total_connections = np.zeros((xMax, yMax))
total_visits = np.zeros((xMax, yMax))
closest = np.zeros((xMax, yMax))

seed = 5

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

xbs, ybs = initialise_graph_triangular(radius, xMax, yMax)
number_of_bs = len(xbs)
print(number_of_bs)
# name = 'Simulations/torus_bs' + str(number_of_bs) + 'seed' + str(seed)

for iteration in range(1):
    np.random.seed(iteration)
    # xu1 = np.random.uniform(xMin, xMin + 0.5 * xMax, number_of_users_1)
    # yu1 = np.random.uniform(yMin, yMax, number_of_users_1)
    # xu2 = np.random.uniform(xMin + 0.5 * xMax, xMax, number_of_users_2)
    # yu2 = np.random.uniform(yMin, yMax, number_of_users_2)

    # xu = [*xu1, *xu2]
    # yu = [*yu1, *yu2]

    xu = np.random.uniform(xMin, xMax, number_of_users)
    yu = np.random.uniform(yMin, yMax, number_of_users)

    np.random.seed(seed)
    # xbs = np.random.uniform(xMin, xMax, number_of_bs)
    # ybs = np.random.uniform(yMin, yMax, number_of_bs)
    xbs, ybs = initialise_graph_triangular(radius, xMax, yMax)
    number_of_bs = len(xbs)

    distances = find_distance_matrix(xu, yu, xbs, ybs)
    logSNR = np.log2(1 + c * np.power(distances, -path_loss))
    logSINR = find_SINR()


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

        channel_capacity_per_user = m.addMVar(shape=(number_of_users,), vtype=GRB.CONTINUOUS)
        channel_capacity_per_user_var = channel_capacity_per_user.tolist()

        angle_soft_constraint = m.addVar(vtype=GRB.CONTINUOUS)

        alpha = m.addMVar(shape=(number_of_users, number_of_bs), vtype=GRB.BINARY)

        if OBJECTIVE == LOG_CHANNEL:
            logarithm_objective = m.addMVar(shape=(number_of_users,))
            logarithm_objective_var = logarithm_objective.tolist()
        if OBJECTIVE == MIN_CHANNEL:
            minimum_objective = m.addVar()

        penalty = m.addMVar(shape = (number_of_users, ), vtype=GRB.CONTINUOUS, lb = 0)

        penalty_importantness = 100
        # ----------------- OBJECTIVE ----------------------------------
        if OBJECTIVE == SUM_CHANNEL:
            m.setObjective(sum(channel_capacity_per_user) - penalty_importantness * sum(penalty), GRB.MAXIMIZE)
        elif OBJECTIVE == LOG_CHANNEL:
            m.setObjective(sum(logarithm_objective) - penalty_importantness * sum(penalty), GRB.MAXIMIZE)
        elif OBJECTIVE == MIN_CHANNEL:
            m.setObjectiveN(minimum_objective, 0)
        # m.setObjectiveN(-penalty, 1)
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
                m.addConstr(channel_capacity[i, j] <= alpha[i, j] * total_bandwidth * logSNR[i,j], name = 'capalpha1')
                m.addConstr(channel_capacity[i, j] >= alpha[i, j] * 0.01, name = 'capalpha2')


        # Capacity constraint

        for i in users:
            m.addConstr(sum(channel_capacity[i, :]) >= minimum_channel_capacity[i] * (1 - penalty[i]), name="Minimum capacity - relaxed")

        # Distance constraint
        for i in users:
            for j in base_stations:
                if distances[i, j] > max_distance:
                    m.addConstr(channel_capacity[i, j] == 0, name = "Distance constraint")

        if ANGLECONSTRAINT:
            for i in users:
                for j in base_stations:
                    for l in base_stations:
                        if j != l:
                            m.addConstr((alpha[i, j] + alpha[i, l] - 1) * minimum_angle <= find_angle(i, j, l) , 'Angle')
                            # m.addConstr((alpha[i, j] + alpha[i, l] - 1) * angle_soft_constraint <= find_angle(i, j, l) , 'Angle')

        # Logarithmic objective constraint
        if OBJECTIVE == LOG_CHANNEL:
            for i in users:
                m.addGenConstrLog(channel_capacity_per_user_var[i], logarithm_objective_var[i], name='log_constraint')

        # Minimum channel_per_user constraint
        if OBJECTIVE == MIN_CHANNEL:
            m.addGenConstrMin(minimum_objective, channel_capacity_per_user_var, name = "min_constraint")


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

    # print('Penalty =', penalty.X)


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
            # nodesize.append(10)
            # labels[node + number_of_bs] = f'U{node}'
        for bs in range(number_of_bs):
            for user in range(len(xu)):
                if bandwidth[user, bs] > 0:
                    G.add_edge(user + number_of_bs, bs, bw = bandwidth[user, bs])
                    edgesize.append(bandwidth[user, bs] / np.max(bandwidth) * 10)
        # for user in range(len(xu)):
        #     if G.degree(user + number_of_bs) > 1:
        #         nodesize[user + number_of_bs] = 30
        #         colorlist[user + number_of_bs] = ('r')
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

    G, colorlist, nodesize, edgesize, labels = make_graph(xbs, ybs, xu, yu, channel_capacity.X)
    draw_graph(G, colorlist, nodesize, edgesize, labels)
    plt.title('ctc' + str(iteration))
    # plt.savefig('ctc' + str(iteration) + '.png')
    plt.show()
    print(iteration)
    print(penalty.X)

    name = 'users=' + str(number_of_users) + 'bs=' + str(number_of_bs) + 'obj=' + str(OBJECTIVE)
    connections, connections_per_bs, connections_per_user = number_of_connections(channel_capacity.X)


    def find_distance(xu, yu, xbs, ybs):
        xx = xu - xbs
        yy = yu - ybs
        return np.sqrt(xx ** 2 + yy ** 2)

    def find_bs(x, y, xbs, ybs):
        indices = find_distance(x, y, xbs, ybs).argsort()
        return indices[0]



    # print("Connections:", connections_per_bs, connections_per_user)
    # print('Channel capacity per user:', channel_capacity_per_user.X)
    # print('Bandwidth per base station:', sum(channel_capacity.X / logSNR))
    # print('Total channel capacity:', channel_capacity.X.sum())
    # print(channel_capacity.X/logSNR)
    # print('Penalty:', penalty.X)


print(xbs, ybs)

print(find_distance(xbs[4], ybs[4], xbs[8], ybs[8]))
print(find_distance(xbs[6], ybs[6], xbs[4], ybs[4]))