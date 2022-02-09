import matplotlib.pyplot as plt
import numpy as np
from parameters import *
import new_optimization
import functions as f
import time
import pickle

max_iterations = 1000
delta = 2

bandwidth_sharing = True
SNR = False

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
heuristic_beamwidth_nosharing_capacity = []


SC_closest_heuristic_capacity = []
MC2_closest_heuristic_capacity = []
MC3_closest_heuristic_capacity = []
MC4_closest_heuristic_capacity = []
MC5_closest_heuristic_capacity = []


disconnected_users_heuristic = []
disconnected_users_heuristic_noshare = []

failed_snr_constraints_SC_closest_heuristic = []
failed_snr_constraints_MC2_closest_heuristic = []
failed_snr_constraints_MC3_closest_heuristic = []
failed_snr_constraints_MC4_closest_heuristic = []
failed_snr_constraints_MC5_closest_heuristic = []

user = [100, 300, 500, 750, 1000]

for number_of_users in user:
    max_iterations = iterations[number_of_users]
    name = str('beamwidth_heuristic_user_beamforming_no_interference_until_iteration_' + str(max_iterations) + 'users=' + str(
                number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)))
    name_noshare = str('beamwidth_heuristic_nosharing_no_interference_until_iteration_' + str(max_iterations) + 'users=' + str(
                number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)))

    disconnected_users_heuristic.append(pickle.load(open(str('Data/disconnected_users_iteration_'+ str(max_iterations) + 'beamwidth_heuristic_users='  + str(
            number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
            np.degrees(beamwidth_b)) + '.p'), 'rb')))
    disconnected_users_heuristic_noshare.append(pickle.load(open(str('Data/disconnected_users_iteration_'+ str(max_iterations) + 'beamwidth_heuristic_nosharing_users='  + str(
            number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
            np.degrees(beamwidth_b)) + '.p'), 'rb')))

    heuristic_beamwidth_capacity.append(pickle.load(
        open(str('Data/total_channel_capacity' + name + 'delta=' + str(delta) + '.p'), 'rb')))
    heuristic_beamwidth_nosharing_capacity.append(pickle.load(
        open(str('Data/total_channel_capacity' + name_noshare + 'delta=' + str(delta) + '.p'), 'rb')))


    if not SNR:
        SC_closest_heuristic_capacity.append(pickle.load(
            open(str('Data/total_channel_capacity' + name + 'delta=' + str(delta) + '.p'), 'rb')))

        MC2_closest_heuristic_capacity.append(pickle.load(
            open(str('Data/total_channel_capacity' + 'MC_closest_heuristic_no_interference_until_iteration_' + str(iterations[number_of_users]) + 'k=' + str(2) + 'users=' + str(
                number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)) + 'delta=' + str(delta) +  '.p'), 'rb')))

        MC3_closest_heuristic_capacity.append(pickle.load(
            open(str('Data/total_channel_capacity' + 'MC_closest_heuristic_no_interference_until_iteration_' + str(iterations[number_of_users]) + 'k=' + str(3) + 'users=' + str(
                number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)) + 'delta=' + str(delta) +  '.p'), 'rb')))

        MC4_closest_heuristic_capacity.append(pickle.load(
            open(str('Data/total_channel_capacity' + 'MC_closest_heuristic_no_interference_until_iteration_' + str(iterations[number_of_users]) + 'k=' + str(4) + 'users=' + str(
                number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)) + 'delta=' + str(delta) +  '.p'), 'rb')))


        MC5_closest_heuristic_capacity.append(pickle.load(
            open(str('Data/total_channel_capacity' + 'MC_closest_heuristic_no_interference_until_iteration_' + str(iterations[number_of_users]) + 'k=' + str(5) + 'users=' + str(
                number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
                np.degrees(beamwidth_b)) + 'delta=' + str(delta) +  '.p'), 'rb')))

    # if SNR:
    #     name = str('SNR_closest_heuristic_no_interference_until_iteration_' + str(
    #         iterations[number_of_users]) + 'k=1' + 'users=' + str(
    #         number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
    #         np.degrees(beamwidth_b)))
    #     SC_closest_heuristic_capacity.append(pickle.load(
    #         open(str('Data/total_channel_capacity' + name + 'delta=' + str(delta) + '.p'), 'rb')))
    #
    #     MC2_closest_heuristic_capacity.append(pickle.load(
    #         open(str('Data/total_channel_capacity' + 'SNR_closest_heuristic_no_interference_until_iteration_' + str(
    #             iterations[number_of_users]) + 'k=' + str(2) + 'users=' + str(
    #             number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
    #             np.degrees(beamwidth_b)) + 'delta=' + str(delta) + '.p'), 'rb')))
    #
    #     MC3_closest_heuristic_capacity.append(pickle.load(
    #         open(str('Data/total_channel_capacity' + 'SNR_closest_heuristic_no_interference_until_iteration_' + str(
    #             iterations[number_of_users]) + 'k=' + str(3) + 'users=' + str(
    #             number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
    #             np.degrees(beamwidth_b)) + 'delta=' + str(delta) + '.p'), 'rb')))
    #
    #     MC4_closest_heuristic_capacity.append(pickle.load(
    #         open(str('Data/total_channel_capacity' + 'SNR_closest_heuristic_no_interference_until_iteration_' + str(
    #             iterations[number_of_users]) + 'k=' + str(4) + 'users=' + str(
    #             number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
    #             np.degrees(beamwidth_b)) + 'delta=' + str(delta) + '.p'), 'rb')))
    #
    #     MC5_closest_heuristic_capacity.append(pickle.load(
    #         open(str('Data/total_channel_capacity' + 'SNR_closest_heuristic_no_interference_until_iteration_' + str(
    #             iterations[number_of_users]) + 'k=' + str(5) + 'users=' + str(
    #             number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
    #             np.degrees(beamwidth_b)) + 'delta=' + str(delta) + '.p'), 'rb')))

    name = str('no_interference_until_iteration_' + str(max_iterations) + 'users=' + str(
        number_of_users) + 'beamwidth_u=' + str(np.degrees(beamwidth_u)) + 'beamwidth_b=' + str(
        np.degrees(beamwidth_b)))

    capacity.append(pickle.load(open(str('Data/total_channel_capacity' + name + 'delta=' + str(delta) + '.p'), 'rb')))

