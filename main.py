from game_tree import GameTree
from game_node import GameNode

# игра восьмяшки - пятнашки

goal_matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

start_matrix = [
    [2, 4, 3],
    [1, 8, 5],
    [7, 0, 6]
]

game_ai = GameTree(goal_matrix=goal_matrix, 
                   start_matrix=start_matrix)
'''
node3 = GameNode(
    matrix=[[2, 4, 3],
            [1, 8, 5],
            [7, 6, 0]],
    c_nodes=[],
    h_value=1,
    g_value=7,)

node2 = GameNode(
    matrix=[[2, 4, 3],
            [1, 0, 5],
            [7, 8, 6]],
    c_nodes=[],
    h_value=1,
    g_value=6,)

node1 = GameNode(
    matrix=[[2, 4, 3],
            [1, 8, 5],
            [0, 7, 6]],
    c_nodes=[],
    h_value=1,
    g_value=8,)

node0 = GameNode(
    matrix=[[1, 2, 3],
            [4, 5, 0],
            [7, 8, 6]],
    c_nodes=[],
    h_value=5,
    g_value=2,
    el_move=5)
'''
#game_ai.root.c_nodes.append(node1)
#game_ai.root.c_nodes.append(node2)
#game_ai.root.c_nodes.append(node3)

flag = True
while(flag):
    flag = game_ai.do_next_move()
