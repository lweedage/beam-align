import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from parameters import *
import seaborn as sns
import matplotlib.pylab as pylab
params = {'legend.fontsize': 'large',
         'axes.labelsize': 'large',
         'axes.titlesize':'large',
         'xtick.labelsize':'large',
         'ytick.labelsize':'large',
          'figure.autolayout': True}
pylab.rcParams.update(params)
# colors = sns.color_palette("ch:s=-.2,r=.6")


mis = dict()
dis = dict()
deg = dict()

mis_user = dict()
mis_bs = dict()

for number_of_users in users:
    iteration_min = 0
    iteration_max = iterations[number_of_users]

    Heuristic = False
    SNRHeuristic = True

    k = 3

    name = str(str(iteration_max) + 'users=' + str(number_of_users) + 'beamwidth_b=' + str(beamwidth_b) + 'M=' + str(
        M) + 's=' + str(users_per_beam) + 'rate=' + str(user_rate))

    if Heuristic:
        name = str('beamwidth_heuristic' + name)

    elif SNRHeuristic:
        name = str('SNR_k=' + str(k) + name)

    if Clustered:
        name = str(name + '_clustered')


    misalignment = pickle.load(open(str('Data/grid_misalignment_bs' + name + '.p'), 'rb'))
    satisfaction = pickle.load(open(str('Data/satisfaction' + name + '.p'), 'rb'))
    mis_bs[number_of_users] = np.std(misalignment) * 2
    degrees = pickle.load(open(str('Data/total_links_per_user' + name + '.p'), 'rb'))
    capacity = pickle.load(open(str('Data/capacity_per_user' + name + '.p'), 'rb'))


    name = str(beamwidth_b) + 'b_' + str(number_of_users) + '_users_M=' + str(M) + 's='  + str(users_per_beam)
    if Heuristic:
        name = str('heuristic_' + name)
    if Clustered:
        name = str(name + '_clustered')

    fig, ax = plt.subplots()
    data1 = misalignment
    plt.hist(data1, density=True, bins=np.arange(-(beamwidth_b / 2), (beamwidth_b / 2) + 0.1, 0.1),
             alpha=0.3)
    plt.xlabel('Misalignment in degrees')
    # plt.legend()
    plt.savefig(str('Figures/' + name + '_misalignment.png'), dpi = 300)
    plt.show()


