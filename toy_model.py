import gurobipy as gp
from gurobipy import GRB
from gurobipy import quicksum


# ------------------------ Start of optimization program ------------------------------------
try:
    m = gp.Model("Model 1")
    # m.setParam('NonConvex', 2)
    # m.Params.LogToConsole = 0

    n = 1
    k = 1

    # -------------- VARIABLES -----------------------------------
    x = {}
    x_sum = {}
    log_obj = {}

    for i in range(n):
        for j in range(k):
            x[i, j] = m.addVar(vtype= GRB.CONTINUOUS, name = f'x{i}')
        log_obj[i] = m.addVar(vtype= GRB.CONTINUOUS, name = f'log_x{i}')
        x_sum[i] = m.addVar(vtype = GRB.CONTINUOUS, name = f'x_sum{i}')

    m.update()

    # ----------------- OBJECTIVE ----------------------------------
    m.setObjective(quicksum(log_obj[i] for i in range(n)), GRB.MAXIMIZE)


    # --------------- CONSTRAINTS -----------------------------
    for i in range(n):
        for j in range(k):
            m.addConstr(x[i, j] <= 5)
            m.addConstr(x_sum[i] == quicksum(x[i,j] for j in range(k)))
        m.addGenConstrLog(x_sum[i], log_obj[i])

    # for i in range(n):
    #     m.addConstr(x[i] <= 5)
    #
    # for i in range(n):
    #     m.addGenConstrLog(x[i], log_obj[i])


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


print([x[i].X for i in range(n)])



