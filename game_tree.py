from __future__ import annotations
from game_node import GameNode
import networkx as nx
import matplotlib.pyplot as plt

class GameTree:
    """Объект дерева
    """
    def __init__(
        self, 
        goal_matrix : list[list[int]], 
        start_matrix : list[list[int]],
        ) -> None:
        
        """Инициализация объекта дерева

        Args:
            goal_matrix (list[list[int]]): целевое состояние
            start_matrix (list[list[int]]): начальное состояние или корень дерева
        """
        
        self.__goal = GameNode(
            matrix=goal_matrix,
            c_nodes=[], 
            h_value=0, 
            g_value=0,)
        
        self.__root = GameNode(
            matrix=start_matrix,
            c_nodes=[], 
            h_value=0, 
            g_value=self.count_g_value(start_matrix),)
        self.root.f_value = self.count_f_value(self.root)
    
    @property
    def goal(self):
        return self.__goal
    
    @property
    def root(self):
        return self.__root
    
    @root.setter
    def root(self, root):
        self.__root = root
       
       
    def count_f_value(self, node : GameNode) -> int:
        """Подсчет оценочной функции (f_value)

        Args:
            node (GameNode): узел

        Returns:
            int: значение оценочной функции (f_value)
        """
        return node.g_value + node.h_value
    
    
    def count_g_value(self, matrix : list[list[int]]) -> int:
        """Подсчет значений вне позиции (g_value)

        Args:
            matrix (list[list[int]]): матрица для сравнения с целевой матрицей

        Returns:
            int: число значений вне позиции (g_value)
        """
        g_value = 0
        
        len_goal_matrix = len(self.goal.matrix) 
        for i in range(len_goal_matrix):
            for j in range(len_goal_matrix):
                if self.goal.matrix[i][j] != matrix[i][j]:
                    g_value += 1
        
        return g_value
    
       
    def search_min_f_value_node(self) -> GameNode:
        """Поиск узла-листа с минимальным значением оценочной функции (обход дерева в глубину)
        """
        # https://ilyachalov.livejournal.com/176395.html
        memory = [self.root]    # память (стек)
                                # в начале память содержит ссылку на корень заданного дерева
        node_with_min_f_value = self.root # запоминаем узел с минимальным f_value
        # внешний цикл, перебирающий линии заглублейний
        # закончить цикл, если не получается извлечь ссылку из памяти (стека)
        while memory:
            cur_ref = memory.pop() # текущая ссылка
            # внутренний цикл обхода каждой линии заглубления дерева до листа
            while True:
                # обработка данных узла...
                if cur_ref.g_value is None:
                    cur_ref.g_value = self.count_g_value(cur_ref.matrix)
                if cur_ref.f_value is None:
                    cur_ref.f_value = self.count_f_value(cur_ref)
                    
                # если значение f текущего узла меньше или равно f записанного узла и
                # если текущий узел - это лист
                if cur_ref.f_value <= node_with_min_f_value.f_value and not cur_ref.c_nodes:
                    node_with_min_f_value = cur_ref # запоминаем ссылку на текущий узел
                
                # если узел - это лист, выйти из цикла
                if not cur_ref.c_nodes:
                    break
                
                # помещаем ветви, ведущие налево, в память (стек)
                # если только один дочерний узел, переходим к нему без работы с памятью
                for i in range(len(cur_ref.c_nodes) - 1):
                    memory.append(cur_ref.c_nodes[i])

                # переходим по ветви, ведущей направо
                cur_ref = cur_ref.c_nodes[-1]
            
        return node_with_min_f_value    
    
    
    def generate_next_nodes(self, best_f_value_node : GameNode) -> GameNode | None:
        """Генерация новых узлов

        Args:
            best_f_value_node (GameNode): лучший узел по значению f_value

        Returns:
            GameNode | None: ссылка на решающий узел, иначе None
        """
        
        next_nodes : list[GameNode] = [] # список с полученными узлами 
        space_i_j = []  # индекс пустого пространства в матрице
        possible_moves = [] # список списков возможных ходов
        # поиск пустого пространства в матрице узла
        len_matrix = len(best_f_value_node.matrix) 
        for i in range(len_matrix):
            if best_f_value_node.matrix[i].count(0):
                space_i_j.append(i) # добавляем i индекс
                space_i_j.append(best_f_value_node.matrix[i].index(0)) # добавляем j индекс
        
        # проверяем возможность хода:
        # сверху
        # проверяем ограничение матрицы сверху и
        # (проверяем None значения ранее пересталвенного элемента (root) или
        # проверяем на отношение елемента сверху с ранее перестановленным элементом)
        if (space_i_j[0] > 0 and
            (best_f_value_node.el_move is None or
            best_f_value_node.matrix[space_i_j[0] - 1][space_i_j[1]] != best_f_value_node.el_move)):
            # добавляем [i, j] индексы в возможные варианты перестановки
            possible_moves.append([space_i_j[0] - 1, space_i_j[1]])
        # снизу 
        if (space_i_j[0] < len_matrix - 1 and
            (best_f_value_node.el_move is None or
            best_f_value_node.matrix[space_i_j[0] + 1][space_i_j[1]] != best_f_value_node.el_move)):
            possible_moves.append([space_i_j[0] + 1, space_i_j[1]])
        # справа  
        if (space_i_j[1] < len_matrix - 1 and
            (best_f_value_node.el_move is None or
                best_f_value_node.matrix[space_i_j[0]][space_i_j[1] + 1] != best_f_value_node.el_move)):
            possible_moves.append([space_i_j[0], space_i_j[1] + 1])
        # слева
        if (space_i_j[1] > 0 and
            (best_f_value_node.el_move is None or
                best_f_value_node.matrix[space_i_j[0]][space_i_j[1] - 1] != best_f_value_node.el_move)):
            possible_moves.append([space_i_j[0], space_i_j[1] - 1])
        
        # клонируем матрицы с перестановками
        for move in possible_moves:
            new_el_move = best_f_value_node.matrix[move[0]][move[1]] # запоминаем значение элемента перестановки
            new_matrix = []
            for i in range(len_matrix):
                new_i_list = []
                for j in range(len_matrix):
                    # если i, j индексы элемента перестановки, записываем 0
                    if move[0] == i and move[1] == j:
                        new_i_list.append(0)
                    # если i, j индексы пустого пространства матрицы (0), записываем элемент перестановки
                    elif space_i_j[0] == i and space_i_j[1] == j:
                        new_i_list.append(new_el_move)
                    # иначе переносим значение из матрицы род.узла в новую матрицу
                    else:
                        new_i_list.append(best_f_value_node.matrix[i][j])
                new_matrix.append(new_i_list)
            
            # генерируем новый узел
            next_node = GameNode(
                matrix=new_matrix,
                c_nodes=[],
                h_value=best_f_value_node.h_value + 1,
                g_value=self.count_g_value(new_matrix),
                el_move=new_el_move # элемент, который был переставлен на данном ходе
            )
            next_nodes.append(next_node)
        # назначаем род.узлу ссылки на вышесозданные дочерние узлы
        best_f_value_node.c_nodes = next_nodes
        # проверяем: есть ли среди новых узлов решающий
        game_finished_node = None
        for next_node in next_nodes:
            if next_node == self.goal:
                game_finished_node = next_node
                break
        return game_finished_node
    
    
    def show_game_tree(self) -> None:
        pass
        