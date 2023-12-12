import sys

import gurobipy as gp
from gurobipy import GRB
from gurobipy import quicksum

import functions as f
from parameters import *


def number_of_connections(channel_capacity):
    connections = channel_capacity > 0
    connections = connections.astype(int)
    connections_per_bs = sum(connections)
    connections_per_user = sum(connections.transpose())
    return connections, connections_per_bs, connections_per_user


def optimization(x_user, y_user, N):
    number_of_users = len(x_user)
    users = range(number_of_users)
    base_stations = range(number_of_bs)

    gain_bs = np.zeros((number_of_users, number_of_bs))
    gain_user = np.zeros((number_of_users, number_of_bs))
    # SNR = np.zeros((number_of_users, number_of_bs))

    path_loss = np.zeros((number_of_users, number_of_bs))
    # spectral_efficiency = np.zeros((number_of_users, number_of_bs))

    user_beamnumber = np.zeros((number_of_users, number_of_bs))
    bs_beamnumber = np.zeros((number_of_users, number_of_bs))

    # calculating the gain, path_loss and interference for every user-bs pair
    for i in users:
        coords_i = f.user_coords(i, x_user, y_user)
        for j in base_stations:
            coords_j = f.bs_coords(j)
            path_loss[i, j] = f.find_path_loss(i, j, coords_i, coords_j)
            gain_bs[i, j] = f.find_gain(coords_j, coords_i, coords_j, coords_i, beamwidth_b)
            gain_user[i, j] = f.find_gain(coords_i, coords_j, coords_i, coords_j, beamwidth_u)
            # SNR[i, j] = transmission_power * gain_bs[i, j] * gain_user[i, j] / (path_loss[i, j] * noise)
            # spectral_efficiency[i, j] = math.log2(1 + SNR[i, j])

            user_beamnumber[i, j] = f.find_beam_number(
                f.find_bore(coords_i, coords_j, beamwidth_u), beamwidth_u)
            bs_beamnumber[i, j] = f.find_beam_number(
                f.find_bore(coords_j, coords_i, beamwidth_b), beamwidth_b)

    # ------------------------ Start of optimization program ------------------------------------
    try:
        m = gp.Model("Model 1")
        # m.setParam('NonConvex', 2)
        m.Params.LogToConsole = 0
        m.Params.OutputFlag = 0
        m.Params.Threads = 3
        m.Params.timeLimit = 10
        m.Params.PoolSearchMode = 2
        m.Params.PoolSolutions = N * 5 + 5

        # -------------- VARIABLES -----------------------------------
        x = {}
        x_user = {}
        C_user = {}
        power = {}
        rate = {}
        SNR = {}
        # active_beam = {}

        disconnected = {}

        for i in users:
            for j in base_stations:
                power[i, j] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=transmission_power * number_of_active_beams,
                                       name=f'p#{i}#{j}')
                x_user[i, j] = m.addVar(vtype=GRB.BINARY, name=f'x_user{i}{j}')
                x[i, j] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1, name=f'x#{i}#{j}')
                rate[i, j] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f'rate_per_bs#{i}#{j}')
                SNR[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'SNR{i}{j}')
            C_user[i] = m.addVar(vtype=GRB.CONTINUOUS, name=f'C_user#{i}')

            disconnected[i] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1, name=f'Disconnected_user#{i}')

        # for j in base_stations:
        #     for d in directions_bs:
        #         active_beam[j, d] = m.addVar(vtype=GRB.BINARY, name=f'active_beam{j}{d}')
        m.update()

        # ----------------- OBJECTIVE ----------------------------------
        m.setObjective(
            quicksum(quicksum(
                x_user[i, j] * power[i, j] * gain_bs[i, j] * gain_user[i, j] / (path_loss[i, j] * noise) for j in
                range(number_of_bs)) for i in users) - M / 2 * quicksum(
                quicksum(power[i, j] for j in base_stations) for i in users),
            GRB.MAXIMIZE)

        # --------------- CONSTRAINTS -----------------------------

        # Only 1 BS per angular direction per user
        for i in users:
            for d in range(len(directions_u)):
                m.addConstr(quicksum(x_user[i, j] for j in base_stations if user_beamnumber[i, j] == d) <= 1,
                            name=f'angle_u#{i}#{d}')

        # the total shares per beam could never exceed the number of users per beam
        # for j in base_stations:
        #     for d in directions_bs:
        #         m.addConstr(
        #             quicksum(x[i, j] for i in users if bs_beamnumber[i, j] == d) <= active_beam[j, d],
        #             name=f'shares_per_beam#{j}#{d}')
        #
        # for j in base_stations:
        #     m.addConstr(quicksum(active_beam[j, d] for d in directions_bs) <= number_of_active_beams,
        #                 f'max_active_beams#{j}')

        # if a user has at least one share, the user is connected to that base station
        eps = 0.0001
        for i in users:
            for j in base_stations:
                # If x > 0, then x_user = 1, otherwise x_user = 0
                m.addConstr(x[i, j] >= 0 + eps - M * (1 - x_user[i, j]), name="bigM_constr1")
                m.addConstr(x[i, j] <= 0 + (1 + eps) * x_user[i, j], name="bigM_constr2")

        # Minimum SNR
        # for i in users:
        #     for j in base_stations:
        #         m.addConstr(x_user[i, j] * SINR_min <= SNR[i, j], name=f'minimum_SNR#{i}#{j}')

        # (C3)
        for i in users:
            m.addConstr(quicksum(x_user[i, j] for j in base_stations) >= 1, name=f'MC_user#{i}')

        # (C4)
        for j in base_stations:
            m.addConstr(quicksum(x_user[i, j] for i in users) >= 1, name=f'MC_BS#{j}')

        # find channel capacity, (C5)
        for i in users:
            m.addConstr(quicksum(
                x_user[i, j] * power[i, j] * gain_bs[i, j] * gain_user[i, j] / (path_loss[i, j] * noise) for j in
                range(number_of_bs)) >= (2 ** (user_rate / (overhead_factor * W)) - 1), f'rate{i}')

        # (C5)
        # for i in users:
        #     m.addConstr(C_user[i] >= user_rate, name=f'rate_req{i}')

        # (C6)
        for j in base_stations:
            m.addConstr(
                quicksum(power[i, j] * x_user[i, j] for i in users) <= transmission_power * number_of_active_beams,
                name=f'power{i}{j}')

        # --------------------- OPTIMIZE MODEL -------------------------
        # m.computeIIS()
        # m.write("IISmodel.lp")

        m.optimize()
        # m.write("model.lp")
        # m.getObjective()
        # print('Objective value: %g' % m.ObjVal)


    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))
        sys.exit()

    feasibles = []
    # if m.status == 2:
    for m.Params.SolutionNumber in np.arange(1, N * 5 + 5, 5):
        X = np.zeros((number_of_users, number_of_bs))
        P = np.zeros((number_of_users, number_of_bs))
        R = np.zeros((number_of_users, number_of_bs))

        for i in users:
            for j in base_stations:
                X[i, j] = x_user[i, j].Xn
                P[i, j] = power[i, j].Xn
                R[i, j] = overhead_factor * W * X[i, j] * math.log2(
                    1 + P[i, j] * gain_bs[i, j] * gain_user[i, j] / (path_loss[i, j] * noise))
        feasibles.append((X, P, R))
        # print('X= ', X)
        # print('P =', P)
        # print('R = ', R)
    return feasibles
