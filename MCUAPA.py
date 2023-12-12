import os
import pickle

import find_feasible_solutions
import functions as f
from parameters import *


def load_file(name):
    if os.path.exists(name):
        return pickle.load(open(str(name), 'rb'))
    else:
        return None


def find_rate(X, P, number_of_users, misc):
    R = np.zeros((number_of_users, number_of_bs))
    for i in range(number_of_users):
        for j in range(number_of_bs):
            R[i, j] = rate(i, j, X, P, misc)
    return R


def objective(X, P, R, number_of_users):
    sum_R = np.sum(X * R)
    sum_P = np.sum(X * P)
    sigma_user = math.sqrt(
        (1 / number_of_users) * np.sum(np.sum(np.subtract(X * R, sum_R / number_of_users), axis=1) ** 2))
    sigma_BS = math.sqrt((1 / number_of_bs) * np.sum(np.sum(np.subtract(X * R, sum_R / number_of_bs), axis=0) ** 2))

    if sigma_user == 0:
        sigma_user = math.inf
    if sigma_BS == 0:
        sigma_BS = math.inf
    if sum_P == 0:
        EE = 0
    else:
        EE = sum_R / sum_P
    return EE, -sigma_user, -sigma_BS


def feasible_solution(X, P, R):
    rate = np.sum(X * R, axis=1)
    # C1 an C2 are satisfied by construction
    C3 = np.all(np.sum(X, axis=0) >= 1)
    C4 = np.all(np.sum(X, axis=1) >= 1)
    C5 = np.all(rate >= user_rate - 1)
    C6 = np.all(np.sum(X * P, axis=0) <= P_max + 1)
    C7 = np.sum(X - X * X) <= 0
    return C3 and C4 and C5 and C6 and C7


def rate(i, j, X, P, misc):
    if np.sum(X[:, j]) == 0:
        return 0
    else:
        return overhead_factor * X[i, j] * W * math.log2(1 + SNR(i, j, P, misc))


def distance(i, j, user_locations, bs_locations):
    xu, yu = user_locations[i]
    xbs, ybs = bs_locations[j]
    return math.sqrt((xu - xbs) ** 2 + (yu - ybs) ** 2)


def SNR(i, j, P, misc):
    gain_bs, gain_user, path_loss = misc
    received_power = P[i, j] * gain_bs[i, j] * gain_user[i, j] / path_loss[i, j]
    WN = noise
    return received_power / WN


def gain(i, j, user_locations, bs_locations):  # THIS IS OVERLY SIMPLIFIED!
    coord_user = user_locations[i]
    coord_bs = bs_locations[j]
    gain_user = f.find_gain(coord_user, coord_bs, coord_user, coord_bs, beamwidth_u)
    gain_bs = f.find_gain(coord_bs, coord_user, coord_bs, coord_user, beamwidth_b)
    return gain_user * gain_bs


def levy(mu, x):
    beta = 1.5
    teller = math.gamma(1 + beta) * math.sin(math.pi * beta / 2)
    noemer = math.gamma(1 / 2 * (1 + beta)) * beta * 2 ** ((beta - 1) / 2)
    sigma = (teller / noemer) ** (1 / beta)
    return 0.01 * (mu * sigma) / abs(x) ** (1 / beta)


def LCSDP_procedure(X, P, C_X, C_P, number_of_users):
    i = np.random.randint(0, number_of_users)
    j = np.random.randint(0, number_of_bs)
    X[i, j] = C_X
    P[i, j] = P_min + C_P * (P_max - P_min)

    return np.clip(X, 0, 1, out=X), np.clip(P, P_min, P_max, out=P)


def dominance(sol1, sol2, number_of_users):
    X1, P1, R1 = sol1
    X2, P2, R2 = sol2

    a1, b1, c1 = objective(X1, P1, R1, number_of_users)
    a2, b2, c2 = objective(X2, P2, R2, number_of_users)

    if a1 >= a2 and b1 >= b2 and c1 >= c2:
        if a1 > a2 or b1 > b2 or c1 > c2:
            return True


