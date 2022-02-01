import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import functions as f
import time
import pickle

max_iterations = 1000
delta = 2


# name = str('beamwidth_heuristic_no_interference_until_iteration_' + str(max_iterations) + 'users=' + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)))
#
# heuristic_capacity = pickle.load(open(str('Data/total_channel_capacity' + name + 'delta=' + str(delta) + '.p'),'rb'))
#
# if Interference:
#     name = str('until_iteration_' + str(max_iterations) + 'users='  + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)))
# else:
#     name = str('no_interference_until_iteration_' + str(max_iterations) + 'users='  + str(number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)))
#
# capacity = pickle.load(open(str('Data/total_channel_capacity' + name + 'delta=' + str(delta) + '.p'),'rb'))
#
# fig, ax = plt.subplots()
# plt.hist(capacity, alpha = 0.3, label = 'Optimal', density = True)
# plt.hist(heuristic_capacity, alpha = 0.3, label = 'Heuristic', density = True)
# plt.legend()
# plt.show()
#
# fig, ax = plt.subplots()
# plt.scatter(range(max_iterations), sorted_heuristic_capacity, label = 'Heuristic', marker = '+', color = color_list)
# plt.plot(range(max_iterations), sorted(capacity), label = 'Optimal', color = 'red')
# # plt.scatter(range(max_iterations), sorted_disconnected, label = '#disconnected users')
# plt.legend()
# plt.show()
#
# difference = np.array(capacity) - np.array(heuristic_capacity)
# fig, ax = plt.subplots()
# plt.hist(difference)
# plt.title('Difference between optimal total capacity and heuristic total capacity')
# plt.show()

capacity = []
heuristic_beamwidth_capacity = []
SC_closest_heuristic_capacity = []
MC2_closest_heuristic_capacity = []
MC3_closest_heuristic_capacity = []
MC4_closest_heuristic_capacity = []
MC5_closest_heuristic_capacity = []


disconnected_users_heuristic = []

failed_snr_constraints_SC_closest_heuristic = []
failed_snr_constraints_MC2_closest_heuristic = []
failed_snr_constraints_MC3_closest_heuristic = []
failed_snr_constraints_MC4_closest_heuristic = []
failed_snr_constraints_MC5_closest_heuristic = []

user = [100, 300, 500, 750, 1000]

