import numpy as np
import matplotlib.pyplot as plt
import new_optimization
import functions as f
from parameters import *
import pickle

fig, ax = plt.subplots()

iteration = 0
for number_of_users in [1000]:
    np.random.seed(iteration)
    x_user, y_user = f.find_coordinates(number_of_users)
    print(x_user[990], y_user[990])
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
plt.show()

disconnected = []
for user in range(number_of_users):
    if sum(opt_x[user]) == 0:
        disconnected.append(user)
print(disconnected)


f.plot_BSs(x_user, y_user, links, users_per_beam)
# name = str(
#     'users=' + str(number_of_users) + 'beamwidth_b=' + str(np.degrees(beamwidth_b)) + 'M=' + str(M) + 's=' + str(
#         users_per_beam))
# optimal = pickle.dump(opt_x, open(str('Data/assignment' + name + '.p'), 'wb'))


dis2 = [6, 9, 11, 13, 17, 23, 26, 27, 34, 36, 38, 43, 53, 56, 61, 63, 64, 67, 68, 69, 71, 72, 78, 79, 83, 85, 86, 93, 94, 103, 104, 110, 113, 114, 116, 118, 127, 128, 131, 132, 138, 146, 150, 155, 162, 168, 174, 176, 180, 181, 184, 186, 196, 198, 199, 201, 205, 208, 211, 214, 219, 222, 227, 228, 231, 238, 239, 240, 245, 247, 259, 264, 281, 282, 285, 286, 298, 300, 302, 303, 305, 309, 311, 316, 317, 319, 320, 322, 323, 332, 336, 337, 339, 345, 348, 349, 350, 351, 352, 353, 355, 356, 376, 380, 386, 389, 394, 398, 403, 404, 406, 410, 414, 415, 417, 420, 421, 426, 437, 438, 441, 443, 444, 455, 459, 464, 468, 469, 470, 473, 475, 476, 478, 480, 485, 491, 492, 498, 499, 502, 506, 518, 519, 521, 523, 529, 532, 533, 537, 538, 542, 546, 550, 554, 555, 557, 561, 564, 566, 569, 572, 574, 575, 576, 578, 579, 580, 590, 591, 596, 597, 598, 605, 608, 610, 612, 614, 617, 624, 626, 627, 631, 634, 636, 647, 657, 659, 661, 665, 670, 675, 680, 681, 683, 685, 687, 693, 694, 695, 697, 699, 703, 704, 705, 706, 721, 723, 724, 728, 729, 737, 739, 747, 750, 751, 754, 756, 758, 759, 760, 764, 768, 771, 773, 781, 783, 785, 790, 792, 801, 804, 805, 806, 808, 809, 813, 816, 828, 829, 830, 834, 836, 840, 841, 846, 848, 849, 858, 861, 862, 867, 875, 877, 878, 881, 885, 886, 887, 888, 890, 892, 901, 908, 912, 914, 916, 923, 925, 928, 935, 940, 941, 948, 949, 950, 951, 955, 958, 966, 969, 972, 973, 977, 978, 981, 990, 991, 994, 997]
dis10 = [6, 17, 36, 61, 67, 78, 85, 113, 146, 180, 247, 281, 337, 339, 345, 349, 353, 441, 455, 459, 468, 469, 473, 485, 538, 561, 614, 617, 647, 657, 681, 687, 694, 695, 697, 721, 724, 737, 739, 773, 783, 801, 816, 901, 928, 935, 950, 958, 978, 997]

shares = []
for user in dis2:
    shares.append(sum(links[user]))
    print(user, links[user])

print(shares)