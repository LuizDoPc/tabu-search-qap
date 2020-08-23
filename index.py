import numpy as np
import pandas as pd
import itertools as itr
import math
import readDat
import time

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

def getInitialSolution(indexes):
    init = indexes
    initSol = []
    cont = 0
    while cont < len(init):
        rIndex = np.random.randint(0, len(init))
        if init[rIndex] not in initSol:
            initSol.append(init[rIndex])
            cont += 1
    return initSol


def tabuSearchToQAP(filename):
    res = readDat.readFile(filename)

    INDEXES = getIndexes(res.get("len"))

    distric = pd.DataFrame(res.get("distric"),
                           columns=INDEXES,
                           index=INDEXES)

    flow = pd.DataFrame(res.get("flow"),
                        columns=INDEXES,
                        index=INDEXES)

    initialSolution = getInitialSolution(INDEXES)

    reindexedDistrict = distric.reindex(
        columns=initialSolution, index=initialSolution)
    reindexedDistrictArray = np.array(reindexedDistrict)

    objFuncStartValue = pd.DataFrame(reindexedDistrictArray*flow)
    objFuncStartArray = np.array(objFuncStartValue)

    finalStartValue = sum(sum(objFuncStartArray))

    initialSolutionCopy = initialSolution[:]

    MAX_ITERATIONS = 60

    tabuListSize = 10

    tabuList = np.empty((0, len(initialSolution)+1))

    finalSolution = []

    currentIteration = 1

    solutions = np.empty((0, len(initialSolution)+1))

    for i in range(MAX_ITERATIONS):
        neighbors = list(itr.combinations(initialSolution, 2))

        neighborIndex = 0

        solutionTracker = np.empty((0, len(initialSolution)))

        for i in neighbors:
            swapAux = []
            swapPair = neighbors[neighborIndex]
            pairA = swapPair[0]
            pairB = swapPair[1]

            u = 0
            for j in initialSolution:
                if initialSolution[u] == pairA:
                    swapAux = np.append(swapAux, pairB)
                elif initialSolution[u] == pairB:
                    swapAux = np.append(swapAux, pairA)
                else:
                    swapAux = np.append(swapAux, initialSolution[u])

                swapAux = swapAux[np.newaxis]

                u += 1

            solutionTracker = np.vstack((solutionTracker, swapAux))

            neighborIndex += 1

        objFuncAllSolutions = np.empty((0, len(initialSolution)+1))
        objFuncValues = np.empty((0, len(initialSolution)+1))

        for i in solutionTracker:

            reindexedDistrict = distric.reindex(columns=i, index=i)
            reindexedDistrictArray = np.array(reindexedDistrict)

            objFuncStartValue = pd.DataFrame(reindexedDistrictArray*flow)
            objFuncStartArray = np.array(objFuncStartValue)

            totalCost = sum(sum(objFuncStartArray))

            i = i[np.newaxis]

            objFuncAllSolutions = np.column_stack((totalCost, i))

            objFuncValues = np.vstack((objFuncValues, objFuncAllSolutions))

        objFuncValuesOrdered = np.array(
            sorted(objFuncValues, key=lambda x: x[0]))

        t = 0
        currSolution = objFuncValuesOrdered[t]

        while currSolution[0] in tabuList[:, 0]:
            currSolution = objFuncValuesOrdered[t]
            t += 1

        if len(tabuList) >= tabuListSize:
            tabuList = np.delete(tabuList, (tabuListSize-1), axis=0)

        tabuList = np.vstack((currSolution, tabuList))

        solutions = np.vstack((currSolution, solutions))

        modIterations = currentIteration % 10

        randomA = np.random.randint(1, len(initialSolution)+1)
        randomB = np.random.randint(1, len(initialSolution)+1)
        randomC = np.random.randint(1, len(initialSolution)+1)

        if modIterations == 0:
            solutionAux = []
            swapA = currSolution[randomA]
            swapB = currSolution[randomB]

            solAux = currSolution

            w = 0
            for _ in solAux:
                if solAux[w] == swapA:
                    solutionAux = np.append(solutionAux, swapB)
                else:
                    if solAux[w] == swapB:
                        solutionAux = np.append(solutionAux, swapA)
                    else:
                        solutionAux = np.append(solutionAux, solAux[w])
                w += 1

            currSolution = solutionAux

            solutionAux = []
            swapA = currSolution[randomA]
            swapB = currSolution[randomC]

            w = 0
            for _ in currSolution:
                if currSolution[w] == swapA:
                    solutionAux = np.append(solutionAux, swapB)
                else:
                    if currSolution[w] == swapB:
                        solutionAux = np.append(solutionAux, swapA)
                    else:
                        solutionAux = np.append(solutionAux, currSolution[w])
                w += 1

            currSolution = solutionAux

        initialSolution = currSolution[1:]

        currentIteration += 1

        if modIterations == 5 or modIterations == 0:
            tabuListSize = np.random.randint(5, 20)

    t = 0
    finalAux = []
    for _ in solutions:
        if (solutions[t, 0]) <= min(solutions[:, 0]):
            finalAux = solutions[t, :]
        t += 1

    finalSolution = finalAux[np.newaxis]
    """
    print("QAP WITH DYNAMIC TABU LIST")
    print("Initial Solution:", " ".join(initialSolutionCopy))
    print("Initial Cost:", finalStartValue)
    print("Final Solution:", " ".join(finalSolution[0, 1:]))
    print("Final Cost:", finalSolution[0, 0])
    """
    return {"Solução inicial": " ".join(initialSolutionCopy), "Custo inicial": finalStartValue, "Solução final": " ".join(finalSolution[0, 1:]), "Custo final": finalSolution[0, 0]}


filenames = {"bur26a.dat": 5426670, "bur26b.dat": 3817852, "bur26c.dat": 5426795, "bur26d.dat": 3821225, "bur26e.dat": 5386879,
             "bur26f.dat": 3782044, "bur26g.dat": 10117172, "bur26h.dat": 7098658, "esc32a.dat": 130, "esc32b.dat": 168, "esc32c.dat": 642, "esc32d.dat": 200}

linhas = {}
for name in filenames:
    print("name = ", name)
    tempoInicial = time.time()
    res = tabuSearchToQAP("./inputs/" + name)
    tempoFinal = time.time()
    res["Custo ótimo"] = filenames[name]
    res["Precisão (%)"] = (100 * filenames[name]) / float(res["Custo final"])
    res["Tempo (s)"] = tempoFinal - tempoInicial
    linhas[name] = res
pd.set_option('display.max_colwidth', -1)
tabela = pd.DataFrame.from_dict(linhas, orient='index')
print(tabela.to_latex())
