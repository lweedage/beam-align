import gurobipy as gp
from gurobipy import GRB
from gurobipy import quicksum
import numpy as np

# ------------------------ Start of optimization program ------------------------------------

try:
    m = gp.Model("Model 1")
    m.setParam('NonConvex', 2)
    # m.Params.LogToConsole = 0

    users = range(10)
    base_stations = range(2)

    alpha = 2

    # -------------- VARIABLES -----------------------------------
    x = {}
    x_sum = {}
    log_obj = {}
    maxmin_obj = {}
    SINR = {}
    sigma_I = {}
    C = {}
    log_C = {}
    I_inv = {}

    I = {}

    for i in users:
        for j in base_stations:
            x[i, j] = m.addVar(vtype= GRB.BINARY, name = f'x{i}')
            SINR[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'SINR#{i}#{j}')
            I[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'I#{i}#{j}')
            sigma_I[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'sigma_I#{i}#{j}')
            I_inv[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'I_inv#{i}#{j}')
            C[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'C#{i}#{j}')
            log_C[i, j] = m.addVar(vtype=GRB.CONTINUOUS, name=f'logC#{i}#{j}')
        log_obj[i] = m.addVar(vtype= GRB.CONTINUOUS, name = f'log_x{i}')
        x_sum[i] = m.addVar(vtype = GRB.CONTINUOUS, name = f'x_sum{i}')
        maxmin_obj[i] = m.addVar(vtype= GRB.CONTINUOUS, name = f'maxmin_x{i}')


    m.update()

    # ----------------- OBJECTIVE ----------------------------------
    if alpha == 1:
        m.setObjective(quicksum(log_obj[i] for i in base_stations), GRB.MAXIMIZE)
    elif alpha == 0:
        m.setObjective(quicksum(x_sum[i] for i in base_stations), GRB.MAXIMIZE)
    else:
        m.setObjective(1 / (1 - alpha) * quicksum(maxmin_obj[i] for i in base_stations), GRB.MAXIMIZE)

    # --------------- CONSTRAINTS -----------------------------
    for i in users:
        m.addConstr(x_sum[i] == quicksum(SINR[i,j] for j in base_stations))
        m.addGenConstrLog(x_sum[i], log_obj[i])
        for j in base_stations:
            m.addConstr(SINR[i,j] <= SINR[i,j] * x[i,j])

    for i in users:
        m.addGenConstrPow(x_sum[i], maxmin_obj[i], 1 - alpha)

    for i in users:
        for j in base_stations:
            m.addConstr(I[i, j] == quicksum(quicksum(x[k, m] * 0.05 for k in users if not (i == k and j == m)) for m in
                base_stations), name=f'Interference#{i}#{j}')
            m.addConstr(I[i, j] * I_inv[i, j] == 1, name=f'helper_constraint#{i}#{j}')
            m.addConstr(SINR[i, j] == x[i, j] * I_inv[i, j], name=f'find_SINR#{i}#{j}')

    # --------------------- OPTIMIZE MODEL -------------------------
    # m.computeIIS()
    # m.write("IIS_toy_model.lp")

    m.optimize()
    m.write("toy_model.lp")
    m.getObjective()
    print('Objective value: %g' % m.objVal)




except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))
    # sys.exit()


print([sum([x[i,j].X for j in base_stations]) for i in users])
print([[I[i,j].X for j in base_stations] for i in users])

a = np.zeros((len(users), len(base_stations)))

for i in users:
    for j in base_stations:
        a[i, j] = x[i, j].X