def find_next(params, population, number_of_users, misc):
    X, P, R, X_rabbit, P_rabbit, X_m, P_m, t = params

    E0 = np.random.uniform(-1, 1)
    E = 2 * E0 * (1 - t / T_iter)
    [r1], [r2], [r3], [r4], [r5], [q], [r] = np.random.rand(7, 1)
    J = 2 * (1 - r5)

    new_X = None

    if abs(E) >= 1:
        if q >= 0.5:
            X_rand = population[0][np.random.randint(0, N)][0]
            P_rand = population[0][np.random.randint(0, N)][1]
            new_X = X_rand - r1 * abs(X_rand - 2 * r2 * X)
            new_P = P_rand - r1 * abs(P_rand - 2 * r2 * P)

        elif q < 0.5:
            new_X = X_rabbit - X_m - r3 * r4
            new_P = P_rabbit - P_m - r3 * (P_min + r4 * (P_max - P_min))

    elif abs(E) >= 0.5 and r >= 0.5:
        new_X = (X_rabbit - X) - E * abs(J * X_rabbit - X)
        new_P = (P_rabbit - P) - E * abs(J * P_rabbit - P)

    elif abs(E) < 0.5 and r >= 0.5:
        new_X = X_rabbit - E * abs(X_rabbit - X)
        new_P = P_rabbit - E * abs(P_rabbit - P)

    elif abs(E) >= 0.5 and r < 0.5:
        Y_X = np.clip(X_rabbit - E * abs(J * X_rabbit - X), 0, 1)
        Y_P = np.clip(P_rabbit - E * abs(J * P_rabbit - P), P_min, P_max)
        Y_R = find_rate(Y_X, Y_P, number_of_users, misc)
        S_X = np.random.rand(number_of_users, number_of_bs)
        S_P = np.random.rand(number_of_users, number_of_bs) * P_max
        Z_X = np.clip(Y_X + S_X * levy(np.random.rand(1), np.random.rand(1)), 0, 1)
        Z_P = np.clip(Y_P + S_P * levy(np.random.rand(1), np.random.rand(1)), P_min, P_max)
        Z_R = find_rate(Z_X, Z_P, number_of_users, misc)

        if dominance((Y_X, Y_P, Y_R), (X, P, R), number_of_users):
            new_X, new_P, new_R = Y_X, Y_P, Y_R
        elif dominance((Z_X, Z_P, Z_R), (X, P, R), number_of_users):
            new_X, new_P, new_R = Z_X, Z_P, Z_R
        else:
            new_X, new_P, new_R = X, P, R
    elif abs(E) < 0.5 and r < 0.5:
        Y_X = np.clip(X_rabbit - E * abs(J * X_rabbit - X_m), 0, 1)
        Y_P = np.clip(P_rabbit - E * abs(J * P_rabbit - P_m), P_min, P_max)
        Y_R = find_rate(Y_X, Y_P, number_of_users, misc)

        S_X = np.random.rand(number_of_users, number_of_bs)
        S_P = np.random.rand(number_of_users, number_of_bs) * P_max
        Z_X = np.clip(Y_X + S_X * levy(np.random.rand(1), np.random.rand(1)), 0, 1)
        Z_P = np.clip(Y_P + S_P * levy(np.random.rand(1), np.random.rand(1)), P_min, P_max)
        Z_R = find_rate(Z_X, Z_P, number_of_users, misc)

        if dominance((Y_X, Y_P, Y_R), (X, P, R), number_of_users):
            new_X, new_P, new_R = Y_X, Y_P, Y_R
        elif dominance((Z_X, Z_P, Z_R), (X, P, R), number_of_users):
            new_X, new_P, new_R = Z_X, Z_P, Z_R
        else:
            new_X, new_P, new_R = X, P, R

    if new_X is not None:
        np.clip(new_X, 0, 1, out=new_X)
        np.clip(new_P, P_min, P_max, out=new_P)
        new_R = find_rate(X, P, number_of_users, misc)
        return new_X, new_P, new_R
    else:
        return None, None


def find_delta(X, P, R):
    rate = np.sum(X * R, axis=1)
    term1 = max(0, np.sum(np.subtract(1, np.sum(X, axis=0))))
    term2 = max(0, np.sum(np.subtract(1, np.sum(X, axis=1))))
    term3 = max(0, np.sum(np.subtract(user_rate, rate)))
    term4 = max(0, np.sum(np.subtract(X * P, P_max)))
    term5 = max(0, np.sum(X - X * X))
    return term1 + term2 + term3 + term4 + term5


