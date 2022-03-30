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

    n_bins = 50
    plt.hist(capacity_per_user, n_bins, density=True, histtype='step',
             cumulative=True, label=f'{number_of_users} users')
plt.legend()
plt.xlabel('Capacity per user (Mbps)')
plt.ylabel('CDF')
plt.savefig('test.png', dpi=300)
# plt.show()
print(' blub')

# name = str(
#     'users=' + str(number_of_users) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)) + 'M=' + str(M) + 's=' + str(
#         users_per_beam))
# optimal = pickle.dump(opt_x, open(str('Data/assignment' + name + '.p'), 'wb'))
