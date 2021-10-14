import numpy as np
import initialization
import matplotlib.pyplot as plt

seed = 5
simulation_number = 1

penalties1, penalties2, penalties3 = [], [], []
users1, users2, users3, totalusers = [], [], [], []

for simulation_number in [i + 42 for i in [1, 3, 4, 5]]:
    name = 'Simulations/simulation_' + str(simulation_number) + 'seed' + str(seed)
    hexagonal, ppp, number_of_users_1, number_of_users_2, number_of_users_3, OBJECTIVE, number_of_iterations, blub = initialization.initialization(simulation_number)


    if OBJECTIVE == 0:
        obj = 'log'
    elif OBJECTIVE == 1:
        obj = 'sum'
    penalty1 = np.loadtxt(name + 'penalty1' + obj + 'SNR'+ str(2* number_of_iterations - 1) + '.txt')
    penalty2 = np.loadtxt(name + 'penalty2' + obj + 'SNR'+ str(2* number_of_iterations - 1) + '.txt')
    penalty3 = np.loadtxt(name + 'penalty3' + obj + 'SNR'+ str(2* number_of_iterations - 1) + '.txt')

    penalties1.append(1 - sum(penalty1)/len(penalty1))
    penalties2.append(1 - sum(penalty2)/len(penalty2))
    penalties3.append(1 - sum(penalty3)/len(penalty3))

    users1.append(3 * number_of_users_1)
    users2.append(3 * number_of_users_2)
    users3.append(3 * number_of_users_3)
    totalusers.append(number_of_users_1 + number_of_users_2 + number_of_users_3)

fig, ax = plt.subplots()
plt.plot(users1, penalties1, ':', marker = 'o', label = 'Type 1')
plt.plot(users2, penalties2, ':', marker = 'o', label = 'Type 2')
plt.plot(users3, penalties3, ':', marker = 'o', label = 'Type 3')
plt.ylabel('Satisfaction level')
plt.xlabel('Number of users')
plt.ylim([-0.1, 1.1])
plt.legend()
plt.savefig('penalties_simulation_' + str(simulation_number) + obj + 'SNR' + '.png')
plt.show()