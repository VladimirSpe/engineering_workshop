import numpy as np
import logging
from Inp_Rea import Read_Json


class Basic_methods:
    def __init__(self, matrix):
        self.matrix = matrix

    def reduction(self):
        """Поиск минимумов и удаление их"""

        f = np.amin(self.matrix[1:, 1:], keepdims=True, axis=1)
        self.matrix[1:, 1:] = self.matrix[1:, 1:] - np.amin(self.matrix[1:, 1:], keepdims=True, axis=1)
        f2 = np.amin(self.matrix[1:, 1:], keepdims=True, axis=0)
        self.matrix[1:, 1:] = self.matrix[1:, 1:] - np.amin(self.matrix[1:, 1:], keepdims=True, axis=0)
        h = np.sum(f) + np.sum(f2)
        return np.copy(self.matrix), h

    def zero_rating(self):
        """Функция, реализующая подсчет весов нулей"""

        x, y = np.where(self.matrix[1:, 1:] == 0)
        m = self.matrix[1:, 1:]
        d = {}
        for i in range(len(x)):
            row_sort = np.sort(m[:, y[i]])
            str_sort = np.sort(m[x[i], :])
            row_min = row_sort[1]
            str_min = str_sort[1]
            d[(int(self.matrix[1:, 0][x[i]]), int(self.matrix[0][1:][y[i]]), x[i], y[i])] = row_min + str_min
        # for i in range(len(x)):
        #     str_min1 = np.min(m[x[i], :][:y[i]]) if len(m[x[i], :][:y[i]]) != 0 else np.inf
        #     str_min2 = np.min(m[x[i], 1:][y[i]:]) if len(m[x[i], 1:][y[i]:]) != 0 else np.inf
        #     row_min1 = np.min(m[:, y[i]][:x[i]]) if len(m[:, y[i]][:x[i]]) != 0 else np.inf
        #     row_min2 = np.min(m[:, y[i]][x[i] + 1:]) if len(m[:, y[i]][x[i] + 1:]) != 0 else np.inf
        #     row_min = min(row_min1, row_min2)
        #     st_min = min(str_min1, str_min2)
        #     d[(int(self.matrix[1:, 0][x[i]]), int(self.matrix[0][1:][y[i]]), x[i], y[i])] = row_min + st_min
        print(f"Zero: {sorted(d, key=lambda k: d[k], reverse=True)}")
        return sorted(d, key=lambda k: d[k], reverse=True)[0]


class Var_edge:
    """Класс для хранения ветвей графа (matrix - Полученная матрица перед дейстивем с графом, h - вес предыдущей мартицы,
     coord_edge - координаты графа, f - флаг, добавили или удалили граф)"""

    def __init__(self, matrix: np.array, h: int, coord_edge, f: bool):
        self.h = 0
        self.matrix, self.hh, self.coord_edge, self.f = matrix, h, coord_edge, f

    def include_edge_graph(self):
        """Добавление ветви"""

        if self.coord_edge[0] in self.matrix[0] and self.coord_edge[1] in self.matrix[1:, 0]:
            y = np.where(self.matrix[0] == self.coord_edge[0])[0]
            x = np.where(self.matrix[:, 0] == self.coord_edge[1])[0]
            self.matrix[x[0]][y[0]] = np.inf
        self.matrix = np.delete(self.matrix, self.coord_edge[2] + 1, axis=0)
        self.matrix = np.delete(self.matrix, self.coord_edge[3] + 1, axis=1)
        self.prep()

    def exclude_edge_graph(self):
        """Удаление ветви"""

        self.matrix[self.coord_edge[2] + 1][self.coord_edge[3] + 1] = np.inf
        self.prep()

    def prep(self):
        """Функция для просчета H после удаления или добавления"""

        m, self.h = Basic_methods(self.matrix).reduction()
        self.h += self.hh

    def __le__(self, other):
        return self.h <= other.h

    def __lt__(self, other):
        return self.h < other.h


class Main_method:
    def __init__(self, file_name, matrix):

        if file_name == 0:
            mat = Read_Json(file_name)
            ff = mat.preparation()
            matrix = np.array([i for i in range(np.shape(ff[0])[0] + 1)])
            mm = np.column_stack((np.array([np.array(i) for i in range(1, np.shape(ff[0])[0] + 1)]), ff[0]))
            self.matrix = np.vstack((matrix, mm))
        else:
            self.matrix = matrix
        self.h = 0
        self.answer = []  # Список с конечным ответом
        self.list_dangling_branches = []  # Список оборванных ветвей
        self.solution = []  # Решение для каждого ребенка дерева

    def solution_cycle(self):
        """Основной цикл"""

        while np.shape(self.matrix)[0] != 3:
            base = Basic_methods(self.matrix)
            matr, h = base.reduction()
            coord_edge = base.zero_rating()
            inc = Var_edge(matr.copy(), h if len(self.solution) == 0 else self.solution[-1].h, coord_edge, True)  # Маршрут с добавлением графа
            inc.include_edge_graph()
            ex = Var_edge(matr.copy(), h if len(self.solution) == 0 else self.solution[-1].h, coord_edge, False)  # Маршрут с удалением графа
            ex.exclude_edge_graph()
            self.choosing_path(inc, ex)
        mat, self.h = Basic_methods(self.matrix).reduction()  # Формирование ответа после получения матрицы 2х2
        self.h += self.solution[-1].h
        self.solution.append(
            Var_edge(self.matrix, self.h + self.solution[-1].h, (self.matrix[:, 0][-1], self.matrix[0][1]), True))
        self.solution.append(
            Var_edge(self.matrix, self.h + self.solution[-1].h, (self.matrix[:, 0][1], self.matrix[0][2]), True))
        for i in self.solution:
            if i.f:
                self.answer.append(i.coord_edge[:2])
        return self.answer, self.h

    def choosing_path(self, inc, ex):
        """Функция для выбора оптимального дерева (с графом или без)"""
        if inc <= ex:
            if self.checking_past_paths(inc, ex):
                self.list_dangling_branches.append([ex, self.solution[:]])
                self.solution.append(inc)
                self.matrix = inc.matrix.copy()
                self.h = inc.h

        elif self.checking_past_paths(ex, inc):
            self.list_dangling_branches.append([inc, self.solution[:]])
            self.solution.append(ex)
            self.matrix = inc.matrix.copy()
            self.h = inc.h

    def checking_past_paths(self, cl, cl1):
        """Проверка на оптимальность в оборванных ветвях"""

        for i in range(len(self.list_dangling_branches)):
            if self.list_dangling_branches[i][0] < cl:
                self.list_dangling_branches.append([cl, self.solution[:]])
                self.list_dangling_branches.append([cl1, self.solution[:]])
                self.solution = self.list_dangling_branches[i][1][:]
                self.solution.append(self.list_dangling_branches[i][0])
                self.matrix = self.list_dangling_branches[i][0].matrix.copy()
                self.h = self.list_dangling_branches[i][0].h
                del self.list_dangling_branches[i]

                return False
        return True


if __name__ == "__main__":
    logging.basicConfig(filename="dd.log", filemode="w")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    mat = np.array([[0, 1, 2, 3, 4, 5, 6],
                  [1, np.inf, 10, 15, 11, 2, 55],
                  [2, 17, np.inf, 16, 18, 21, 13],
                  [3, 10, 50, np.inf, 39, 22, 3],
                  [4, 28, 29, 24, np.inf, 28, 25],
                  [5, 27, 9, 32, 9, np.inf, 2],
                  [6, 43, 48, 40, 43, 21, np.inf]])
    m = Main_method(1, mat)
    print(m.solution_cycle())