y_err = np.zeros((2, len(user)))
y_err_beamwidth_heuristic = np.zeros((2, len(user)))
y_err_SC_closest_heuristic = np.zeros((len(user)))
y_err_MC2_closest_heuristic = np.zeros((len(user)))
y_err_MC3_closest_heuristic = np.zeros((len(user)))
y_err_MC4_closest_heuristic = np.zeros((len(user)))
y_err_MC5_closest_heuristic = np.zeros((len(user)))

for i in range(len(user)):
    y_err[0, i] = min(capacity[i])
    y_err[1, i] = max(capacity[i])
    y_err_beamwidth_heuristic[0, i] = min(heuristic_beamwidth_capacity[i])
    y_err_beamwidth_heuristic[1, i] = max(heuristic_beamwidth_capacity[i])

    # y_err_SC_closest_heuristic[i] = 2 * np.std(SC_closest_heuristic_capacity[i])
    # y_err_MC2_closest_heuristic[i] = 2 * np.std(MC2_closest_heuristic_capacity[i])
    # y_err_MC3_closest_heuristic[i] = 2 * np.std(MC3_closest_heuristic_capacity[i])
    # y_err_MC4_closest_heuristic[i] = 2 * np.std(MC4_closest_heuristic_capacity[i])
    # y_err_MC5_closest_heuristic[i] = 2 * np.std(MC5_closest_heuristic_capacity[i])


# fig, ax = plt.subplots()
# plt.errorbar(user, [sum(capacity[i])/len(capacity[i]) for i in range(len(user))], yerr = y_err)
# plt.errorbar(user, [sum(heuristic_beamwidth_capacity[i])/len(heuristic_beamwidth_capacity[i]) for i in range(len(user))], yerr = y_err_beamwidth_heuristic)
# plt.scatter(user, [sum(capacity[i])/len(capacity[i]) for i in range(len(user))], label = 'Optimal')
# plt.scatter(user, [sum(heuristic_beamwidth_capacity[i])/len(heuristic_beamwidth_capacity[i]) for i in range(len(user))], label = 'Beamwidth heuristic')
# plt.scatter(user, [sum(heuristic_beamwidth_nosharing_capacity[i])/len(heuristic_beamwidth_nosharing_capacity[i]) for i in range(len(user))], label = 'Beamwidth heuristic - no sharing')
#
# plt.xlabel('Number of users')
# plt.ylabel('Total channel capacity (Gbit/s/Hz)')
# plt.legend()
# plt.show()


nonzero_capacity = list([] for i in range(len(user)))
nonzero_heuristic_nosharing = list([] for i in range(len(user)))

for i in range(len(user)):
    nonzero_capacity[i] = [v for v in capacity[i] if v != 0]
    nonzero_heuristic_nosharing[i] = [v for v in heuristic_beamwidth_nosharing_capacity[i] if v != 0]
