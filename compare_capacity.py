import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import functions as f
import time
import pickle

max_iterations = 100
delta = 2

if Interference:
    name = str('beamwidth_heuristic_until_iteration_' + str(max_iterations) + 'users='  + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)))
else:
    name = str('beamwidth_heuristic_no_interference_until_iteration_' + str(max_iterations) + 'users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)))

heuristic_capacity = pickle.load(open(str('Data/total_channel_capacity' + name + 'delta=' + str(delta) + '.p'),'rb'))

if Interference:
    name = str('until_iteration_' + str(max_iterations) + 'users='  + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)))
else:
    name = str('no_interference_until_iteration_' + str(max_iterations) + 'users='  + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)))

capacity = pickle.load(open(str('Data/total_channel_capacity' + name + 'delta=' + str(delta) + '.p'),'rb'))

fig, ax = plt.subplots()
plt.hist(capacity, alpha = 0.3, label = 'Optimal', density = True)
plt.hist(heuristic_capacity, alpha = 0.3, label = 'Heuristic', density = True)
plt.legend()
plt.show()

sorted_heuristic_capacity = [heuristic_capacity[i] for i in np.argsort(capacity)]

fig, ax = plt.subplots()
plt.scatter(range(max_iterations), sorted_heuristic_capacity, label = 'Heuristic')
plt.plot(range(max_iterations), sorted(capacity), label = 'Optimal')

plt.legend()
plt.show()

print(capacity)