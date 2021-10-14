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
            power[i,j] = fading[i, j] * gain_bs[j, i, i, j] * gain_user[i, j, j, i] * path_loss[i,j]


    # ------------------------ Start of optimization program ------------------------------------
    try:
        m = gp.Model("Model 1")
        m.setParam('NonConvex', 2)
        # m.Params.LogToConsole = 0

        # -------------- VARIABLES -----------------------------------
        channel_capacity = m.addMVar(shape=(number_of_users, number_of_bs), vtype=GRB.CONTINUOUS, name = 'C')

        channel_capacity_per_user = m.addMVar(shape=(number_of_users,), vtype=GRB.CONTINUOUS, name = 'C_user')

        alpha = m.addMVar(shape=(number_of_users, number_of_bs, number_of_timeslots), vtype=GRB.BINARY, name = 'alpha' )

        SINR = m.addMVar(shape=(number_of_users, number_of_bs, number_of_timeslots), vtype = GRB.CONTINUOUS, name = 'SINR')
        interference = m.addMVar(shape=(number_of_users, number_of_bs, number_of_timeslots), vtype = GRB.CONTINUOUS, name = 'I')
        inverse_interference = m.addMVar(shape=(number_of_users, number_of_bs, number_of_timeslots), vtype = GRB.CONTINUOUS, name = 'I-1')
        sigma_interference = m.addMVar(shape=(number_of_users, number_of_bs, number_of_timeslots), vtype = GRB.CONTINUOUS, name = 'I-1')

        # ----------------- OBJECTIVE ----------------------------------
        m.setObjective(sum(channel_capacity_per_user), GRB.MAXIMIZE)

        # --------------- CONSTRAINTS -----------------------------
        # Define SINR and interference
        for i in users:
            for j in base_stations:
                for t in time_slots:
                    m.addConstr(sigma_interference[i,j,t] == sigma**2 + interference[i,j,t], name = 'sigma_interference')
                    m.addConstr(sigma_interference[i,j,t] @ inverse_interference[i, j, t] == 1, name='helper_constraint'+str(i) + '_' + str(j) + '_' + str(t))
                    m.addConstr(SINR[i,j,t] == power[i, j] * inverse_interference[i,j,t], name='find_SINR'+str(i) + '_' + str(j) + '_' + str(t))
                    m.addConstr(interference[i, j, t] == sum(sum(alpha[m, k,t] * fading[m, k] * gain_bs[k, m, i, j] * gain_user[i, j, k, m] * path_loss[i, k] for m in users) for k in base_stations) - power[i,j], name='Interference'+str(i) + '_' + str(j) + '_' + str(t))

        # Minimum SNR
        for i in users:
            for j in base_stations:
                for t in time_slots:
                    m.addConstr(SINR[i,j,t] >= alpha[i, j, t] * SINR_min, name = 'minimum_SNR_user'+ str(i) + '_BS' + str(j) + '_t=' + str(t))

        # Connections per BS
        for j in base_stations:
            for t in time_slots:
                m.addConstr(sum(alpha[i, j, t] for i in users) <= N_bs, name= 'connections_BS_BS' + str(j) + '_t=' + str(t))

        # Connections per user
        for i in users:
            for t in time_slots:
                m.addConstr(sum(alpha[i,j,t] for j in base_stations) <= N_user, name='connections_user'+str(i) + '_'  + str(t))

        # Rate requirement
        # for i in users:
        #     m.addConstr(sum(sum(SINR[i,j,t] for j in base_stations)for t in time_slots) >= min_rate, name='rate_requirement')

        # at least 1 connection:
        for i in users:
            m.addConstr(sum(sum(alpha[i,j,t] for j in base_stations) for t in time_slots) >= 1, name='1_con_user' + str(i))

        for i in users:
            for j in base_stations:
                m.addConstr(channel_capacity[i, j] == sum(alpha[i,j,t] @ SINR[i,j,t]  for t in time_slots) , name = 'channel_cap')
            m.addConstr(channel_capacity_per_user[i] == sum(channel_capacity[i,j] for j in base_stations) , name='channel_cap_user')

        # --------------------- OPTIMIZE MODEL -------------------------
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

    return alpha.X, channel_capacity_per_user.X

