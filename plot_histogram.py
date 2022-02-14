import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

from parameters import *

number_of_users = int(input('Number of users?'))

iteration_min = 0
iteration_max = iterations[number_of_users]

delta = 2

Heuristic = False

start = time.time()
if Heuristic:
    name = str(
        'beamwidth_heuristic' + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(
            np.degrees(beamwidth_b)))
else:
    name = str('users=' + str(number_of_users)  + 'beamwidth_b=' + str(np.degrees(beamwidth_b)))

misalignment_user = pickle.load(open(str('Data/grid_misalignment_user' + name + '.p'), 'rb'))
misalignment_bs = pickle.load(open(str('Data/grid_misalignment_bs' + name + '.p'), 'rb'))
misalignment_mc = pickle.load(open(str('Data/grid_misalignment_mc' + name + '.p'), 'rb'))
misalignment_sc = pickle.load(open(str('Data/grid_misalignment_sc' + name + '.p'), 'rb'))

distances = pickle.load(open(str('Data/distances' + name + '.p'), 'rb'))
distances_mc = pickle.load(open(str('Data/distances_mc' + name + '.p'), 'rb'))
distances_sc = pickle.load(open(str('Data/distances_sc' + name + '.p'), 'rb'))

degrees = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
degrees = [i for i in degrees if i != 0]

disconnected = pickle.load(open(str('Data/disconnected_users' + name + '.p'), 'rb'))

data = misalignment_bs

print('Disconnected users:', np.sum(disconnected)/len(disconnected))
if not (Heuristic):
    no_optimal_value = pickle.load(open(str('Data/no_optimal_value_found' + name + '.p'), 'rb'))
    print('No succes in', no_optimal_value / iterations[number_of_users] * 100, 'percent of the iterations')


fig, ax = plt.subplots()
data = np.degrees(data)
plt.hist(data, density=True, bins=np.arange(min(data), max(data) + 0.1, 0.1), label='simulated')
sigma = np.std(data)
print('STD = ', sigma * 2)
x = np.linspace(-3 * sigma, 3 * sigma, 100)
plt.plot(x, stats.norm.pdf(x, 0, sigma), label=f'N(0, {str(sigma)[:5]})')
plt.xlabel('Misalignment in degrees')
plt.legend()
plt.show()


name = str(int(math.ceil(np.degrees(beamwidth_b)))) + 'b_' + str(number_of_users) + '_users'
if Heuristic:
    name = str('heuristic_' + name)

fig, ax = plt.subplots()
data1 = np.degrees(misalignment_sc)
data2 = np.degrees(misalignment_mc)
print(max(data1), max(data2))
plt.hist(data1, density=True, bins=np.arange(-np.degrees(beamwidth_b / 2), np.degrees(beamwidth_b / 2) + 0.1, 0.1),
         alpha=0.3, label='single connections')
plt.hist(data2, density=True, bins=np.arange(-np.degrees(beamwidth_b / 2), np.degrees(beamwidth_b / 2) + 0.1, 0.1),
         alpha=0.3, label='multiple connections')
plt.xlabel('Misalignment in degrees')
plt.legend()
plt.savefig(str('Figures/' + name + '_misalignment.png'))
plt.show()

fig, ax = plt.subplots()
data = distances
step = 2
# plt.hist(data, density=True, bins = np.arange(min(data), max(data) + step, step), alpha = 0.3, label = 'all distances')
data = distances_sc
plt.hist(data, density=True, bins=np.arange(min(data), 55 + step, step), alpha=0.3, label='single connections')
data = distances_mc
plt.hist(data, density=True, bins=np.arange(min(data), 55 + step, step), alpha=0.3, label='multiple connections')
plt.legend()
plt.xlabel('Link distance (m)')
plt.savefig(str('Figures/' + name + '_distances.png'))
plt.show()

# fig, ax = plt.subplots()
# step = 2
# data = distances_2mc
# plt.hist(data, density=True, bins = np.arange(min(data), 55 + step, step), alpha = 0.3, label = '2mc')
# data = distances_3mc
# plt.hist(data, density=True, bins = np.arange(min(data), 55 + step, step), alpha = 0.3, label = '3mc')
# data = distances_4mc
# plt.hist(data, density=True, bins = np.arange(min(data), 55 + step, step), alpha = 0.3, label = '4mc')
# data = distances_5mc
# plt.hist(data, density=True, bins = np.arange(min(data), 55 + step, step), alpha = 0.3, label = '>5mc')
# plt.xlabel('Link distance (m)')
# plt.legend()
# plt.show()


fig, ax = plt.subplots()
plt.hist(degrees, density=True)
plt.xlabel('Number of connections')
plt.savefig(str('Figures/' + name + '_degrees.png'))
print('Average number of connections:', sum(degrees) / len(degrees))
plt.show()

# print(misalignment_bs)

# fig, ax = plt.subplots()
# plt.scatter(np.degrees(np.abs(misalignment_bs)), distances, s = 0.5, label = 'SC')
# plt.scatter(np.degrees(np.abs(misalignment_mc)), distances_mc, s = 0.5, label = 'MC')
# plt.xlabel('Misalignment')
# plt.ylabel('Distance')
# plt.legend()
# plt.savefig(str('Figures/' + name + '_degrees_scatter.png'))
# plt.show()
