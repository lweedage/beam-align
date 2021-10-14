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

xMin, xMax = 0, 59  # in the case of hexagonal grid
yMin, yMax = 0, 51  # in the case of hexagonal grid

min_cap_type1 = 2
min_cap_type2 = 20
min_cap_type3 = 100

radius = 15
number_of_bs = 16

max_distance = 2000

total_bandwidth = 50

power = 1000
noise = 1
c = power / noise
path_loss = 2

seed = 5


def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3/4) * radius
    for i in range(0, int(xDelta/radius) + 1):
        for j in range(0, int(yDelta/dy) + 1):
            xbs.append(i*radius + 0.5*(j%2) * radius)
            ybs.append(j*dy)
    return xbs, ybs

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

def number_of_connections(channel_capacity):
    connections = channel_capacity > 0
    connections = connections.astype(int)
    connections_per_bs = sum(connections)
    connections_per_user = sum(connections.transpose())
    return connections, connections_per_bs, connections_per_user


def optimization(hexagonal, ppp, number_of_users_1, number_of_users_2, number_of_users_3, OBJECTIVE, penalty_importantness, iteration, one_connection = False):
    number_of_users = number_of_users_1 + number_of_users_2 + number_of_users_3
    minimum_channel_capacity = np.concatenate((np.ones(number_of_users_1) * min_cap_type1, np.ones(number_of_users_2) * min_cap_type2, np.ones(number_of_users_3) * min_cap_type3), axis=None)

    # ------------------------------- Initialisation --------------------------------------------
    np.random.seed(iteration)
    number_of_bs = 16

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

        if OBJECTIVE == 0:
            logarithm_objective = m.addMVar(shape=(number_of_users,))
            logarithm_objective_var = logarithm_objective.tolist()

        penalty = m.addMVar(shape=(3,), vtype=GRB.CONTINUOUS, lb=0)


        # ----------------- OBJECTIVE ----------------------------------
        if OBJECTIVE == 1:
            m.setObjective(sum(channel_capacity_per_user) - penalty_importantness * sum(penalty), GRB.MAXIMIZE)
        elif OBJECTIVE == 0:
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
        if OBJECTIVE == 0:
            for i in users:
                m.addGenConstrLog(channel_capacity_per_user_var[i], logarithm_objective_var[i], name='log_constraint')

        if one_connection:
            for i in users:
                m.addConstr(sum(alpha[i,:]) == 1, name = 'One connection')

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

    connections, connections_per_bs, connections_per_user = number_of_connections(channel_capacity.X)
    return connections, bandwidth.X

def bandwidth_optimization(hexagonal, ppp, number_of_users_1, number_of_users_2, number_of_users_3, OBJECTIVE, penalty_importantness, iteration, alpha):
    number_of_users = number_of_users_1 + number_of_users_2 + number_of_users_3
    minimum_channel_capacity = np.concatenate((np.ones(number_of_users_1) * min_cap_type1, np.ones(number_of_users_2) * min_cap_type2, np.ones(number_of_users_3) * min_cap_type3), axis=None)

    # ------------------------------- Initialisation --------------------------------------------
    np.random.seed(iteration)
    number_of_bs = 16

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

    # ------------------------ Start of optimization program ------------------------------------
    try:
        m = gp.Model("Model 1")
        m.Params.LogToConsole = 0

        # -------------- VARIABLES -----------------------------------
        channel_capacity = m.addMVar(shape=(number_of_users, number_of_bs), vtype=GRB.CONTINUOUS)
        bandwidth = m.addMVar(shape=(number_of_users, number_of_bs), vtype=GRB.CONTINUOUS)

        channel_capacity_per_user = m.addMVar(shape=(number_of_users,), vtype=GRB.CONTINUOUS)
        channel_capacity_per_user_var = channel_capacity_per_user.tolist()

        if OBJECTIVE == 0:
            logarithm_objective = m.addMVar(shape=(number_of_users,))
            logarithm_objective_var = logarithm_objective.tolist()

        penalty = m.addMVar(shape=(3,), vtype=GRB.CONTINUOUS, lb=0)


        # ----------------- OBJECTIVE ----------------------------------
        if OBJECTIVE == 1:
            m.setObjective(sum(channel_capacity_per_user) - penalty_importantness * sum(penalty), GRB.MAXIMIZE)
        elif OBJECTIVE == 0:
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
        if OBJECTIVE == 0:
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

    connections, connections_per_bs, connections_per_user = number_of_connections(channel_capacity.X)
    return connections, bandwidth.X