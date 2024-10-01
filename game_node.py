from __future__ import annotations # отложенное исполнение аннотаций

class GameNode:
    """Объект узла дерева
    """
    
    def __init__(
        self,
        matrix : list[list[int]],
        c_nodes : list[GameNode],
        h_value : int = None,
        g_value : int | None = None,
        f_value : int | None = None,
        el_move : int | None = None,
        ) -> None:
        
        """Инициализация объекта узла дерева

        Args:
            matrix (list[list[int]]): матрица узла
            c_nodes (list[GameNode]): ссылки на дочерние узлы
            h_value (int): номер хода
            g_value (int): значений вне позиции
            f_value (int): результат оценочной функции
            el_move (int): задействованный в ходе елемент
        """
        self.__matrix = matrix
        self.__c_nodes = c_nodes
        self.__h_value = h_value
        self.__g_value = g_value
        self.__f_value = f_value
        self.__el_move = el_move
        
    # свойсвто-геттер
    @property
    def matrix(self):
        return self.__matrix
    
    @property
    def c_nodes(self):
        return self.__c_nodes
    
    @property
    def h_value(self):
        return self.__h_value
    
    @property
    def g_value(self):
        return self.__g_value
    
    @property
    def f_value(self):
        return self.__f_value
    
    @property
    def el_move(self):
        return self.__el_move
        
    @c_nodes.setter
    def c_nodes(self, c_nodes):
        self.__c_nodes = c_nodes
    
    @h_value.setter
    def h_value(self, h_value):
        self.__h_value = h_value
        
    @g_value.setter
    def g_value(self, g_value):
        self.__g_value = g_value
        
    @f_value.setter
    def f_value(self, f_value):
        self.__f_value = f_value
        
    @el_move.setter
    def el_move(self, el_move):
        self.__el_move = el_move
        
        
    def __eq__(self, other) -> bool:
        return self.matrix == other.matrix
        