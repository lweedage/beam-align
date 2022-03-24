import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

from parameters import *
import functions as f

colors = {100: 'DeepSkyBlue', 300: 'DarkMagenta', 500:'LightPink', 750:'Orange', 1000:'LimeGreen'}

def find_user_distances(user, x_user, y_user, radius):
    distances = f.find_distance_allbs(user, x_user, y_user)
    user_list = []
    for i in range(len(x_user)):
        if distances[i] <= radius:
            user_list.append(i)
    return user_list

def average(x):
    return sum(x)/max(1, len(x))

delta = 2
x_max, y_max = int(np.ceil(xmax * delta)), int(np.ceil(ymax * delta))
bs_degree = dict()

for number_of_users in [100, 300, 500, 750, 1000]:
    print(number_of_users)
    iteration_min = 0
    iteration_max = iterations[number_of_users]

    name = str('users=' + str(number_of_users) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)) + 'M=' + str(
        M) + 's=' + str(s[0]))

    optimals = pickle.load(open(str('Data/assignment' + name + '.p'), 'rb'))
    xs = pickle.load(open(str('Data/xs' + name + '.p'), 'rb'))
    ys = pickle.load(open(str('Data/ys' + name + '.p'), 'rb'))

    connect_to_bs = np.zeros((number_of_bs, y_max, x_max))
    total_visits = np.zeros((y_max, x_max))

    bs_degree[number_of_users] = []

    neighbors = {i: [] for i in range(24)}

    for iteration in range(iteration_max):
        opt_x = optimals[iteration]
        x_user, y_user = xs[iteration], ys[iteration]
        links_per_user = sum(np.transpose(opt_x))
        links_per_bs = sum(opt_x)
        for deg in links_per_bs:
            bs_degree[number_of_users].append(deg)

        # for bs in range(number_of_bs):
        #     for user in range(number_of_users):
        #         u = f.user_coords(user, x_user, y_user)
        #         if opt_x[user, bs] == 1:
        #             connect_to_bs[bs, int(u[1]*delta), int(u[0]*delta)] += 1
        #             total_visits[int(u[1]*delta), int(u[0]*delta)] += 1
        # for user in range(number_of_users):
        #     u = f.user_coords(user, x_user, y_user)
        #     user_list = find_user_distances(u, x_user, y_user, radius = 5)
        #     neighbors[links_per_user[user]].append(len(user_list))

    x_large = [x * delta for x in x_bs]
    y_large = [y * delta for y in y_bs]

    values = range(0, int(xmax) + 1, 10)
    real_value = range(0, int(xmax)*delta + 1, 10 * delta)

    values_y = range(0, int(ymax) + 1, 10)
    real_value_y = range(0, int(ymax)*delta + 1, 10 * delta)

    # for bs in [5]:
    #     fig, ax = plt.subplots()
    #     plt.imshow(connect_to_bs[bs] / total_visits)
    #     plt.colorbar()
    #     plt.scatter(x_large, y_large, color='white', marker='o')
    #     plt.xticks(real_value, values)
    #     plt.yticks(real_value_y, values_y)
    #     plt.title(f"Connect to BS {bs}")
    #     # plt.savefig(str('Figures/mc_heatmap' + name + '.png'))
    #     plt.show()

    averages = []
    error = []
    # for degree in range(24):
    #     averages.append(average(neighbors[degree]))
    #     error.append(np.std(neighbors[degree]))
    # plt.plot(range(24), averages, label = str(str(number_of_users) + ' users'), color = colors[number_of_users])
    # plt.fill_between(range(24), np.subtract(averages, error), np.add(averages, error), alpha = 0.3, color = colors[number_of_users])
# plt.xlabel('Degree of user')
# plt.ylabel('Average number of neighbors in 5m radius')
# plt.legend()
# plt.show()

fig, ax = plt.subplots()
for number_of_users in [100, 300, 500, 750, 1000]:
    plt.hist(bs_degree[number_of_users], density = True, label = f'{number_of_users} users')
plt.xlabel('Number of users per BS')
plt.legend()
plt.ylim([0, 1])
plt.show()