for number_of_users in user:
    max_iterations = iterations[number_of_users]

    name = str('beamwidth_heuristic_no_interference_until_iteration_' + str(max_iterations) + 'users=' + str(
            number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
            np.degrees(beamwidth_b)))

    disconnected_users_heuristic.append(pickle.load(open(str('Data/disconnected_users_iteration_'+ str(max_iterations) + 'beamwidth_heuristic_users='  + str(
            number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
            np.degrees(beamwidth_b)) + '.p'), 'rb')))


    heuristic_beamwidth_capacity.append(pickle.load(
        open(str('Data/total_channel_capacity' + name + 'delta=' + str(delta) + '.p'), 'rb')))

    # name = str('SC_closest_heuristic_no_interference_until_iteration_' + str(iterations[number_of_users]) + 'users=' + str(
    #         number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
    #         np.degrees(beamwidth_b)))
    #
    # failed_snr_constraints_SC_closest_heuristic.append(pickle.load(open(str('Data/failed_sinr_constraints_iteration_5000SC_closest_heuristic_users='  + str(
    #         number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
    #         np.degrees(beamwidth_b)) + '.p'), 'rb')))

    # SC_closest_heuristic_capacity.append(pickle.load(
    #     open(str('Data/total_channel_capacity' + name + 'delta=' + str(delta) + '.p'), 'rb')))
    #
    # MC2_closest_heuristic_capacity.append(pickle.load(
    #     open(str('Data/total_channel_capacity' + 'MC_closest_heuristic_no_interference_until_iteration_' + str(iterations[number_of_users]) + 'k=' + str(2) + 'users=' + str(
    #         number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
    #         np.degrees(beamwidth_b)) + 'delta=' + str(delta) +  '.p'), 'rb')))
    #
    # failed_snr_constraints_MC2_closest_heuristic.append(pickle.load(open(str('Data/failed_sinr_constraints_iteration_5000MC_closest_heuristic_k=' + str(2) + 'users='  + str(
    #         number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
    #         np.degrees(beamwidth_b)) + '.p'), 'rb')))
    #
    # MC3_closest_heuristic_capacity.append(pickle.load(
    #     open(str('Data/total_channel_capacity' + 'MC_closest_heuristic_no_interference_until_iteration_' + str(iterations[number_of_users]) + 'k=' + str(3) + 'users=' + str(
    #         number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
    #         np.degrees(beamwidth_b)) + 'delta=' + str(delta) +  '.p'), 'rb')))
    #
    # failed_snr_constraints_MC3_closest_heuristic.append(pickle.load(open(str('Data/failed_sinr_constraints_iteration_5000MC_closest_heuristic_k=' + str(3) + 'users='  + str(
    #         number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
    #         np.degrees(beamwidth_b)) + '.p'), 'rb')))
    #
    # MC4_closest_heuristic_capacity.append(pickle.load(
    #     open(str('Data/total_channel_capacity' + 'MC_closest_heuristic_no_interference_until_iteration_' + str(iterations[number_of_users]) + 'k=' + str(4) + 'users=' + str(
    #         number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
    #         np.degrees(beamwidth_b)) + 'delta=' + str(delta) +  '.p'), 'rb')))
    #
    # failed_snr_constraints_MC4_closest_heuristic.append(pickle.load(open(str('Data/failed_sinr_constraints_iteration_5000MC_closest_heuristic_k=' + str(4) + 'users='  + str(
    #         number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
    #         np.degrees(beamwidth_b)) + '.p'), 'rb')))
    #
    # MC5_closest_heuristic_capacity.append(pickle.load(
    #     open(str('Data/total_channel_capacity' + 'MC_closest_heuristic_no_interference_until_iteration_' + str(iterations[number_of_users]) + 'k=' + str(5) + 'users=' + str(
    #         number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
    #         np.degrees(beamwidth_b)) + 'delta=' + str(delta) +  '.p'), 'rb')))
    #
    # failed_snr_constraints_MC5_closest_heuristic.append(pickle.load(open(str('Data/failed_sinr_constraints_iteration_5000MC_closest_heuristic_k=' + str(5) + 'users='  + str(
    #         number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
    #         np.degrees(beamwidth_b)) + '.p'), 'rb')))


    name = str('no_interference_until_iteration_' + str(max_iterations) + 'users=' + str(
        number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
        np.degrees(beamwidth_b)))

    capacity.append(pickle.load(open(str('Data/total_channel_capacity' + name + 'delta=' + str(delta) + '.p'), 'rb')))



y_err = np.zeros((len(user)))
y_err_beamwidth_heuristic = np.zeros((len(user)))
y_err_SC_closest_heuristic = np.zeros((len(user)))
y_err_MC2_closest_heuristic = np.zeros((len(user)))
y_err_MC3_closest_heuristic = np.zeros((len(user)))
y_err_MC4_closest_heuristic = np.zeros((len(user)))
y_err_MC5_closest_heuristic = np.zeros((len(user)))

for i in range(len(user)):
    y_err[i] = 2 * np.std(capacity[i])
    y_err_beamwidth_heuristic[i] = 2 * np.std(heuristic_beamwidth_capacity[i])
    # y_err_SC_closest_heuristic[i] = 2 * np.std(SC_closest_heuristic_capacity[i])
    # y_err_MC2_closest_heuristic[i] = 2 * np.std(MC2_closest_heuristic_capacity[i])
    # y_err_MC3_closest_heuristic[i] = 2 * np.std(MC3_closest_heuristic_capacity[i])
    # y_err_MC4_closest_heuristic[i] = 2 * np.std(MC4_closest_heuristic_capacity[i])
    # y_err_MC5_closest_heuristic[i] = 2 * np.std(MC5_closest_heuristic_capacity[i])


