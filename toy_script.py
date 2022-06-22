import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import pickle
import functions as f
import progressbar
# def find_rain(r, rain_rate):
#     k = 0.124
#     alpha = 1.061
#     rain_att = k * rain_rate ** alpha
#     return rain_att * (r / 1000)  # attenuation is in db/km
#
#
# distances = np.arange(1, 400, 1)
# fig, ax = plt.subplots()
# plt.plot(distances, [find_rain(r, 2.5) for r in distances], label='2.5')
# plt.plot(distances, [find_rain(r, 25) for r in distances], label='25')
# plt.plot(distances, [find_rain(r, 150) for r in distances], label='150')
# plt.legend()
# plt.show()
# users = [900]
k = 24

def find_closest(user):
    x = np.minimum((x_bs - user[0]) % xDelta, (user[0] - x_bs) % xDelta)
    y = np.minimum((y_bs - user[1]) % yDelta, (user[1] - y_bs) % yDelta)
    return np.argsort(x ** 2 + y ** 2)[:k]

for number_of_users in users:
    iteration_max = iterations[number_of_users]
    Heuristic = False
    SNRHeuristic = False

    name = find_name(iteration_max, number_of_users, Heuristic, SNRHeuristic, k, Clustered, M, Greedy)

    total_links_per_user = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
    print(f'{number_of_users} users, disconnected users: {len([i for i in total_links_per_user if i == 0])/len(total_links_per_user)}')