print(SC_closest_heuristic_capacity)
fig, ax = plt.subplots()
plt.errorbar(user, [sum(nonzero_capacity[i])/max(1, len(nonzero_capacity[i])) for i in range(len(user))], yerr = None)
plt.errorbar(user, [sum(heuristic_beamwidth_capacity[i])/len(heuristic_beamwidth_capacity[i]) for i in range(len(user))], yerr = None)
plt.errorbar(user, [sum(nonzero_heuristic_nosharing[i])/len(nonzero_heuristic_nosharing[i]) for i in range(len(user))], yerr = None)

plt.scatter(user, [sum(nonzero_capacity[i])/max(1, len(nonzero_capacity[i])) for i in range(len(user))], label = 'Optimal')
plt.scatter(user, [sum(heuristic_beamwidth_capacity[i])/len(heuristic_beamwidth_capacity[i]) for i in range(len(user))], label = 'Beamwidth heuristic - sharing')
plt.scatter(user, [sum(nonzero_heuristic_nosharing[i])/len(nonzero_heuristic_nosharing[i]) for i in range(len(user))], label = 'Beamwidth heuristic')
# plt.errorbar(user, [sum(SC_closest_heuristic_capacity[i])/len(SC_closest_heuristic_capacity[i]) for i in range(len(user))], yerr = None, label = 'SNR-1')
# plt.errorbar(user, [sum(MC2_closest_heuristic_capacity[i])/len(MC2_closest_heuristic_capacity[i]) for i in range(len(user))], yerr = None, label = 'Closest-2')
# plt.errorbar(user, [sum(MC3_closest_heuristic_capacity[i])/len(MC3_closest_heuristic_capacity[i]) for i in range(len(user))], yerr = None, label = 'Closest-3')
# plt.errorbar(user, [sum(MC4_closest_heuristic_capacity[i])/len(MC4_closest_heuristic_capacity[i]) for i in range(len(user))], yerr = None, label = 'Closest-4')
# plt.errorbar(user, [sum(MC4_closest_heuristic_capacity[i])/len(MC4_closest_heuristic_capacity[i]) for i in range(len(user))], yerr = None, label = 'Closest-5')

plt.xlabel('Number of users')
plt.ylabel('Total channel capacity (Gbit/s/Hz)')
# plt.title('Only non-zero entries of capacity')
plt.legend()
plt.show()




for i in range(len(user)):
    # print(user[i], 'users:', (1 - (sum(heuristic_beamwidth_capacity[i])/len(heuristic_beamwidth_capacity[i]))/(sum(nonzero_capacity[i])/len(nonzero_capacity[i]))) *100, 'percent difference between optimal')
    print('Average number of disconnected users (beamwidth heuristic):', sum(disconnected_users_heuristic[i])/(len(disconnected_users_heuristic) * user[i]), 'out of', user[i], 'users', 'in', sum([1 for j in range(len(disconnected_users_heuristic[i])) if disconnected_users_heuristic[i][j] > 0])/len(disconnected_users_heuristic[i]) * 100, 'percent of the iterations')

disconnected = [[0.088, 1.368, 4.5892, 9.828666, 13.8018], [11.718, 23.738666, 32.8072, 37.448, 37.9252], [41.13, 50.12, 54.6288, 54.0464, 50.4656]]
fix, ax = plt.subplots()
plt.plot(user, disconnected[0], label = '5 degrees')
plt.plot(user, disconnected[1], label = '10 degrees')
plt.plot(user, disconnected[2], label = '15 degrees')
plt.scatter(user, disconnected[0])
plt.scatter(user, disconnected[1])
plt.scatter(user, disconnected[2])
plt.xlabel('Number of users')
plt.ylabel('Average percentage of disconnected users')
plt.legend()
plt.show()
# for i in range(len(user)):
#     zipje = zip(capacity[i], heuristic_beamwidth_capacity[i])
#     zipje = sorted(zipje, reverse=True)
#     heuristic_capacity = [y for x, y in zipje]
#
#     zipje2 = zip(capacity[i], heuristic_beamwidth_nosharing_capacity[i])
#     zipje2 = sorted(zipje, reverse=True)
#     heuristic_capacity_nosharing = [y for x, y in zipje2]
#
#     fig, ax = plt.subplots()
#     plt.scatter(range(iterations[user[i]]), sorted(capacity[i]), label='Optimal')
#     plt.scatter(range(iterations[user[i]]), heuristic_capacity, label='Heuristic - sharing')
#     plt.scatter(range(iterations[user[i]]), heuristic_capacity_nosharing, label='Heuristic')
#     plt.legend()
#     plt.ylabel('Total capacity (Gbps)')
#     plt.xlabel('Iteration number')
#     plt.show()