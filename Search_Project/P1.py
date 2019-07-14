from search import *
import matplotlib.pyplot as plt
import time
import numpy as np
import math

# Primeiramente vamos montar o grid
w, h = 60, 60
matrix = [[0 for x in range(w)] for y in range(h)]


# Conjunto de funcoes secundarias
def restart_matrix():
    for i in range(0, 60):
        for j in range(0, 60):
            matrix[i][j] = 0
    restricao()


def restricao():
    for i in range(0, 60):
        for j in range(0, 60):
            if j == 20 and i > 20:
                matrix[i][j] = "x"
            if i == 0 or i == 59 or j == 0 or j == 59:
                matrix[i][j] = "x"
            if i < 40 and j == 40:
                matrix[i][j] = "x"
    matrix[int(ini[0])][int(ini[1])] = "s"
    matrix[int(fim[0])][int(fim[1])] = "e"


def imprime_matrix():
    for i in range(0, 60):
        for j in range(0, 60):
            if j == 59:
                print(matrix[i][j])
            else:
                print(matrix[i][j], end=' ')


# Funcao para auxiliar na impressao do grafico
def samplemat(dims):
    data = np.zeros(dims)
    for i in range(0, 60):
        for j in range(0, 60):
            if matrix[i][j] == "x":
                data[i, j] = 1
            if matrix[i][j] == "0":
                data[i, j] = 2
            if matrix[i][j] == "s":
                data[i, j] = 3
            if matrix[i][j] == "e":
                data[i, j] = 4
            if matrix[i][j] == "t":
                data[i, j] = 5
    return data


def imprime_graph():
    plt.matshow(samplemat((60, 60)))
    plt.show()


# Entrar as coordenadas de inicio e objetivo
print("Digite a coordenada de início:")
ini_input = input()
ini = ini_input.split()
print("Digite a coordenada de fim:")
fim_input = input()
fim = fim_input.split()

# Colocar as restricoes na matriz
restricao()


# Nessa parte vamos definir problema
class robotProblem(Problem):

    def __init__(self, initial, goal):
        Problem.__init__(self, initial, goal)

    def actions(self, stateStr):
        state = stateStr.split()
        possible_actions = ['UP', 'UPLEFT', 'UPRIGHT', 'DOWN', 'DOWNLEFT', 'DOWNRIGHT', 'LEFT', 'RIGHT']
        if matrix[int(state[0])][int(state[1])+1] == "x":
            possible_actions.remove('LEFT')
        if matrix[int(state[0])+1][int(state[1])] == "x":
            possible_actions.remove('UP')
        if matrix[int(state[0])][int(state[1])-1] == "x":
            possible_actions.remove('RIGHT')
        if matrix[int(state[0])-1][int(state[1])] == "x":
            possible_actions.remove('DOWN')
        if matrix[int(state[0])+1][int(state[1])+1] == "x":
            possible_actions.remove('UPLEFT')
        if matrix[int(state[0])+1][int(state[1])-1] == "x":
            possible_actions.remove('UPRIGHT')
        if matrix[int(state[0])-1][int(state[1])+1] == "x":
            possible_actions.remove('DOWNLEFT')
        if matrix[int(state[0])-1][int(state[1])-1] == "x":
            possible_actions.remove('DOWNRIGHT')
        return possible_actions

    def result(self, stateStr, action):
        state = stateStr.split()
        new_state = state
        if action == "UP":
            new_state[0] = str(int(state[0])+1)
            new_state[1] = str(int(state[1]))
        if action == "UPLEFT":
            new_state[0] = str(int(state[0])+1)
            new_state[1] = str(int(state[1])+1)
        if action == "UPRIGHT":
            new_state[0] = str(int(state[0])+1)
            new_state[1] = str(int(state[1])-1)
        if action == "DOWN":
            new_state[0] = str(int(state[0])-1)
            new_state[1] = str(int(state[1]))
        if action == "DOWNLEFT":
            new_state[0] = str(int(state[0])-1)
            new_state[1] = str(int(state[1])+1)
        if action == "DOWNRIGHT":
            new_state[0] = str(int(state[0])-1)
            new_state[1] = str(int(state[1])-1)
        if action == "LEFT":
            new_state[0] = str(int(state[0]))
            new_state[1] = str(int(state[1])+1)
        if action == "RIGHT":
            new_state[0] = str(int(state[0]))
            new_state[1] = str(int(state[1])-1)
        newstate = ' '.join(new_state)
        return newstate

    def goal_test(self, stateStr):
        state = stateStr.split()
        if not matrix[int(state[0])][int(state[1])] == "s" or matrix[int(state[0])][int(state[1])] == "e":
            matrix[int(state[0])][int(state[1])] = "t"
        return self.goal == stateStr


imprime_graph()
# Cria uma instancia do problema
theProblem = robotProblem(ini_input, fim_input)

# Roda essa instancia para o DFS
start_time1 = time.time()
solution1 = depth_first_graph_search(theProblem)
print("DFS runs in %.6s seconds" % (time.time() - start_time1))
print("DFS path cost is %s" % solution1.path_cost)
imprime_graph()
restart_matrix()

# Roda essa instancia para o BFS
start_time2 = time.time()
solution2 = breadth_first_graph_search(theProblem)
print("BFS runs in %.6s seconds" % (time.time() - start_time2))
print("BFS path cost is %s" % solution2.path_cost)
imprime_graph()
restart_matrix()


# Roda essa instancia para o astar com a heuristica de distancia manhattan
def manhattan(node):
    stateStr = node.state
    state = stateStr.split()
    objStr = fim_input
    obj = objStr.split()
    dx = abs(int(state[0]) - int(obj[0]))
    dy = abs(int(state[1]) - int(obj[1]))
    return dx + dy


start_time3 = time.time()
solution3 = astar_search(theProblem, manhattan)
print("A* with manhattan runs in %.6s seconds" % (time.time() - start_time3))
print("A* with manhattan path cost is %s" % solution3.path_cost)
imprime_graph()
restart_matrix()


# Roda essa instancia pra o astar com a distancia euclidiana
def euclidian(node):
    stateStr = node.state
    state = stateStr.split()
    objStr = fim_input
    obj = objStr.split()
    dx = abs(int(state[0]) - int(obj[0]))
    dy = abs(int(state[1]) - int(obj[1]))
    return math.sqrt(dx*dx + dy*dy)


start_time4 = time.time()
solution4 = astar_search(theProblem, euclidian)
print("A* with euclidian runs in %.6s seconds" % (time.time() - start_time4))
print("A* with euclidian path cost is %s" % solution4.path_cost)
imprime_graph()
restart_matrix()