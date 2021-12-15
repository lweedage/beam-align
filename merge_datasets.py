import pickle
import numpy as np

number_of_users = 50
iterations_1 = 1000
iterations_2 = 1000

Interference = True

if Interference:
    grid_1bs_1 = pickle.load(open(str('Data/grid_1bs_until_iteration_' + str(iterations_1) + 'users=' + str(number_of_users) + '.p'),'rb'))
    grid_2mc_1 = pickle.load(open(str('Data/grid_2mc_until_iteration_' + str(iterations_1) + 'users=' + str(number_of_users) + '.p'),'rb'))
    grid_3mc_1 = pickle.load(open(str('Data/grid_3mc_until_iteration_' + str(iterations_1) + 'users=' + str(number_of_users) + '.p'),'rb'))
    grid_4mc_1 = pickle.load(open(str('Data/grid_4mc_until_iteration_' + str(iterations_1) + 'users=' + str(number_of_users) + '.p'),'rb'))
    grid_5mc_1 = pickle.load(open(str('Data/grid_5mc_until_iteration_' + str(iterations_1) + 'users=' + str(number_of_users) + '.p'),'rb'))

    grid_1bs_2 = pickle.load(open(str('Data/grid_1bs_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'),'rb'))
    grid_2mc_2 = pickle.load(open(str('Data/grid_2mc_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'),'rb'))
    grid_3mc_2 = pickle.load(open(str('Data/grid_3mc_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'),'rb'))
    grid_4mc_2 = pickle.load(open(str('Data/grid_4mc_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'),'rb'))
    grid_5mc_2 = pickle.load(open(str('Data/grid_5mc_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'),'rb'))

else:
    grid_1bs_1 = pickle.load(
        open(str('Data/no_interference_grid_1bs_until_iteration_' + str(iterations_1) + 'users=' + str(number_of_users) + '.p'), 'rb'))
    grid_2mc_1 = pickle.load(
        open(str('Data/no_interference_grid_2mc_until_iteration_' + str(iterations_1) + 'users=' + str(number_of_users) + '.p'), 'rb'))
    grid_3mc_1 = pickle.load(
        open(str('Data/no_interference_grid_3mc_until_iteration_' + str(iterations_1) + 'users=' + str(number_of_users) + '.p'), 'rb'))
    grid_4mc_1 = pickle.load(
        open(str('Data/no_interference_grid_4mc_until_iteration_' + str(iterations_1) + 'users=' + str(number_of_users) + '.p'), 'rb'))
    grid_5mc_1 = pickle.load(
        open(str('Data/no_interference_grid_5mc_until_iteration_' + str(iterations_1) + 'users=' + str(number_of_users) + '.p'), 'rb'))

    grid_1bs_2 = pickle.load(
        open(str('Data/no_interference_grid_1bs_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'), 'rb'))
    grid_2mc_2 = pickle.load(
        open(str('Data/no_interference_grid_2mc_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'), 'rb'))
    grid_3mc_2 = pickle.load(
        open(str('Data/no_interference_grid_3mc_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'), 'rb'))
    grid_4mc_2 = pickle.load(
        open(str('Data/no_interference_grid_4mc_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'), 'rb'))
    grid_5mc_2 = pickle.load(
        open(str('Data/no_interference_grid_5mc_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'), 'rb'))

grid_1bs = np.add(grid_1bs_1, grid_1bs_2)//2
grid_2mc = np.add(grid_2mc_1, grid_2mc_2)//2
grid_3mc = np.add(grid_3mc_1, grid_3mc_2)//2
grid_4mc = np.add(grid_4mc_1, grid_4mc_2)//2
grid_5mc = np.add(grid_5mc_1, grid_5mc_2)//2

if Interference:
    pickle.dump(grid_1bs, open(str('Data/grid_1bs_total_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'),'wb'), protocol=4)
    pickle.dump(grid_2mc, open(str('Data/grid_2mc_total_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'),'wb'), protocol=4)
    pickle.dump(grid_3mc, open(str('Data/grid_3mc_total_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'),'wb'), protocol=4)
    pickle.dump(grid_4mc, open(str('Data/grid_4mc_total_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'),'wb'), protocol=4)
    pickle.dump(grid_5mc, open(str('Data/grid_5mc_total_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'),'wb'), protocol=4)
else:
    pickle.dump(grid_1bs, open(
        str('Data/no_interference_grid_1bs_total_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'), 'wb'),
                protocol=4)
    pickle.dump(grid_2mc, open(
        str('Data/no_interference_grid_2mc_total_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'), 'wb'),
                protocol=4)
    pickle.dump(grid_3mc, open(
        str('Data/no_interference_grid_3mc_total_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'), 'wb'),
                protocol=4)
    pickle.dump(grid_4mc, open(
        str('Data/no_interference_grid_4mc_total_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'), 'wb'),
                protocol=4)
    pickle.dump(grid_5mc, open(
        str('Data/no_interference_grid_5mc_total_until_iteration_' + str(iterations_2) + 'users=' + str(number_of_users) + '.p'), 'wb'),
                protocol=4)
