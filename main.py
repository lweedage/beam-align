import numpy as np
import matplotlib.pyplot as plt
import new_optimization
import functions as f
from parameters import *
import pickle

fig, ax = plt.subplots()

iteration = 0
for number_of_users in [100, 300, 500, 750, 1000]:
    np.random.seed(iteration)
    x_user, y_user = f.find_coordinates(number_of_users)
    opt_x, links, capacity_per_user = new_optimization.optimization(x_user, y_user)

    print('Average connections per user: ', np.sum(opt_x) / number_of_users)
    print('Calculated capacity:', sum(capacity_per_user))



    # f.plot_BSs(x_user, y_user, opt_x)

    n_bins = 50
    plt.hist(capacity_per_user, n_bins, density=True, histtype='step',
                               cumulative=True, label = f'{number_of_users} users')
plt.legend()
plt.xlabel('Capacity per user (Gbps)')
plt.ylabel('CDF')
plt.show()
