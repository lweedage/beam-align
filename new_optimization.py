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


def optimization(x_user, y_user):
    number_of_users = len(x_user)
    users = range(number_of_users)
    base_stations = range(number_of_bs)

    gain_bs = np.zeros((number_of_users, number_of_bs))
    gain_user = np.zeros((number_of_users, number_of_bs))
    SNR = np.zeros((number_of_users, number_of_bs))

    path_loss = np.zeros((number_of_users, number_of_bs))
    spectral_efficiency = np.zeros((number_of_users, number_of_bs))

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
            SNR[i, j] = transmission_power * gain_bs[i, j] * gain_user[i, j] / (path_loss[i, j] * noise)
            spectral_efficiency[i, j] = math.log2(1 + SNR[i, j])

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
        m.Params.Threads = 4
        m.Params.timeLimit = 300


        # -------------- VARIABLES -----------------------------------
        x = {}
        x_user = {}
        C_user = {}
        active_beam = {}

        disconnected = {}

        for i in users:
            for j in base_stations:
                x_user[i, j] = m.addVar(vtype=GRB.BINARY, name=f'x_user{i}{j}')
                x[i, j] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1, name=f'x#{i}#{j}')
            C_user[i] = m.addVar(vtype=GRB.CONTINUOUS, name=f'C_user#{i}')
            disconnected[i] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1, name=f'Disconnected_user#{i}')

        for j in base_stations:
            for d in directions_bs:
                active_beam[j, d] = m.addVar(vtype=GRB.BINARY, name=f'active_beam{j}{d}')
        m.update()

        # ----------------- OBJECTIVE ----------------------------------
        m.setObjective(quicksum(C_user[i] for i in users) - M * quicksum(disconnected[i] for i in users), GRB.MAXIMIZE)

        # --------------- CONSTRAINTS -----------------------------

        # Only 1 BS per angular direction per user
        for i in users:
            for d in range(len(directions_u)):
                m.addConstr(quicksum(x_user[i, j] for j in base_stations if user_beamnumber[i, j] == d) <= 1,
                            name=f'angle_u#{i}#{d}')

        # the total shares per beam could never exceed the number of users per beam
        for j in base_stations:
            for d in directions_bs:
                m.addConstr(
                    quicksum(x[i, j] for i in users if bs_beamnumber[i, j] == d) <= active_beam[j, d],
                    name=f'shares_per_beam#{j}#{d}')

        for j in base_stations:
            m.addConstr(quicksum(active_beam[j, d] for d in directions_bs) <= number_of_active_beams,
                        f'max_active_beams#{j}')

        # if a user has at least one share, the user is connected to that base station
        eps = 0.0001
        for i in users:
            for j in base_stations:
                # If x > 0, then x_user = 1, otherwise x_user = 0
                m.addConstr(x[i, j] >= 0 + eps - M * (1 - x_user[i, j]), name="bigM_constr1")
                m.addConstr(x[i, j] <= 0 + (1 + eps) * x_user[i, j], name="bigM_constr2")

        # Minimum SNR
        for i in users:
            for j in base_stations:
                m.addConstr(x_user[i, j] * SINR_min <= SNR[i, j], name=f'minimum_SNR#{i}#{j}')

        # Multi-connectivity constraint
        for i in users:
            m.addConstr(quicksum(x_user[i, j] for j in base_stations) <= max_connections, name=f'MC_user#{i}')

        # find channel capacity
        for i in users:
            m.addConstr(C_user[i] == quicksum(
                W * x[i, j] * spectral_efficiency[i, j] for j in base_stations), f'C_user#{i}')

        # rate requirement
        for i in users:
            m.addConstr(C_user[i] >= user_rate * (1 - disconnected[i]), name=f'rate_req{i}')

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

    a = np.zeros((number_of_users, number_of_bs))
    links = np.zeros((number_of_users, number_of_bs))
    total_C = np.zeros(number_of_users)
    satisfied = np.zeros(number_of_users)

    if m.status == 2:
        for i in users:
            total_C[i] = overhead_factor * C_user[i].X
            for j in base_stations:
                a[i, j] = x_user[i, j].X

        for i in users:
            satisfied[i] = min(1, C_user[i].X / user_rate)
            # print(disconnected[i].X)
            for j in base_stations:
                links[i, j] = x[i, j].X

        # for j in base_stations:
        #     for d in directions_bs:
        #         print('bs', j, 'direction', d, [links[i, j] for i in users if bs_beamnumber[i, j] == d])
        # print(links)

    return a, links, total_C, satisfied


