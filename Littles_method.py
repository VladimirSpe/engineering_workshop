import re
from typing import *
import numpy as np
from Inp_Rea import Read_Json


class Basic_methods:
    def __init__(self, matrix: np.array):
        self.matrix = matrix

    def reduction(self) -> Tuple[np.array, int]:
        """Поиск минимумов и удаление их"""

        f = np.amin(self.matrix[1:, 1:], keepdims=True, axis=1)
        s_sum = 1e10 if np.inf in f else np.sum(f)
        f[~np.isfinite(f)] = 0
        self.matrix[1:, 1:] = self.matrix[1:, 1:] - f
        f2 = np.amin(self.matrix[1:, 1:], keepdims=True, axis=0)
        r_sum = 1e10 if np.inf in f2 else np.sum(f2)
        f2[~np.isfinite(f2)] = 0
        self.matrix[1:, 1:] = self.matrix[1:, 1:] - f2
        h = r_sum + s_sum
        return np.copy(self.matrix), h

    def zero_rating(self) -> Tuple[int, int, int, int]:
        """Функция, реализующая подсчет весов нулей
           Первые два значения - координаты в стандартном массиве
           Вторые два - координаты в массиве в данной итерации"""

        x, y = np.where(self.matrix[1:, 1:] == 0)
        m = self.matrix[1:, 1:]
        d = {}
        for i in range(len(x)):
            row_sort = np.sort(m[:, y[i]])
            str_sort = np.sort(m[x[i], :])
            row_min = row_sort[1]
            str_min = str_sort[1]
            d[(int(self.matrix[1:, 0][x[i]]), int(self.matrix[0][1:][y[i]]), x[i], y[i])] = row_min + str_min
        s = sorted(d, key=lambda k: d[k], reverse=True)
        return s[0]


class Var_edge:
    """Класс для хранения ветвей графа (matrix - Полученная матрица перед дейстивем с графом, h - вес предыдущей мартицы,
     coord_edge - координаты графа, f - флаг, добавили или удалили граф)"""

    def __init__(self, matrix: np.array, h: int, coord_edge: tuple, f: bool):
        self.h = 0
        self.matrix, self.hh, self.coord_edge, self.f = matrix, h, coord_edge, f

    def include_edge_graph(self) -> NoReturn:
        """Добавление ветви"""

        if self.coord_edge[0] in self.matrix[0] and self.coord_edge[1] in self.matrix[1:, 0]:
            y = np.where(self.matrix[0] == self.coord_edge[0])[0]
            x = np.where(self.matrix[:, 0] == self.coord_edge[1])[0]
            self.matrix[x[0]][y[0]] = np.inf
        self.matrix = np.delete(self.matrix, self.coord_edge[2] + 1, axis=0)
        self.matrix = np.delete(self.matrix, self.coord_edge[3] + 1, axis=1)
        self.prep()

    def exclude_edge_graph(self) -> NoReturn:
        """Удаление ветви"""

        self.matrix[self.coord_edge[2] + 1][self.coord_edge[3] + 1] = np.inf
        self.prep()

    def prep(self) -> NoReturn:
        """Функция для просчета H после удаления или добавления"""

        m, self.h = Basic_methods(self.matrix).reduction()
        self.h += self.hh

    def __le__(self, other):
        return self.h <= other.h

    def __lt__(self, other):
        return self.h < other.h