fig, ax = plt.subplots()
plt.errorbar(user, [sum(capacity[i])/len(capacity[i]) for i in range(len(user))], yerr = y_err, label = 'Optimal')
plt.errorbar(user, [sum(heuristic_beamwidth_capacity[i])/len(heuristic_beamwidth_capacity[i]) for i in range(len(user))], yerr = y_err_beamwidth_heuristic, label = 'Beamwidth heuristic')
# plt.errorbar(user, [sum(SC_closest_heuristic_capacity[i])/len(SC_closest_heuristic_capacity[i]) for i in range(len(user))], yerr = y_err_SC_closest_heuristic, label = 'SC - closest')
# plt.errorbar(user, [sum(MC2_closest_heuristic_capacity[i])/len(MC2_closest_heuristic_capacity[i]) for i in range(len(user))], yerr = y_err_MC2_closest_heuristic, label = 'MC2 - closest')
# plt.errorbar(user, [sum(MC3_closest_heuristic_capacity[i])/len(MC3_closest_heuristic_capacity[i]) for i in range(len(user))], yerr = y_err_MC3_closest_heuristic, label = 'MC3 - closest')
# plt.errorbar(user, [sum(MC4_closest_heuristic_capacity[i])/len(MC4_closest_heuristic_capacity[i]) for i in range(len(user))], yerr = y_err_MC4_closest_heuristic, label = 'MC4 - closest')
# plt.errorbar(user, [sum(MC4_closest_heuristic_capacity[i])/len(MC4_closest_heuristic_capacity[i]) for i in range(len(user))], yerr = y_err_MC4_closest_heuristic, label = 'MC5 - closest')

plt.xlabel('Number of users')
plt.ylabel('Total channel capacity (Gbit/s/Hz)')
plt.legend()
plt.show()

for i in range(len(user)):
    print(user[i], 'users:', (1 - (sum(heuristic_beamwidth_capacity[i])/len(heuristic_beamwidth_capacity[i]))/(sum(capacity[i])/len(capacity[i]))) *100, 'percent difference between optimal')
    print('Average number of disconnected users (beamwidth heuristic):', sum(disconnected_users_heuristic[i])/(len(disconnected_users_heuristic) * user[i]), 'out of', user[i], 'users', 'in', sum([1 for j in range(len(disconnected_users_heuristic[i])) if disconnected_users_heuristic[i][j] > 0])/len(disconnected_users_heuristic[i]) * 100, 'percent of the iterations')
    # print('Failed link constraints:', sum([1 for j in range(len(failed_snr_constraints_beamwidth_heuristic[i])) if failed_snr_constraints_beamwidth_heuristic[i][j] > 0])/len(failed_snr_constraints_beamwidth_heuristic[i])*100, 'percent of the iterations')

    # print('Failed link constraints:', sum([1 for j in range(len(failed_snr_constraints_SC_closest_heuristic[i])) if
    #                                        failed_snr_constraints_SC_closest_heuristic[i][j] > 0]) / len(
    #     failed_snr_constraints_SC_closest_heuristic[i]) * 100, 'percent of the iterations')


fig, ax = plt.subplots()
plt.plot(user, [np.count_nonzero(disconnected_users_heuristic[i])/len(disconnected_users_heuristic[i])*100 for i in range(len(user))], label = 'Beamwidth - disconnected', marker = 'o')

# plt.plot(user, [np.count_nonzero(failed_snr_constraints_SC_closest_heuristic[i])/len(failed_snr_constraints_SC_closest_heuristic[i])*100 for i in range(len(user))], label = 'SC - closest', marker = 'o')
# plt.plot(user, [np.count_nonzero(failed_snr_constraints_MC2_closest_heuristic[i])/len(failed_snr_constraints_MC2_closest_heuristic[i])*100 for i in range(len(user))], label = 'MC2 - closest', marker = 'o')
# plt.plot(user, [np.count_nonzero(failed_snr_constraints_MC3_closest_heuristic[i])/len(failed_snr_constraints_MC3_closest_heuristic[i])*100 for i in range(len(user))], label = 'MC3 - closest', marker = 'o')
# plt.plot(user, [np.count_nonzero(failed_snr_constraints_MC4_closest_heuristic[i])/len(failed_snr_constraints_MC4_closest_heuristic[i])*100 for i in range(len(user))], label = 'MC4 - closest', marker = 'o')
# plt.plot(user, [np.count_nonzero(failed_snr_constraints_MC5_closest_heuristic[i])/len(failed_snr_constraints_MC5_closest_heuristic[i])*100 for i in range(len(user))], label = 'MC5 - closest', marker = 'o')
plt.xlabel('Number of users')
plt.ylabel('% of iterations with disconnected users')
plt.legend()
plt.show()


fig, ax = plt.subplots()
plt.scatter(range(iterations[100]), capacity[0] , label = 'Optimal')
plt.scatter(range(iterations[100]), heuristic_beamwidth_capacity[0], label = 'Heuristic')
plt.legend()
plt.ylabel('Total capacity (Gbps)')
plt.xlabel('Iteration number')
plt.show()