def optimization_SINR(x_user, y_user):
    number_of_users = len(x_user)
    users = range(number_of_users)
    base_stations = range(number_of_bs)

    gain_bs = np.zeros((number_of_users, number_of_bs))
    gain_user = np.zeros((number_of_users, number_of_bs))

    path_loss = np.zeros((number_of_users, number_of_bs))
    half_interf = np.zeros((number_of_users, number_of_bs))

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
            user_beamnumber[i, j] = f.find_beam_number(
                f.find_bore(coords_i, coords_j, beamwidth_u), beamwidth_u)
            bs_beamnumber[i, j] = f.find_beam_number(
                f.find_bore(coords_j, coords_i, beamwidth_b), beamwidth_b)
    for i in users:
        for j in base_stations:
            half_interf[i, j] = transmission_power * gain_bs[i, j] * gain_user[i, j] / path_loss[i, j]

            # ------------------------ Start of optimization program ------------------------------------
    try:
        m = gp.Model("Model 1")
        m.setParam('NonConvex', 2)
        # m.Params.LogToConsole = 0
        # m.Params.OutputFlag = 0
        # m.Params.Threads = 3

        # -------------- VARIABLES -----------------------------------
        x = {}
        x_user = {}
        interference = {}
        inverse_interference = {}
        oneSINR = {}
        spectral_efficiency = {}

        C_user = {}
        active_beam = {}
        SINR = {}

        disconnected = {}

        for i in users:
            for j in base_stations:
                SINR[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'SNR#{i}#{j}')
                oneSINR[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'oneSNR#{i}#{j}')
                x_user[i, j] = m.addVar(vtype=GRB.BINARY, name=f'x_user{i}{j}')
                x[i, j] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1, name=f'x#{i}#{j}')
                interference[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'interference#{i}#{j}')
                inverse_interference[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'inv_interference#{i}#{j}')
                spectral_efficiency[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'spectral_efficiency#{i}#{j}')
            C_user[i] = m.addVar(vtype=GRB.CONTINUOUS, name=f'C_user#{i}')
            disconnected[i] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1, name=f'Disconnected_user#{i}')

        for j in base_stations:
            for d in directions_bs:
                active_beam[j, d] = m.addVar(vtype=GRB.BINARY, name=f'active_beam{j}{d}')
        m.update()

        # ----------------- OBJECTIVE ----------------------------------
        m.setObjective(quicksum(C_user[i] for i in users) - M * quicksum(disconnected[i] for i in users), GRB.MAXIMIZE)

        # --------------- CONSTRAINTS -----------------------------

        # Only 1 BS per angular direction per user
        for i in users:
            for d in range(len(directions_u)):
                m.addConstr(quicksum(x_user[i, j] for j in base_stations if user_beamnumber[i, j] == d) <= 1,
                            name=f'angle_u#{i}#{d}')

        # the total shares per beam could never exceed the number of users per beam
        for j in base_stations:
            for d in directions_bs:
                m.addConstr(
                    quicksum(x[i, j] for i in users if bs_beamnumber[i, j] == d) <= active_beam[j, d],
                    name=f'shares_per_beam#{j}#{d}')

        for j in base_stations:
            m.addConstr(quicksum(active_beam[j, d] for d in directions_bs) <= number_of_active_beams,
                        f'max_active_beams#{j}')

        # if a user has at least one share, the user is connected to that base station
        eps = 0.0001
        for i in users:
            for j in base_stations:
                # If x > 0, then x_user = 1, otherwise x_user = 0
                m.addConstr(x[i, j] >= 0 + eps - M * (1 - x_user[i, j]), name="bigM_constr1")
                m.addConstr(x[i, j] <= 0 + (1 + eps) * x_user[i, j], name="bigM_constr2")

        # Minimum SINR
        for i in users:
            for j in base_stations:
                m.addConstr(x_user[i, j] * SINR_min <= SINR[i, j], name=f'minimum_SNR#{i}#{j}')
                m.addConstr(SINR[i, j] == half_interf[i, j] * inverse_interference[i, j], f'definition_SNR#{i}#{j}')
                m.addConstr(interference[i, j] == noise + quicksum(
                    half_interf[i, k] * active_beam[k, bs_beamnumber[i, k]] for k in base_stations if
                    f.find_distance((x_bs[j], y_bs[j]), (x_bs[k], y_bs[k])) > radius), f'interference#{i}#{j}')
                m.addGenConstrPow(interference[i, j], inverse_interference[i, j], -1, f'inverse_constr#{i}#{j}')
                m.addConstr(1 + SINR[i, j] == oneSINR[i, j], f'oneSINR${i}${j}')

        # Multi-connectivity constraint
        for i in users:
            m.addConstr(quicksum(x_user[i, j] for j in base_stations) <= max_connections, name=f'MC_user#{i}')

        for i in users:
            for j in base_stations:
                m.addGenConstrLogA(oneSINR[i, j], spectral_efficiency[i, j], 2, f'logSNR#{i}#{j}')

        # find channel capacity
        for i in users:
            m.addConstr(C_user[i] == quicksum(
                (W / users_per_beam) * x[i, j] * spectral_efficiency[i, j] for j in base_stations), f'C_user#{i}')

        # rate requirement
        for i in users:
            m.addConstr(C_user[i] >= user_rate * (1 - disconnected[i]), name=f'rate_req{i}')

        # --------------------- OPTIMIZE MODEL -------------------------
        # m.computeIIS()
        # m.write("IISmodel.lp")

        m.optimize()
        m.write("model.lp")
        m.getObjective()
        # print('Objective value: %g' % m.ObjVal)


    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))
        sys.exit()

    a = np.zeros((number_of_users, number_of_bs))
    links = np.zeros((number_of_users, number_of_bs))
    total_C = np.zeros(number_of_users)
    satisfied = np.zeros(number_of_users)

    if m.status == 2:
        for i in users:
            total_C[i] = overhead_factor * C_user[i].X
            for j in base_stations:
                a[i, j] = x_user[i, j].X

        for i in users:
            satisfied[i] = min(1, C_user[i].X / user_rate)
            # print(disconnected[i].X)
            for j in base_stations:
                links[i, j] = x[i, j].X
                # print(interference[i, j].X)

        # for j in base_stations:
        #     for d in directions_bs:
        #         print('bs', j, 'direction', d, [links[i, j] for i in users if bs_beamnumber[i, j] == d])
        print('links = ', links)

    return a, links, total_C, satisfied
