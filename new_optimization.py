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
from parameters import *
import functions as f

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

def number_of_connections(channel_capacity):
    connections = channel_capacity > 0
    connections = connections.astype(int)
    connections_per_bs = sum(connections)
    connections_per_user = sum(connections.transpose())
    return connections, connections_per_bs, connections_per_user


def optimization():
    users = range(number_of_users)
    base_stations = range(number_of_bs)
    time_slots = range(number_of_timeslots)

    gain_bs = np.zeros((number_of_bs, number_of_users, number_of_users, number_of_bs))
    gain_user = np.zeros((number_of_users, number_of_bs, number_of_bs, number_of_users))
    power = np.zeros((number_of_users, number_of_bs))
    path_loss = np.zeros((number_of_users, number_of_bs))

    for i in users:
        for j in base_stations:
            for k in users:
                for m in base_stations:
                    gain_bs[j, i, k, m] = f.gain_bs(j, i, k, m)
                    gain_user[i, j, m, k] = f.gain_user(i, j, m, k)
            path_loss[i,j] = f.path_loss(i,j)
            power[i,j] = gain_bs[j, i, i, j] * gain_user[i, j, j, i] * path_loss[i,j] * fading[i, j]

    print(gain_bs)
    # ------------------------ Start of optimization program ------------------------------------
    try:
        m = gp.Model("Model 1")
        m.setParam('NonConvex', 2)
        # m.Params.LogToConsole = 0

        # -------------- VARIABLES -----------------------------------
        alpha = {}
        SINR = {}
        C = {}
        C_user = {}
        I = {}
        I_inv = {}
        sigma_I = {}



        for i in users:
            for j in base_stations:
                for t in time_slots:
                    alpha[i,j,t] = m.addVar(vtype = GRB.BINARY, name = f'alpha#{i}#{j}#{t}')
                    SINR[i,j,t] = m.addVar(vtype = GRB.CONTINUOUS, name = f'SINR#{i}#{j}#{t}')
                    I[i,j,t] = m.addVar(vtype = GRB.CONTINUOUS, name = f'I#{i}#{j}#{t}')
                    sigma_I[i,j,t] = m.addVar(vtype = GRB.CONTINUOUS, name = f'sigma_I#{i}#{j}#{t}')
                    I_inv[i,j,t] = m.addVar(vtype = GRB.CONTINUOUS, name = f'I_inv#{i}#{j}#{t}')
                C[i,j] = m.addVar(vtype = GRB.CONTINUOUS, name = f'C#{i}#{j}')
            C_user[i] = m.addVar(vtype= GRB.CONTINUOUS, name = f'C_user#{i}')


        m.update()

        # ----------------- OBJECTIVE ----------------------------------
        m.setObjective(quicksum(quicksum(quicksum(alpha[i,j,t] * SINR[i,j,t] for t in time_slots) for j in base_stations) for i in users), GRB.MAXIMIZE)

        # --------------- CONSTRAINTS -----------------------------
        # Define SINR and interference
        for i in users:
            for j in base_stations:
                for t in time_slots:
                    m.addConstr(I[i, j, t] == quicksum(quicksum(alpha[m, k, t] * fading[m, k] * gain_bs[k, m, i, j] * gain_user[i, j, k, m] * path_loss[i, k] for m in users) for k in base_stations) - power[i,j] * alpha[i,j,t], name=f'Interference#{i}#{j}#{t}')
                    m.addConstr(sigma_I[i,j,t] == sigma**2 + I[i,j,t], name = f'sigma_interference#{i}#{j}#{t}')
                    m.addConstr(sigma_I[i,j,t] * I_inv[i, j, t] == 1, name=f'helper_constraint#{i}#{j}#{t}')
                    m.addConstr(SINR[i,j,t] == power[i, j] * I_inv[i,j,t], name=f'find_SINR#{i}#{j}#{t}')

        # Minimum SNR
        for i in users:
            for j in base_stations:
                for t in time_slots:
                    m.addConstr(SINR[i,j,t] >= alpha[i, j, t] * SINR_min, name = f'minimum_SNR#{i}#{j}#{t}')

        # Connections per BS
        for j in base_stations:
            for t in time_slots:
                m.addConstr(quicksum(alpha[i, j, t] for i in users) <= N_bs, name= f'connections_BS#{j}#{t}')

        # Connections per user
        for i in users:
            for t in time_slots:
                m.addConstr(quicksum(alpha[i,j,t] for j in base_stations) <= N_user, name=f'connections_user#{i}#{t}')

        # Rate requirement
        # for i in users:
        #     m.addConstr(sum(sum(SINR[i,j,t] for j in base_stations)for t in time_slots) >= min_rate, name='rate_requirement')

        # at least 1 connection:
        for i in users:
            m.addConstr(quicksum(quicksum(alpha[i,j,t] for j in base_stations) for t in time_slots) >= 1, name=f'1_con_user#{i}')

        # find capacity
        # for i in users:
        #     for j in base_stations:
        #         m.addConstr(C[i, j] == quicksum(alpha[i,j,t] * SINR[i,j, t] for t in time_slots) , name = f'channel_cap#{i}#{j}')
        #     m.addConstr(C_user[i] ==  , name=f'channel_cap_user#{i}')

        # --------------------- OPTIMIZE MODEL -------------------------
        # m.computeIIS()
        # m.write("IISmodel.lp")

        m.optimize()
        m.write("model.lp")
        m.getObjective()
        print('Objective value: %g' % m.objVal)




    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))
        # sys.exit()

    except AttributeError:
        print('Encountered an attribute error')
        # sys.exit()

    a = np.zeros((number_of_users, number_of_bs, number_of_timeslots))
    capacity = np.zeros((number_of_users))

    for i in range(number_of_users):
        for j in range(number_of_bs):
            for t in range(number_of_timeslots):
                a[i, j, t] = alpha[i, j, t].X
        capacity[i] = C_user[i].X

    return a, capacity

