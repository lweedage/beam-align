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
import functions as f
from parameters import *


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


def optimization(x_user, y_user):
    users = range(number_of_users)
    base_stations = range(number_of_bs)

    gain_bs = np.zeros((number_of_users, number_of_bs))
    gain_user = np.zeros((number_of_users, number_of_bs))
    power = np.zeros((number_of_users, number_of_bs))
    path_loss = np.zeros((number_of_users, number_of_bs))

    # calculating the gain, path_loss and interference for every user-bs pair
    for i in users:
        coords_i = f.user_coords(i, x_user, y_user)
        for j in base_stations:
            coords_j = f.bs_coords(j)
            path_loss[i, j] = f.find_path_loss(coords_i, coords_j)
            gain_bs[i, j] = f.find_gain(coords_j, coords_i, coords_j, coords_i, beamwidth_b)
            if user_misalignment:
                gain_user[i, j] = f.find_gain(coords_i, coords_j, coords_i, coords_j, beamwidth_u)
            else:
                gain_user[i, j] = f.find_user_gain(coords_i, coords_j, coords_i, coords_j, beamwidth_u)
            power[i, j] = transmission_power * gain_bs[i, j] * gain_user[i, j] / path_loss[i, j]

    # ------------------------ Start of optimization program ------------------------------------
    try:
        m = gp.Model("Model 1")
        m.setParam('NonConvex', 2)
        m.Params.LogToConsole = 0
        m.Params.OutputFlag = 0
        m.Params.Threads = 10

        # -------------- VARIABLES -----------------------------------
        x = {}
        SINR = {}
        SINR_user = {}
        C = {}
        log_C = {}
        C_user = {}

        angles_u = {}
        angles_bs = {}

        for i in users:
            for j in base_stations:
                x[i, j] = m.addVar(vtype=GRB.BINARY, name=f'x#{i}#{j}')
                SINR[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'SINR#{i}#{j}')
                C[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'C#{i}#{j}')
                log_C[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'logC#{i}#{j}')

            SINR_user[i] = m.addVar(vtype=GRB.CONTINUOUS, name=f'SINR_user#{i}')
            C_user[i] = m.addVar(vtype=GRB.CONTINUOUS, name=f'C_user#{i}')

        for j in base_stations:
            for d in directions_bs:
                angles_bs[j, d] = m.addVar(vtype=GRB.BINARY, name=f'angle_bs#{j}#{d}')
        for i in users:
            for d in directions_u:
                angles_u[i, d] = m.addVar(vtype=GRB.BINARY, name=f'angle_u#{i}#{d}')
        m.update()

        # ----------------- OBJECTIVE ----------------------------------
        m.setObjective(quicksum(C_user[i] for i in users), GRB.MAXIMIZE)

        # --------------- CONSTRAINTS -----------------------------
        # Define SINR and interference
        for i in users:
            for j in base_stations:
                m.addConstr(SINR[i, j] == x[i, j] * power[i, j] / noise, name=f'find_SINR#{i}#{j}')

        # Only 1 BS/User per angular direction
        for i in users:
            for d in directions_u:
                m.addConstr(angles_u[i, d] == quicksum(x[i, j] for j in base_stations if f.find_beam_number(
                    f.find_bore(f.user_coords(i, x_user, y_user), f.bs_coords(j), beamwidth_u), beamwidth_u) == d),
                            name=f'direction_user#{i}#{d}')
                m.addConstr(angles_u[i, d] <= 1, name = f'angle_u#{i}#{d}')

        for j in base_stations:
            for d in directions_bs:
                m.addConstr(angles_bs[j, d] == quicksum(x[i, j] for i in users if f.find_beam_number(
                    f.find_bore(f.bs_coords(j), f.user_coords(i, x_user, y_user), beamwidth_b), beamwidth_b) == d),
                            name=f'direction_bs#{j}#{d}')
                m.addConstr(angles_bs[j, d] <= 1, name=f'angle_bs#{j}#{d}')

        # Minimum SNR
        for i in users:
            for j in base_stations:
                m.addConstr(SINR[i, j] >= x[i, j] * SINR_min, name=f'minimum_SNR#{i}#{j}')

        # # Connections per BS
        for j in base_stations:
            m.addConstr(quicksum(x[i, j] for i in users) <= N_bs, name= f'connections_BS#{j}')

        # Connections per user
        for i in users:
            m.addConstr(quicksum(x[i,j] for j in base_stations) <= N_user, name=f'connections_user#{i}')

        # Rate requirement
        # for i in users:
        #     m.addConstr(quicksum(SINR[i,j] for j in base_stations) >= min_rate_SINR, name='rate_requirement')

        # at least 1 connection:
        for i in users:
            m.addConstr(quicksum(x[i, j] for j in base_stations) >= 1, name=f'1_con_user#{i}')

        # find channel capacity
        for i in users:
            for j in base_stations:
                m.addConstr(C[i, j] == (1 + SINR[i, j]), name=f'capacity#{i}#{j}')
                m.addGenConstrLog(C[i, j], log_C[i, j], name=f'log_C#{i}#{j}',
                                  options="FuncPieces=-1 FuncPieceError=0.01")
            m.addConstr(C_user[i] == quicksum([log_C[i, j] for j in base_stations]), name=f'C_user#{i}')

        # --------------------- OPTIMIZE MODEL -------------------------
        # m.computeIIS()
        # m.write("IISmodel.lp")

        m.optimize()
        # m.write("model.lp")
        # m.getObjective()
        # print('Objective value: %g' % m.objVal)



    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))
        sys.exit()

    a = np.zeros((number_of_users, number_of_bs))
    total_C = np.zeros(number_of_users)

    if m.status == 2:
        for i in range(number_of_users):
            total_C[i] = C_user[i].X
            # print([angles_u[i, j].X for j in directions_u])

        # print(total_C)
        for i in users:
            for j in base_stations:
                a[i,j] = x[i,j].X
    return a, total_C
