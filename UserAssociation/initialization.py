
def initialization(simulation_number):
    if simulation_number >= 25:
        simulation_number -= 24
        penalty_importantness = 1000
    else:
        penalty_importantness = 500
    if simulation_number <= 12:
        hexagonal = True
        ppp = False
    else:
        hexagonal = False
        ppp = True
    if simulation_number in [1, 7, 13, 19]:
        number_of_users_1 = 10
        number_of_users_2 = 10
        number_of_users_3 = 10
        number_of_iterations = 3334
    elif simulation_number in [2, 8, 14, 20]:
        number_of_users_1 = 50
        number_of_users_2 = 5
        number_of_users_3 = 1
        number_of_iterations = 1786
    elif simulation_number in [3, 9, 15, 21]:
        number_of_users_1 = 20
        number_of_users_2 = 20
        number_of_users_3 = 20
        number_of_iterations = 1667
    elif simulation_number in [4, 10, 16, 22]:
        number_of_users_1 = 30
        number_of_users_2 = 30
        number_of_users_3 = 30
        number_of_iterations = 1111
    elif simulation_number in [5, 11, 17, 23]:
        number_of_users_1 = 40
        number_of_users_2 = 40
        number_of_users_3 = 40
        number_of_iterations = 834
    elif simulation_number in [6, 12, 18, 24]:
        number_of_users_1 = 100
        number_of_users_2 = 10
        number_of_users_3 = 2
        number_of_iterations = 893
    if simulation_number <= 6 or 13 <= simulation_number <= 18:
        OBJECTIVE = 1
    elif 7 <= simulation_number <= 12 or 19 <= simulation_number <= 24:
        OBJECTIVE = 0
    if simulation_number == 19:
        gamma = [0.54, 0.53, 0.66]
    elif simulation_number == 22:
        gamma = [0.04, 0.15, 0.58]
    else:
        gamma = [0.5, 0.5, 0.5]
    return hexagonal, ppp, number_of_users_1, number_of_users_2, number_of_users_3, OBJECTIVE, number_of_iterations, penalty_importantness, gamma