def find_new_candidates(candidates, number_of_users):
    deltas = {(id(X), id(P)): find_delta(X, P, R) for X, P, R in candidates}

    feasible_solutions = [(X, P, R) for X, P, R in candidates if feasible_solution(X, P, R)]
    feasible_objectives = [objective(X, P, R, number_of_users) for X, P, R in feasible_solutions]
    infeasible_solutions = [(X, P, R) for X, P, R in candidates if not feasible_solution(X, P, R)]
    infeasible_deltas = [deltas[(id(X), id(P))] for X, P, R in infeasible_solutions]

    argsort_feasible_solns = sorted(range(len(feasible_objectives)), key=lambda i: feasible_objectives[i], reverse=True)
    argsort_infeasible_solns = np.argsort(infeasible_deltas)

    newXs = [feasible_solutions[i] for i in argsort_feasible_solns]
    for j in argsort_infeasible_solns:
        newXs.append(infeasible_solutions[j])

    return newXs[:N]


N = 100
T_iter = 300
#
P_min = 0
P_max = transmission_power * number_of_active_beams


def do_algorithm(x_user, y_user, iteration):
    number_of_users = len(x_user)
    gain_bs = np.zeros((number_of_users, number_of_bs))
    gain_user = np.zeros((number_of_users, number_of_bs))
    path_loss = np.zeros((number_of_users, number_of_bs))

    for i in range(number_of_users):
        coords_i = f.user_coords(i, x_user, y_user)
        for j in range(number_of_bs):
            coords_j = f.bs_coords(j)
            path_loss[i, j] = f.find_path_loss(i, j, coords_i, coords_j)
            gain_bs[i, j] = f.find_gain(coords_j, coords_i, coords_j, coords_i, beamwidth_b)
            gain_user[i, j] = f.find_gain(coords_i, coords_j, coords_i, coords_j, beamwidth_u)

    misc = (gain_bs, gain_user, path_loss)

    feasibles = load_file(str('Data/feasibles' + str(scenario) + str(iteration) + str(N) + str(number_of_users) + '.p'))
    # feasibles = None
    while feasibles == None or len(feasibles) == 0:
        feasibles = feasible_solutions.optimization(x_user, y_user, N + 1)
        pickle.dump(feasibles,
                    open(str('Data/feasibles' + str(scenario) + str(iteration) + str(N) + str(number_of_users) + '.p'),
                         'wb'), protocol=4)

    population = dict()
    population[0] = feasibles[:-1]
    (X_rabbit, P_rabbit, R_rabbit) = feasibles[-1]
    # print('Feasible solutions have been found')

    # time steps
    [C_X], [C_P] = np.random.rand(2, 1)
    mu_chaos = 3.9  #

    obs1, obs2, obs3 = np.zeros(T_iter), np.zeros(T_iter), np.zeros(T_iter)
    for t in range(T_iter):
        # print('t =', t)
        if t > 0:
            X_rabbit, P_rabbit, R_rabbit = population[t - 1][0]
        C_X = mu_chaos * C_X * (1 - C_X)
        C_P = mu_chaos * C_P * (1 - C_P)

        candidates = []

        X_m = 1 / N * sum([X for X, P, R in population[t]])
        P_m = 1 / N * sum([P for X, P, R in population[t]])
        for X, P, R in population[t]:
            params = [X, P, R, X_rabbit, P_rabbit, X_m, P_m, t]
            new_X, new_P, new_R = find_next(params, population, number_of_users, misc)
            candidates.append((X, P, R))
            if new_X is not None:
                candidates.append((new_X, new_P, new_R))

                if feasible_solution(new_X, new_P, new_R):
                    extra_X, extra_P = LCSDP_procedure(new_X, new_P, C_X, C_P, number_of_users)
                    extra_R = find_rate(extra_X, extra_P, number_of_users, misc)
                    candidates.append((extra_X, extra_P, extra_R))

        KDs = find_new_candidates(candidates, number_of_users)
        population[t + 1] = [(X, P, R) for X, P, R in KDs]

    X, P, R = population[t + 1][0]
    for i in range(number_of_users):
        for j in range(number_of_bs):
            if P[i, j] == 0:
                X[i, j] = 0
    # print('objective:', objective(X, P, R, number_of_users))
    return X, P, np.sum(R, axis=1)
