from parameters import *
import numpy as np
import functions as f
import model as m



def strongest_SNR(number_of_users, SNR,  k):
    # connect to k base stations with highest SNR (if SNR > SNR_min)
    links = np.zeros((number_of_users, number_of_bs))
    for u in range(number_of_users):
        sorted_BS = np.argsort(SNR[u])
        for b in sorted_BS[:k]:
            if SNR[u, b] > min_SNR:
                links[u, b] = 1
    return links

def strongest_SINR(number_of_users, SINR,  k):
    # connect to k base stations with highest SINR (if SINR > SNR_min)
    # assuming every BS is `on` - so every beam that is directed towards the user will interfere
    links = np.zeros((number_of_users, number_of_bs))
    for u in range(number_of_users):
        sorted_BS = np.argsort(SINR[u])
        for b in sorted_BS[:k]:
            if SINR[u, b] > min_SINR:
                links[u, b] = 1
    return links

def closest(number_of_users, distances, SNR, k):
    # connect to k base stations with highest SNR (if SNR > SNR_min)
    links = np.zeros((number_of_users, number_of_bs))
    for u in range(number_of_users):
        sorted_BS = np.argsort(distances[u])
        for b in sorted_BS[:k]:
            if SNR[u, b] > min_SNR:
                links[u, b] = 1
    return links

def online_load(number_of_users, SNR):
    # every user connects to the BS with the smallest load
    # ties: connect to closest
    links = np.zeros((number_of_users, number_of_bs))
    for u in range(number_of_users):
        BS_load = sum(links)
        minimum_load = min(BS_load)
        first_bs = np.where(BS_load == minimum_load)
        snr = math.inf
        for b in first_bs[0]:
            if SNR[u, b] < snr:
                snr = SNR[u, b]
                bs = b
        links[u, bs] = 1
    return links


