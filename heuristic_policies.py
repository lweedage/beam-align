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
import optimization
import os

def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3/4) * radius
    for i in range(0, int(xDelta/radius) + 1):
        for j in range(0, int(yDelta/dy) + 1):
            xbs.append(i*radius + 0.5*(j%2) * radius)
            ybs.append(j*dy)
    return xbs, ybs

SNR_policy = False
SNR_fixed = False
one_connection = False
closest = False
optimal = False

fixed_BW = False
fair_BW = False
fair3_BW = False
optimal_BW = False
noBW = False

T = 10

min_cap_type1 = 2
min_cap_type2 = 20
min_cap_type3 = 100
seed = 5

total_bandwidth = 50

xMin, xMax = 0, 59  # in the case of hexagonal grid
yMin, yMax = 0, 51  # in the case of hexagonal grid

number_of_bs = 16

for simulation_number in [19, 22]:
    hexagonal, ppp, number_of_users_1, number_of_users_2, number_of_users_3, OBJECTIVE, number_of_iterations, penalty_importantness, gamma = initialization.initialization(
        simulation_number)
    for optimal, one_connection in [(True, False), (False, True)]:
        for fair_BW, fixed_BW in [(True, False), (False, True)]: # [(True, False, False), (False, True, False), (False, False, True)]:

            np.random.seed(seed)
            if hexagonal:
                xbs, ybs = initialise_graph_triangular(radius, xMax, yMax)
            elif ppp:
                xbs = np.random.uniform(xMin, xMax, number_of_bs)
                ybs = np.random.uniform(yMin, yMax, number_of_bs)
            number_of_bs = len(xbs)
        
            if SNR_policy:
                gamma = 10
                policy = str('snr' + str(gamma))
            elif SNR_fixed:
                policy = str('snr_fixed' + str(T))
            elif one_connection:
                policy = 'one_connection'
            elif closest:
                policy = 'closest'
            elif optimal:
                policy = 'optimal'

            if fixed_BW:
                bw = 'fixed_BW'
            elif fair_BW:
                bw = 'fair_BW'
            elif fair3_BW:
                bw = 'fair3_BW'
            elif optimal_BW:
                bw = 'optimal_BW'
            elif noBW:
                bw = 'no_BW'
            print(policy, bw)


            if optimal_BW or one_connection or optimal:
                number_of_iterations = 500
            else:
                number_of_iterations = 10000
            LOG_CHANNEL = 0
            SUM_CHANNEL = 1

            radius = 15
            number_of_bs = 16

            max_distance = 2000

            number_of_users = number_of_users_1 + number_of_users_2 + number_of_users_3


            minimum_channel_capacity = np.concatenate((np.ones(number_of_users_1) * min_cap_type1, np.ones(number_of_users_2) * min_cap_type2, np.ones(number_of_users_3) * min_cap_type3), axis=None)
            types = np.concatenate((0 * np.ones(number_of_users_1), 1 * np.ones(number_of_users_2), 2 * np.ones(number_of_users_3)), axis = None)



            objective_values = []
            channel_type1, channel_type2, channel_type3 = [], [], []
            satisfaction_type1, satisfaction_type2, satisfaction_type3 = [], [], []

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

            seed = 5

            if OBJECTIVE == 0:
                obj = 'log'
            elif OBJECTIVE == 1:
                obj = 'sum'

            snr_sinr = 'SNR'


            name = 'Simulations/simulation_' + str(simulation_number) + 'seed' + str(seed)
            # print(name)
            for iteration in range(number_of_iterations):
                print('Iteration', iteration, 'Simulation', simulation_number)
                # if iteration % 100 == 0:
                #     print(iteration)
                np.random.seed(iteration)

                xu = np.random.uniform(xMin, xMax, number_of_users)
                yu = np.random.uniform(yMin, yMax, number_of_users)

                distances = find_distance_matrix(xu, yu, xbs, ybs)
                logSNR = np.log2(1 + c * np.power(distances, -path_loss))

                users = range(number_of_users)
                base_stations = range(number_of_bs)

                # ---------------------- Checking if model is feasible
                if max_distance < max([min(distances[i, :]) for i in users]):
                    print('Maximum user distance is too close')
                    sys.exit()

                # -------------------------- Plotting the solution --------------------------------------
                def find_distance(xu, yu, xbs, ybs):
                    xx = xu - xbs
                    yy = yu - ybs
                    return np.sqrt(xx ** 2 + yy ** 2)

                def find_bs(x, y, xbs, ybs):
                    indices = find_distance(x, y, xbs, ybs).argsort()
                    return indices[:2]

                snr = np.zeros((number_of_users, number_of_bs))
                for i in users:
                    for j in base_stations:
                        snr[i, j] = c * find_distance(xu[i],yu[i], xbs[j], ybs[j])**(-path_loss)

                # The different heuristics:
                # --- USER ASSOCIATION

                filename1 = name + 'alpha' + obj + policy + str(iteration) + '.txt'
                filename2 = name + 'bandwidth' + obj + policy + str(iteration) + '.txt'


                if SNR_policy or closest or SNR_fixed:
                    alpha = np.zeros((number_of_users, number_of_bs))
                    for i in users:
                        x, y = xu[i], yu[i]
                        j, k = find_bs(x, y, xbs, ybs)
                        alpha[i, j] = 1
                        p = np.random.uniform(0, 1)
                        if gamma/snr[i,j] >= p and SNR_policy:
                            alpha[i, k] = 1
                        if snr[i, j] <= T and SNR_fixed:
                            alpha[i, k] = 1


                elif one_connection:
                    if os.path.exists(filename1):
                        alpha = np.loadtxt(filename1)
                        bandwidth_optimal = np.loadtxt(filename2)
                    else:
                        alpha, bandwidth_optimal = optimization.optimization(hexagonal, ppp, number_of_users_1, number_of_users_2, number_of_users_3, OBJECTIVE, penalty_importantness, iteration, one_connection = True)

                elif optimal:
                    if os.path.exists(filename1):
                        alpha = np.loadtxt(filename1)
                        bandwidth_optimal = np.loadtxt(filename2)
                        print('Found this file')
                    else:
                        alpha, bandwidth_optimal = optimization.optimization(hexagonal, ppp, number_of_users_1, number_of_users_2, number_of_users_3, OBJECTIVE, penalty_importantness, iteration, one_connection = False)

                if not noBW:
                    # --- BANDWIDTH
                    channel_capacity = np.zeros((number_of_users, number_of_bs))
                    if fixed_BW:
                        for j in base_stations:
                            degree = sum(alpha[:, j])
                            if degree > 0:
                                bandwidth_per_user = total_bandwidth/degree
                            for i in users:
                                if alpha[i, j] == 1:
                                    channel_capacity[i, j] = bandwidth_per_user * math.log(1 + snr[i, j])
                    elif fair_BW or fair3_BW:
                        for j in base_stations:
                            required_bw = 0
                            required_bw_type3 = 0
                            for i in users:
                                if alpha[i, j] == 1:
                                    required_bw += minimum_channel_capacity[i]/math.log(1 + snr[i, j])
                                    if fair3_BW and minimum_channel_capacity[i] == 100:
                                        required_bw_type3 += minimum_channel_capacity[i]/math.log(1 + snr[i, j])
                            if required_bw > 0 and fair_BW:
                                epsilon = total_bandwidth / required_bw
                                for i in users:
                                    if alpha[i, j] == 1:
                                        channel_capacity[i, j] = minimum_channel_capacity[i] * epsilon
                            elif required_bw > 0 and fair3_BW:
                                print(total_bandwidth, required_bw, required_bw_type3)
                                if required_bw_type3 > 0:
                                    epsilon = (total_bandwidth - (required_bw - required_bw_type3)) / required_bw_type3
                                    print(epsilon)
                                for i in users:
                                    if alpha[i, j] == 1:
                                        if minimum_channel_capacity[i] == 100:
                                            channel_capacity[i, j] = minimum_channel_capacity[i] * epsilon
                                        else:
                                            channel_capacity[i,j] = minimum_channel_capacity[i]


                    elif optimal_BW:
                        if SNR_policy or closest:
                            alpha, bandwidth_optimal = optimization.bandwidth_optimization(hexagonal, ppp, number_of_users_1, number_of_users_2, number_of_users_3, OBJECTIVE, penalty_importantness, iteration, alpha)
                        for i in users:
                            for j in base_stations:
                                channel_capacity[i, j] = bandwidth_optimal[i, j] * math.log(1 + snr[i,j])


                    if obj == 'log':
                        objective = sum([math.log(sum(channel_capacity[i,:])) for i in range(number_of_users)])
                    elif obj == 'sum':
                        objective = sum(sum(channel_capacity))

                    objective_values.append(objective)

                    channel_capacity_per_user = [sum(channel_capacity[i, :]) for i in users]
                    channel_type1.extend(channel_capacity_per_user[0 : number_of_users_1])
                    channel_type2.extend(channel_capacity_per_user[number_of_users_1 : number_of_users_1 + number_of_users_2])
                    channel_type3.extend(channel_capacity_per_user[number_of_users_1 + number_of_users_2 : number_of_users])

                    satisfaction_type1.append(min(np.divide(channel_capacity_per_user[0: number_of_users_1], minimum_channel_capacity[0])))
                    satisfaction_type2.append(min(np.divide(channel_capacity_per_user[number_of_users_1 : number_of_users_1 + number_of_users_2], minimum_channel_capacity[number_of_users_1])))
                    satisfaction_type3.append(min(np.divide(channel_capacity_per_user[number_of_users_1 + number_of_users_2 : number_of_users], minimum_channel_capacity[number_of_users - 1])))

                np.savetxt(name + 'alpha' + obj + policy + str(iteration) + '.txt', alpha)
                np.savetxt(name + 'bandwidth' + obj + policy + str(iteration) + '.txt', alpha)

            if not noBW:
                np.savetxt(name + 'channel_type1' + obj + policy + bw + str(iteration) + '.txt', channel_type1)
                np.savetxt(name + 'channel_type2' + obj + policy + bw + str(iteration) + '.txt', channel_type2)
                np.savetxt(name + 'channel_type3' + obj + policy + bw + str(iteration) + '.txt', channel_type3)

                np.savetxt(name + 'satisfaction_type1' + obj + policy + bw + str(iteration) + '.txt', satisfaction_type1)
                np.savetxt(name + 'satisfaction_type2' + obj + policy + bw + str(iteration) + '.txt', satisfaction_type2)
                np.savetxt(name + 'satisfaction_type3' + obj + policy + bw + str(iteration) + '.txt', satisfaction_type3)

                np.savetxt(name + 'objectives' + obj + policy + bw + str(iteration) + '.txt', objective_values)