class Main_Method:
    def __init__(self, file_name: str, matrix: np.array, aeroport_id: int, number_bpla: int = 1):
        if len(file_name) != 0:
            mat = Read_Json(file_name)
            ff, self.id = mat.preparation()
            matrix = np.array([i for i in range(np.shape(ff[0])[0] + 1)])
            mm = np.column_stack((np.array([np.array(i) for i in range(1, np.shape(ff[0])[0] + 1)]), ff[0]))
            self.matrix = np.vstack((matrix, mm))
        else:
            self.matrix = matrix
        if number_bpla > 1:
            # start_coord = self.id[aeroport_id]
            self.start_coord = aeroport_id
            self.matrix = self.upd_matr_bpla(self.matrix, self.start_coord, number_bpla)
        self.h = 0
        self.number_bpla = number_bpla
        self.p = True
        self.start_size = np.size(self.matrix[0])
        self.answer = []  # Список с конечным ответом
        self.list_dangling_branches = []  # Список оборванных ветвей
        self.solution = []  # Решение для каждого ребенка дерева

    def upd_matr_bpla(self, matrix: np.array, start_coord: int, number_bpla: int) -> np.array:
        """Добавление копий аэродромов при решении mTSP"""

        m = matrix[:]
        r = np.copy(m[:, start_coord])
        for i in range(1, number_bpla):
            r[0] = int(f'{start_coord}0{i}')
            m = np.column_stack((m, r))
        s = np.copy(m[start_coord])
        for i in range(1, number_bpla):
            s[0] = int(f'{start_coord}0{i}')
            m = np.vstack([m, s])
        return m[:]

    def solution_cycle(self) -> Tuple[list, int]:
        """Основной цикл"""

        while self.p:
            if np.shape(self.matrix)[0] == 3:
                if len(np.where(self.matrix == np.inf)[0]) == 1:
                    self.prep_ans()
                    if self.test_an(self.answer, self.start_size):
                        if self.number_bpla > 1:
                            self.answer = self.mtsp_answer(self.answer)
                        self.p = False
                        continue
                    else:
                        self.upd_branch()
                        continue
                else:
                    self.upd_branch()
                    continue

            base = Basic_methods(self.matrix)
            matr, h = base.reduction()
            coord_edge = base.zero_rating()
            inc = Var_edge(np.copy(matr), h if len(self.solution) == 0 else self.solution[-1].h, coord_edge,
                           True)  # Маршрут с добавлением графа
            inc.include_edge_graph()
            ex = Var_edge(np.copy(matr), h if len(self.solution) == 0 else self.solution[-1].h, coord_edge,
                          False)  # Маршрут с удалением графа
            ex.exclude_edge_graph()
            self.choosing_path(inc, ex)

        return self.answer, self.h

    def choosing_path(self, inc, ex) -> NoReturn:
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
            self.matrix = ex.matrix.copy()
            self.h = ex.h

    def checking_past_paths(self, cl: Var_edge, cl1: Var_edge) -> bool:
        """Проверка на оптимальность в оборванных ветвях"""

        a = sorted(self.list_dangling_branches, key=lambda x: x[0].h)
        for i in range(len(a)):
            if a[i][0] < cl:
                self.list_dangling_branches.append([cl, self.solution[:]])
                self.list_dangling_branches.append([cl1, self.solution[:]])
                self.solution = a[i][1][:]
                self.solution.append(a[i][0])
                self.matrix = a[i][0].matrix.copy()
                self.h = a[i][0].h
                del self.list_dangling_branches[self.list_dangling_branches.index(a[i])]
                return False
        return True

    def prep_ans(self):
        """Формирование ответа при получении матрицы 2X2"""

        mat, self.h = Basic_methods(self.matrix).reduction()
        x, y = np.where(self.matrix[1:, 1:] == np.inf)
        x1, y1 = (x + 1) % 2, y % 2
        x2, y2 = x % 2, (y + 1) % 2
        self.solution.append(
            Var_edge(self.matrix, self.h + self.solution[-1].h,
                     (int(self.matrix[:, 0][x1 + 1]), int(self.matrix[0][y1 + 1])),
                     True))
        self.solution.append(
            Var_edge(self.matrix, self.h + self.solution[-1].h,
                     (int(self.matrix[:, 0][x2 + 1]), int(self.matrix[0][y2 + 1])),
                     True))
        for i in self.solution:
            if i.f:
                self.answer.append(i.coord_edge[:2])
        self.answer = list(map(lambda x: [x[0], x[1]], self.answer))

    def test_an(self, ans: np.array, size: int) -> bool:
        """Проверка: является ли полученный ответ Гамильтоновым циклом"""

        if len(ans) != size - 1:
            return False
        for i in range(len(ans)):
            if ans[i][0] == ans[i][1] or (re.fullmatch(f"{self.start_coord}0*\d*", str(ans[i][0])) and re.fullmatch(
                    f"{self.start_coord}0*\d*", str(ans[i][1]))):
                return False
        v = [ans[0][0]]
        y = ans[0][1]
        for i in range(len(ans)):
            for j in range(len(ans)):
                if ans[j][0] == y:
                    y = ans[j][1]
                    if ans[j][0] not in v:
                        v.append(ans[j][0])
                    elif len(v) != size - 1:
                        return False
        return True

    def transport_mtsp(self, ans: list) -> list:
        for i in range(len(ans)):
            if re.fullmatch(f"{self.start_coord}0*\d*", str(ans[i][0])):
                ans[i][0] = self.start_coord
            if re.fullmatch(f"{self.start_coord}0*\d*", str(ans[i][1])):
                ans[i][1] = self.start_coord
        return ans

    def mtsp_answer(self, ans: list) -> list:
        """Формирование маршрута для нескольких бпла"""
        s_answer = []
        for i in range(len(ans)):
            if re.fullmatch(f"{self.start_coord}0\d*", str(ans[i][0])) or self.start_coord == ans[i][0]:
                s_answer.append(ans[i])
        final_ans = []
        answer = []
        for i in range(len(s_answer)):
            answer.append([self.start_coord, s_answer[i][1]])
            y = s_answer[i][1]
            j = 0
            while True:
                if ans[j][0] == y:
                    answer.append([ans[j][0],
                                   self.start_coord if re.fullmatch(f"{self.start_coord}0\d*", str(ans[j][1])) else
                                   ans[j][1]])
                    y = ans[j][1]
                    j = 0
                    if re.fullmatch(f"{self.start_coord}0\d*", str(y)) or y == self.start_coord:
                        break
                else:
                    j += 1
            final_ans.append(answer[:])
            answer = []
        return final_ans[:]

    def upd_branch(self):
        """Обновление ребра ветвления при получении не гамильтонова цикла"""

        self.answer = []
        a = sorted(self.list_dangling_branches, key=lambda x: x[0].h)
        # self.solution[-1].h = np.inf
        self.list_dangling_branches.append([self.solution[-1], self.solution[:]])
        self.solution = a[0][1][:]
        self.solution.append(a[0][0])
        self.matrix = a[0][0].matrix.copy()
        self.h = a[0][0].h
        del self.list_dangling_branches[self.list_dangling_branches.index(a[0])]


if __name__ == "__main__":
    mat = np.array([[0, 1, 2, 3, 4, 5],
                    [1, np.inf, 4, 5, 7, 5],
                    [2, 8, np.inf, 5, 6, 6],
                    [3, 3, 5, np.inf, 9, 6],
                    [4, 3, 5, 6, np.inf, 2],
                    [5, 6, 2, 3, 8, np.inf]])
    m = Main_Method("", mat, 1, 1)
    print(m.solution_cycle())
