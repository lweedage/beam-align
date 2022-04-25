import math
from cycler import cycler
import matplotlib
import numpy as np
import pickle

matplotlib.rcParams['axes.prop_cycle'] = cycler('color', ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed'])
colors =  ['DeepSkyBlue', 'DarkMagenta', 'LightPink', 'Orange', 'LimeGreen', 'OrangeRed', 'grey'] * 10

def initialise_graph_triangular(radius, xDelta, yDelta):
    xbs, ybs = list(), list()
    dy = math.sqrt(3 / 4) * radius
    for i in range(0, int(xDelta / radius) + 1):
        for j in range(0, int(yDelta / dy) + 1):
            if i * radius + 0.5 * (j % 2) * radius < xmax and j * dy < ymax:
                xbs.append(i * radius + 0.5 * (j % 2) * radius)
                ybs.append(j * dy)
    return xbs, ybs



# iterations = {50: 1, 100: 5000, 300: 1667, 500: 1000, 750: 667, 1000: 500}
# iterations = {50: 1, 100: 1000, 300: 334, 500: 200, 750: 133, 1000: 100}
# iterations = {10: 1, 100: 500, 300: 167, 500: 100, 750: 67, 1000: 50}
# iterations = {10: 1, 100: 10, 300: 10, 500: 10, 750: 10, 1000: 10}
iterations = {60: 1, 601: 1, 3007: 1}

Torus = True

pi = math.pi
bs_of_interest = 0
radius = 200  # for triangular grid

xmin, xmax = 0, 800
ymin, ymax = 0, math.sqrt(3 / 4) * 2 * radius * 3

xDelta = xmax - xmin
yDelta = ymax - ymin

users = [int(i / (xDelta / 1000 * yDelta / 1000)) for i in [50, 500, 2500]]
print(users)

x_bs, y_bs = initialise_graph_triangular(radius, xDelta, yDelta)
number_of_bs = len(x_bs)


def find_scenario(scenario):
    if scenario in [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31]:
        beamwidth_deg = 5
    elif scenario in [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32]:
        beamwidth_deg = 10
    else:
        beamwidth_deg = 15

    if scenario in [1, 2, 3, 4, 5, 6]:
        users_per_beam = 1
    elif scenario in [7, 8, 9, 10, 11, 12]:
        users_per_beam = 2
    elif scenario in [13, 14, 15, 16, 17, 18]:
        users_per_beam = 5
    elif scenario in [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]:
        users_per_beam = 10
    elif scenario in [31, 32, 33]:
        users_per_beam = 1000
    else:
        users_per_beam = False

    if scenario in [1, 2, 3, 7, 8, 9, 13, 14, 15, 19, 20, 21, 25, 26, 27, 31, 32, 33]:
        Penalty = True
    else:
        Penalty = False

    if scenario in [25, 26, 27, 28, 29, 30]:
        Clustered = True
    else:
        Clustered = False

    return beamwidth_deg, users_per_beam, Penalty, Clustered

def fairness(x):
    teller = sum(x)**2
    noemer = len(x) * sum([i**2 for i in x])
    return teller/noemer



def get_data(scenario, user_rate, Heuristic = False, SNRHeuristic = False, k = 0, User_Heuristic = False, GreedyHeuristic = False, GreedyRate = False, Iterative = False):
    print('Getting data...')
    beamwidth_deg, users_per_beam, Penalty, Clustered = find_scenario(scenario)
    beamwidth_b = beamwidth_deg

    if Penalty:
        M = 100000  # penalty on having disconnected users
    else:
        M = 0

    mis = dict()
    mis_user = dict()

    sat = dict()
    deg = dict()
    cap = dict()
    fair = dict()
    cap_blocked = dict()
    sat_blocked = dict()
    fair_blocked = dict()


    for number_of_users in users:
        iteration_min = 0
        iteration_max = iterations[number_of_users]

        # print(iteration_max)
        name = str(
            str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(
                M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))

        if Heuristic:
            if User_Heuristic:
                name = str('beamwidth_user_heuristic' + name)
            else:
                name = str('beamwidth_heuristic' + name)
            if Iterative:
                name = str(name + '_Iterative')

        elif SNRHeuristic:
            name = str('SNR_k=' + str(k) + name)

        elif GreedyRate:
            name = str(name + 'GreedyRate')
        elif GreedyHeuristic:
            name = str(name + 'GreedyHeuristic')

        if Clustered:
            name = str(name + '_clustered')

        degrees = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
        satisfaction = pickle.load(open(str('Data/satisfaction' + name + '.p'), 'rb'))
        misalignment_bs = pickle.load(open(str('Data/grid_misalignment_bs' + name + '.p'), 'rb'))
        misalignment_user = pickle.load(open(str('Data/grid_misalignment_user' + name + '.p'), 'rb'))
        capacity = pickle.load(open(str('Data/channel_capacity' + name + '.p'), 'rb'))
        blocked_capacity = pickle.load(open(str('Data/blocked_capacity' + name + '.p'), 'rb' ))
        satisfaction_blocked = pickle.load( open(str('Data/satisfaction_blocked' + name + '.p'), 'rb'))
        capacity_per_user = pickle.load(open(str('Data/channel_capacity_per_user' + name + '.p'), 'rb'))
        capacity_per_user_blocked = pickle.load(open(str('Data/blocked_capacity_per_user' + name + '.p'), 'rb'))


        fair[number_of_users] = fairness(capacity_per_user)
        fair_blocked[number_of_users] = fairness(capacity_per_user_blocked)
        deg[number_of_users] = sum(degrees) / len(degrees)
        mis[number_of_users] = np.std(misalignment_bs) * 2
        # mis_user[number_of_users] = np.degrees(np.std(misalignment_user)*2)
        sat[number_of_users] = np.sum(satisfaction) / (len(satisfaction) * len(satisfaction[0]))
        cap[number_of_users] = np.sum(capacity)/len(capacity)
        cap_blocked[number_of_users] = np.sum(blocked_capacity)/len(blocked_capacity)
        sat_blocked[number_of_users] = np.sum(satisfaction)/len(satisfaction)

    print(mis)
    name = str(str(beamwidth_deg) + str(M) + str(users_per_beam) + str(user_rate))
    if Heuristic:
        if User_Heuristic:
            name = str('beamwidth_user_heuristic' + name)
        else:
            name = str('beamwidth_heuristic' + name)
        if Iterative:
            name = str(name + '_Iterative')

    elif SNRHeuristic:
        name = str('SNR_k=' + str(k) + name)

    elif GreedyRate:
        name = str(name + 'GreedyRate')
    elif GreedyHeuristic:
        name = str(name + 'GreedyHeuristic')

    if Clustered:
        name = str(name + '_clustered')


    pickle.dump(deg, open(str('Data/Processed/deg' + name + '.p'),'wb'), protocol=4)
    pickle.dump(mis, open(str('Data/Processed/mis' + name + '.p'),'wb'), protocol=4)
    pickle.dump(sat, open(str('Data/Processed/sat' + name + '.p'),'wb'), protocol=4)
    pickle.dump(cap, open(str('Data/Processed/cap' + name + '.p'),'wb'), protocol=4)
    pickle.dump(fair, open(str('Data/Processed/fair' + name + '.p'),'wb'), protocol=4)
    pickle.dump(cap_blocked, open(str('Data/Processed/cap_blocked' + name + '.p'),'wb'), protocol=4)
    pickle.dump(sat_blocked, open(str('Data/Processed/sat_blocked' + name + '.p'),'wb'), protocol=4)
    pickle.dump(fair_blocked, open(str('Data/Processed/fair_blocked' + name + '.p'),'wb'), protocol=4)
    print(scenario, mis)

if __name__ == '__main__':
    for scenario in [19, 20, 21]:
        print(f'Scenario {scenario}')
        for k in [0]: #[1, 2, 3, 4, 5]:
            Heuristic = False
            Iterative = False
            SNRHeuristic = False
            User_Heuristic = False
            GreedyRate = False
            GreedyHeuristic = False

            get_data(scenario, Heuristic, SNRHeuristic, k, User_Heuristic, GreedyHeuristic, GreedyRate, Iterative)
