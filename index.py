from gurobipy import *

file = open('Instances/instance1.txt', "r")
lines = file.readlines()
n = int(lines[1].strip('\n'))
line = 3
graph = [[0 for _ in range(n)] for _ in range(n)]
while lines[line][0] != '#':
    i, j = lines[line].strip('\n').split(' ')
    graph[int(i)][int(j)] = 1
    graph[int(j)][int(i)] = 1
    line += 1


model = Model('Graph Coloring model')

x = [[model.addVar(vtype=GRB.BINARY, name="Vertex " + str(i) + " colored with color " + str(j))
          for j in range(len(graph))]
         for i in range(len(graph))]

w = [model.addVar(vtype=GRB.BINARY, name="Color " + str(j) + " used") for j in range(len(graph))]
model.update()


model.setObjective(quicksum(w[j] for j in range(len(w))))

for i in range(len(x)):
    model.addConstr(quicksum(x[i][j] for j in range(len(w))) == 1, name="One color in vertex " + str(i))

for i in range(len(x)):
    for k in range(len(x)):
        if graph[i][k] == 1 or graph[k][i] == 1:
            for j in range(len(w)):
                model.addConstr(x[i][j] + x[k][j] <= w[j],
                                name="Sum of colors of vertex " + str(i) + " and " + str(k)
                                        + " less or equal color " + str(j))
model.update()


model.optimize()
