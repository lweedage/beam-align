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


def optimization(alpha):
    # alpha = input('Alpha = ')
    # alpha = int(alpha)

    # ------------------------ Start of optimization program ------------------------------------
    try:
        m = gp.Model("Model 1")
        m.setParam('NonConvex', 2)
        m.Params.LogToConsole = 0

        # -------------- VARIABLES -----------------------------------
        x = {}
        SINR = {}
        SINR_user = {}
        C = {}
        log_C = {}
        SE_user = {}
        I = {}
        I_inv = {}
        sigma_I = {}

        log_obj = {}

        maxmin_obj = {}
        angles_u = {}
        angles_bs = {}

        for i in users:
            for j in base_stations:
                x[i, j] = m.addVar(vtype=GRB.BINARY, name=f'x#{i}#{j}')
                SINR[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'SINR#{i}#{j}')
                I[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'I#{i}#{j}')
                sigma_I[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'sigma_I#{i}#{j}')
                I_inv[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'I_inv#{i}#{j}')
                C[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'C#{i}#{j}')
                log_C[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'logC#{i}#{j}')

            SINR_user[i] = m.addVar(vtype=GRB.CONTINUOUS, name=f'SINR_user#{i}')
            SE_user[i] = m.addVar(vtype=GRB.CONTINUOUS, name=f'SE_user#{i}')
            # if alpha == 1:
            log_obj[i] = m.addVar(vtype=GRB.CONTINUOUS, name=f'log_obj_user#{i}')
            # elif alpha == 2:
            maxmin_obj[i] = m.addVar(vtype=GRB.CONTINUOUS, name=f'maxmin_obj_user#{i}')
        for j in base_stations:
            for d in directions_bs:
                angles_bs[j, d] = m.addVar(vtype=GRB.BINARY, name=f'angle_bs#{j}#{d}')
        for i in users:
            for d in directions_u:
                angles_u[i, d] = m.addVar(vtype=GRB.BINARY, name=f'angle_u#{i}#{d}')
        m.update()

        # ----------------- OBJECTIVE ----------------------------------
        if alpha == 1:
            m.setObjective(quicksum(log_obj[i] for i in users), GRB.MAXIMIZE)
        elif alpha == 0:
            m.setObjective(quicksum(SE_user[i] for i in users), GRB.MAXIMIZE)
        else:
            m.setObjective(1 / (1 - alpha) * quicksum(maxmin_obj[i] for i in users), GRB.MAXIMIZE)

        # --------------- CONSTRAINTS -----------------------------
        # Define SINR and interference
        if number_of_interferers > 0:
            for i in users:
                for j in base_stations:
                    m.addConstr(I[i, j] == quicksum(
                        quicksum(x[k, m] * interference[i, j, k, m] for k in users if not (i == k and j == m)) for m in
                        f.closest_bs(i)), name=f'Interference#{i}#{j}')
                    m.addConstr(sigma_I[i, j] == sigma + I[i, j], name=f'sigma_interference#{i}#{j}')
                    m.addConstr(sigma_I[i, j] * I_inv[i, j] == 1, name=f'helper_constraint#{i}#{j}')
                    m.addConstr(SINR[i, j] == x[i, j] * power[i, j] * I_inv[i, j], name=f'find_SINR#{i}#{j}')
        else:
            for i in users:
                for j in base_stations:
                    m.addConstr(SINR[i, j] == x[i, j] * power[i, j] / sigma, name=f'find_SINR#{i}#{j}')

        # Only 1 BS/User per angular direction
        for i in users:
            for d in directions_u:
                m.addConstr(angles_u[i, d] == quicksum(x[i, j] for j in base_stations if f.find_beam_number(
                    f.find_bore(f.user_coords(i), f.bs_coords(j), beamwidth_u), beamwidth_u) == d),
                            name=f'direction_user#{i}#{d}')
                m.addConstr(angles_u[i, d] <= 1, name = f'angle_u#{i}#{d}')

        for j in base_stations:
            for d in directions_bs:
                m.addConstr(angles_bs[j, d] == quicksum(x[i, j] for i in users if f.find_beam_number(
                    f.find_bore(f.bs_coords(j), f.user_coords(i), beamwidth_b), beamwidth_b) == d),
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

        # find spectral efficiency
        for i in users:
            for j in base_stations:
                m.addConstr(C[i, j] == (1 + SINR[i, j]), name=f'capacity#{i}#{j}')
                m.addGenConstrLog(C[i, j], log_C[i, j], name=f'log_C#{i}#{j}',
                                  options="FuncPieces=-1 FuncPieceError=0.001")
            m.addConstr(SE_user[i] == quicksum([log_C[i, j] for j in base_stations]), name=f'SE_user#{i}')

        # if alpha == 1:
        for i in users:
            m.addGenConstrLog(SE_user[i], log_obj[i], name=f'log_constraint#{i}', options="FuncPieces=-1 FuncPieceError=0.001")

        # elif alpha == 2:
        for i in users:
            m.addConstr(SE_user[i] * maxmin_obj[i] == 1, name=f'power_constraint#{i}')

        # --------------------- OPTIMIZE MODEL -------------------------
        # m.computeIIS()
        # m.write("IISmodel.lp")

        m.optimize()
        m.write("model.lp")
        m.getObjective()
        print('Objective value: %g' % m.objVal)




    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))
        sys.exit()

    a = np.zeros((number_of_users, number_of_bs))
    total_C = np.zeros(number_of_users)
    interf = np.zeros((number_of_users, number_of_bs))
    c = np.zeros((number_of_users, number_of_bs))

    angles = np.zeros((number_of_users, len(directions_u)))
    bs_angles = np.zeros((number_of_bs, len(directions_bs)))
    logC = np.zeros((number_of_users, number_of_bs))

    for i in range(number_of_users):
        total_C[i] = SE_user[i].X

    print(total_C)
    print(sum(total_C), sum([log_obj[i].X for i in users]), -1 * sum([maxmin_obj[i].X for i in users]))
    print(sum([math.log(total_C[i]) for i in users]))
    print(-sum([(total_C[i])**(-1) for i in users]))
    for i in users:
        for j in base_stations:
            a[i,j] = x[i,j].X

    # print(find_distance_matrix(x_user, y_user, x_bs, y_bs))
    # print(path_loss)
    # print('alpha = ', alpha)
    # print('Capacity sum:', sum(total_C), 'fairness =', f.fairness(total_C))
    return a, total_C
