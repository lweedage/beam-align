import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import functions as f
import time
import pickle
import scipy.stats as stats

iteration_min = 0

delta = 2

Heuristic = False
degrees = []

for number_of_users in [100, 300, 500, 750]:
    iteration_max = iterations[number_of_users]
    name = str('no_interference_until_iteration_' + str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b))+ 'delta=' + str(delta))

    degrees.append(pickle.load(open(str('Data/total_links_per_user' + name + '.p'),'rb')))

fig, ax = plt.subplots()
plt.boxplot(degrees, showfliers= False)
plt.xticks([1, 2, 3, 4], [100, 300, 500, 750])
plt.xlabel('Number of users')
plt.ylabel('Number of connections')
plt.show()

