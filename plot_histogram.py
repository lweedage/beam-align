import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import functions as f
import time
import pickle
import scipy.stats as stats

iteration_min = 0
iteration_max = 1000

delta = 2

Heuristic = False

start = time.time()
if Heuristic:
    if Interference:
        name = str('beamwidth_heuristic_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b))+ 'delta=' + str(delta))
    else:
        name = str('beamwidth_heuristic_no_interference_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b))+ 'delta=' + str(delta))
else:
    if Interference:
        name = str('until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b))+ 'delta=' + str(delta))
    else:
        name = str('no_interference_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b))+ 'delta=' + str(delta))

misalignment_user = pickle.load(open(str('Data/grid_misalignment_user' + name + '.p'),'rb'))
misalignment_bs = pickle.load(open(str('Data/grid_misalignment_bs' + name + '.p'),'rb'))
misalignment_mc = pickle.load(open(str('Data/grid_misalignment_mc' + name + '.p'),'rb'))
misalignment_sc = pickle.load(open(str('Data/grid_misalignment_sc' + name + '.p'),'rb'))
misalignment_2mc = pickle.load(open(str('Data/grid_misalignment_2mc' + name + '.p'),'rb'))
misalignment_3mc = pickle.load(open(str('Data/grid_misalignment_3mc' + name + '.p'),'rb'))
misalignment_4mc = pickle.load(open(str('Data/grid_misalignment_4mc' + name + '.p'),'rb'))
misalignment_5mc = pickle.load(open(str('Data/grid_misalignment_5mc' + name + '.p'),'rb'))


data = misalignment_user

fig, ax = plt.subplots()
data = np.degrees(data)
plt.hist(data, density=True, bins = np.arange(min(data), max(data) + 0.1, 0.1), label = 'simulated')
sigma = np.std(data)
print('STD = ', sigma * 2)
x = np.linspace(-3*sigma, 3*sigma, 100)
plt.plot(x, stats.norm.pdf(x, 0, sigma), label = f'N(0, {str(sigma)[:5]})')
plt.xlabel('Misalignment in degrees')
plt.legend()
plt.show()

fig, ax = plt.subplots()
data = np.degrees(misalignment_sc)
plt.hist(data, density=True, bins = np.arange(min(data), max(data) + 0.1, 0.1), label = 'simulated')
sigma = np.std(data)
print(sigma)
x = np.linspace(-3*sigma, 3*sigma, 100)
plt.plot(x, stats.norm.pdf(x, 0, sigma), label = f'N(0, {str(sigma)[:5]})')
plt.xlabel('Misalignment in degrees')
plt.legend()
plt.title('Single connectivity')
plt.show()

fig, ax = plt.subplots()
data1 = np.degrees(misalignment_sc)
data2 = np.degrees(misalignment_mc)
plt.hist(data1, density=True, bins = np.arange(min(data1), max(data1) + 0.1, 0.1), alpha = 0.3, label = 'single connections')
plt.hist(data2, density=True, bins = np.arange(min(data2), max(data2) + 0.1, 0.1), alpha = 0.3, label = 'multiple connections')

plt.xlabel('Misalignment in degrees')
plt.legend()
plt.show()


distances = pickle.load(open(str('Data/distances' + name + '.p'),'rb'))
distances_mc = pickle.load(open(str('Data/distances_mc' + name + '.p'),'rb'))
distances_sc = pickle.load(open(str('Data/distances_sc' + name + '.p'),'rb'))
distances_2mc = pickle.load(open(str('Data/distances_2mc' + name + '.p'),'rb'))
distances_3mc = pickle.load(open(str('Data/distances_3mc' + name + '.p'),'rb'))
distances_4mc = pickle.load(open(str('Data/distances_4mc' + name + '.p'),'rb'))
distances_5mc = pickle.load(open(str('Data/distances_5mc' + name + '.p'),'rb'))

fig, ax = plt.subplots()
data = distances
step = 2
# plt.hist(data, density=True, bins = np.arange(min(data), max(data) + step, step), alpha = 0.3, label = 'all distances')
data = distances_sc
plt.hist(data, density=True, bins = np.arange(min(data), max(data) + step, step), alpha = 0.3, label = 'single connections')
data = distances_mc
plt.hist(data, density=True, bins = np.arange(min(data), max(data) + step, step), alpha = 0.3, label = 'multiple connections')
plt.legend()
plt.xlabel('Link distance (m)')
plt.show()

fig, ax = plt.subplots()
step = 2
data = distances_2mc
plt.hist(data, density=True, bins = np.arange(min(data), max(data) + step, step), alpha = 0.3, label = '2mc')
data = distances_3mc
plt.hist(data, density=True, bins = np.arange(min(data), max(data) + step, step), alpha = 0.3, label = '3mc')
data = distances_4mc
plt.hist(data, density=True, bins = np.arange(min(data), max(data) + step, step), alpha = 0.3, label = '4mc')
data = distances_5mc
plt.hist(data, density=True, bins = np.arange(min(data), max(data) + step, step), alpha = 0.3, label = '>5mc')
plt.xlabel('Link distance (m)')
plt.legend()
plt.show()

fig, ax = plt.subplots()
step = 2
data = distances_sc
plt.hist(data, density=True, bins = np.arange(min(data), max(data) + step, step), alpha = 0.3, label = 'sc')
data = distances_5mc
plt.hist(data, density=True, bins = np.arange(min(data), max(data) + step, step), alpha = 0.3, label = '>5mc')
plt.xlabel('Link distance (m)')
plt.legend()
plt.show()

degrees = pickle.load(open(str('Data/total_links_per_user' + name + '.p'),'rb'))

fig, ax = plt.subplots()
plt.hist(degrees, density = True)
plt.xlabel('Number of connections')
plt.show()

print('Average number of connections:', sum(degrees)/len(degrees))