import numpy as np
import matplotlib.pyplot as plt

ONE_CONNECTION = False
CLOSEST_CONNECTION = False
PROBABILITY_POLICY = False
THRESHOLD_POLICY = False

# np.random.seed(49)
LOG_CHANNEL = 0
SUM_CHANNEL = 1
MIN_CHANNEL = 2
SOFT_SUM_CHANNEL = 3
UPF = 4

OBJECTIVE = LOG_CHANNEL
SINR = False

number_of_bs = 9
number_of_users = 50

number_of_iterations = 1000

if OBJECTIVE == LOG_CHANNEL:
    obj = 'log'
elif OBJECTIVE == SUM_CHANNEL:
    obj = 'sum'
elif OBJECTIVE == MIN_CHANNEL:
    obj = 'min'

if SINR:
    snr_sinr = 'SINR'
else:
    snr_sinr = 'SNR'

seed = 5
p = 0.2

optimal_log_obj = np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'optimal' + str(number_of_iterations) + 'log_obj.txt')
optimal_sum_obj = np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'optimal' + str(number_of_iterations) + 'sum_obj.txt')

closest_log_obj = np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'closest_connection' + str(number_of_iterations) + 'log_obj.txt')
closest_sum_obj = np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'closest_connection' + str(number_of_iterations) + 'sum_obj.txt')
#
# prob2_log_obj = np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'probability_policy0.2' + str(number_of_iterations) + 'log_obj.txt')
# prob2_sum_obj = np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'probability_policy0.2' + str(number_of_iterations) + 'sum_obj.txt')

prob5_log_obj = np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'probability_policy' + str(p)  + str(number_of_iterations) + 'log_obj.txt')
prob5_sum_obj = np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'probability_policy' + str(p)  + str(number_of_iterations) + 'sum_obj.txt')
#
# prob8_log_obj = np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'probability_policy0.8' + str(number_of_iterations) + 'log_obj.txt')
# prob8_sum_obj = np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'probability_policy0.8' + str(number_of_iterations) + 'sum_obj.txt')

one_connection_log_obj = prob5_log_obj#np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'one_connection' + str(number_of_iterations) + 'log_obj.txt')
one_connection_sum_obj = prob5_sum_obj#np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'one_connection' + str(number_of_iterations) + 'sum_obj.txt')

# probclosest2_log_obj = np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'probability_and_closest_connection0.2' + str(number_of_iterations) + 'log_obj.txt')
# probclosest2_sum_obj = np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'probability_and_closest_connection0.2' + str(number_of_iterations) + 'sum_obj.txt')

probclosest5_log_obj = np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'probability_and_closest_connection' + str(p)  + str(number_of_iterations) + 'log_obj.txt')
probclosest5_sum_obj = np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'probability_and_closest_connection' + str(p)  + str(number_of_iterations) + 'sum_obj.txt')
#
# probclosest8_log_obj = np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'probability_and_closest_connection0.8' + str(number_of_iterations) + 'log_obj.txt')
# probclosest8_sum_obj = np.loadtxt('Simulations/hexagonalbs' + str(number_of_bs) + 'seed' + str(seed) + snr_sinr + obj + 'probability_and_closest_connection0.8' + str(number_of_iterations) + 'sum_obj.txt')

sum_obj = [optimal_sum_obj, closest_sum_obj, one_connection_sum_obj, prob5_sum_obj, probclosest5_sum_obj]
log_obj = [optimal_log_obj, closest_log_obj, one_connection_log_obj, prob5_log_obj, probclosest5_log_obj]

xtickNames = ['optimal', 'closest', '1 connection', 'Optimal-MC-0.5', 'MC-0.5']

if OBJECTIVE == SUM_CHANNEL:
    fig, ax = plt.subplots()
    plt.boxplot(sum_obj)
    plt.xticks([i + 1 for i in range(len(xtickNames))], xtickNames)
    plt.ylabel('Sum $C_{ij}$')
    plt.show()
if OBJECTIVE == LOG_CHANNEL:
    fig, ax = plt.subplots()
    plt.boxplot(log_obj)
    plt.xticks([i + 1 for i in range(len(xtickNames))], xtickNames)
    plt.ylabel('Log $C_{ij}$')
    plt.show()
#
# fig, ax = plt.subplots()
# plt.scatter(range(len(optimal_sum_obj)), optimal_log_obj, label = 'optimal')
# plt.scatter(range(len(optimal_sum_obj)), one_connection_log_obj, label = 'one-connection')
# # plt.xlim([0, 10])
# plt.legend()
# plt.show()

if OBJECTIVE == SUM_CHANNEL:
    print('optimal average:', sum(optimal_sum_obj)/len(optimal_sum_obj))
    print('one connection average:', sum(one_connection_sum_obj)/len(optimal_sum_obj))
    print('closest average:', sum(closest_sum_obj)/len(optimal_sum_obj))
    print('prob average:', sum(prob5_sum_obj)/len(optimal_sum_obj))
    print('prob closest average:', sum(probclosest5_sum_obj)/len(optimal_sum_obj))
if OBJECTIVE == LOG_CHANNEL:
    print('optimal average:', sum(optimal_log_obj)/len(optimal_log_obj))
    print('one connection average:', sum(one_connection_log_obj)/len(optimal_log_obj))
    print('closest average:', sum(closest_log_obj)/len(optimal_log_obj))
    print('prob average:', sum(prob5_log_obj)/len(optimal_log_obj))
    print('prob closest average:', sum(probclosest5_log_obj)/len(optimal_log_obj))