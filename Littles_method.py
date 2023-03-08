import numpy as np
from Inp_Rea import Read_Json


class Basic_methods:
    def __init__(self, matrix):
        self.matrix = matrix

    def first_step(self):  #Поиск минимумов и удаление их 
        f = np.amin(self.matrix[1:, 1:], keepdims=True, axis=1)
        self.matrix[1:, 1:] = self.matrix[1:, 1:] - np.amin(self.matrix[1:, 1:], keepdims=True, axis=1)
        f2 = np.amin(self.matrix[1:, 1:], keepdims=True, axis=0)
        self.matrix[1:, 1:] = self.matrix[1:, 1:] - np.amin(self.matrix[1:, 1:], keepdims=True, axis=0)
        h = np.sum(f) + np.sum(f2)
        return np.copy(self.matrix), h

    def second_step(self):  #Штука для просчета весов 0
        x, y = np.where(self.matrix[1:, 1:] == 0)
        d = {}
        for i in range(len(x)):
            str_min1 = np.min(self.matrix[1:, 1:][x[i], :][:y[i]]) if len(self.matrix[1:, 1:][x[i], :][:y[i]]) != 0 else np.inf
            str_min2 = np.min(self.matrix[1:, 1:][x[i], 1:][y[i]:]) if len(self.matrix[1:, 1:][x[i], 1:][y[i]:]) != 0 else np.inf
            row_min1 = np.min(self.matrix[1:, 1:][:, y[i]][:x[i]]) if len(self.matrix[1:, 1:][:, y[i]][:x[i]]) != 0 else np.inf
            row_min2 = np.min(self.matrix[1:, 1:][:, y[i]][x[i] + 1:]) if len(
                self.matrix[1:, 1:][:, y[i]][x[i] + 1:]) != 0 else np.inf
            row_min = min(row_min1, row_min2)
            st_min = min(str_min1, str_min2)
            d[(int(self.matrix[1:, 0][x[i]]), int(self.matrix[0][1:][y[i]]), x[i], y[i])] = row_min + st_min
        return sorted(d, key=lambda k: d[k], reverse=True)[0]


class Var_edge:     #Класс для хранения ветвей графа (matrix - Полученная матрица перед дейстивем с графом, h - вес предыдущей мартицы, coord_edge - координаты графа, f - флаг, добавили или удалили граф)
    def __init__(self, matrix, h, coord_edge, f):
        self.h = 0
        self.matrix, self.hh, self.coord_edge, self.f = matrix, h, coord_edge, f

    def include_edge_graph(self):   #Добавление
        if self.coord_edge[0] in self.matrix[0] and self.coord_edge[1] in self.matrix[0][1:]:
            y = np.where(self.matrix[0] == self.coord_edge[0])[0]
            x = np.where(self.matrix[:, 0] == self.coord_edge[1])[0]
            self.matrix[x[0]][y[0]] = np.inf
        self.matrix = np.delete(self.matrix, self.coord_edge[2] + 1, axis=0)
        self.matrix = np.delete(self.matrix, self.coord_edge[3] + 1, axis=1)
        print("include")
        print(self.matrix)
        self.prep()
        print(self.h)

    def exclude_edge_graph(self):       #Удаление
        self.matrix[self.coord_edge[2] + 1][self.coord_edge[3] + 1] = np.inf
        print("exclude")
        print(self.matrix)
        self.prep()
        print(self.h)

    def prep(self):     #Просто вынесено общее для просчета H после удаления или добавления
        m, self.h = Basic_methods(self.matrix).first_step()
        self.h += self.hh

    def __le__(self, other):
        return self.h <= other.h

    def __lt__(self, other):
        return self.h < other.h


class Main_method:
    def __init__(self, file_name, matrix):
        if file_name == 0:
            mat = Read_Json(file_name)
            ff = mat.preparation()            #Получение матрицы и индексов, нам нужна только матрица/ формат возвращаемого значения функции (self.matrix, self.indexes)
            matrix = np.array([i for i in range(np.shape(ff[0])[0] + 1)])         #Эти 3 строки ниже формируют столбец и строку с индексами, тоже желательно протестить
            mm = np.column_stack((np.array([np.array(i) for i in range(1, np.shape(ff[0])[0] + 1)]), ff[0]))
            self.matrix = np.vstack((matrix, mm))
        else:
            self.matrix = matrix
        self.h = 0
        self.answer = []    #Список с конечным ответом
        self.list_dangling_branches = []    #Список оборванных ветвей
        self.solution = []  #Решение для каждого ребенка дерева

    def solution_cycle(self):           #Основной цикл
        while np.shape(self.matrix)[0] != 3:
            print("Solution")
            for i in self.solution:
                print(i.coord_edge[:2], i.f, end=" ")
                print()
            print("------------------")
            print("Die")
            for i in self.list_dangling_branches:
                print(i[0].coord_edge[:2], i[0].f, end=" ")
                print()
            print("------------------")
            base = Basic_methods(self.matrix)
            matr, h = base.first_step()
            coord_edge = base.second_step()
            inc = Var_edge(matr.copy(), h if len(self.solution) == 0 else self.solution[-1].h, coord_edge, True)    #Маршрут с добавлением графа
            inc.include_edge_graph()
            ex = Var_edge(matr.copy(), h if len(self.solution) == 0 else self.solution[-1].h, coord_edge, False)    #Маршрут с удалением графа
            ex.exclude_edge_graph()
            print(self.matrix)
            print(coord_edge)
            self.choosing_path(inc, ex)
        mat, self.h = Basic_methods(self.matrix).first_step()   #Формирование ответа после получения матрицы 2х2
        self.h += self.solution[-1].h
        self.solution.append(Var_edge(self.matrix, self.h + self.solution[-1].h, (self.matrix[:, 0][-1], self.matrix[0][1]), True))
        self.solution.append(Var_edge(self.matrix, self.h + self.solution[-1].h, (self.matrix[:, 0][1], self.matrix[0][2]), True))
        print(self.h)
        for i in self.solution:
            if i.f:
                self.answer.append(i.coord_edge[:2])
        return self.answer, self.h

    def choosing_path(self, inc, ex):   #Функция для выбора оптимального дерева (с графом или без)
        if inc <= ex:
            if self.checking_past_paths(inc, ex):
                self.list_dangling_branches.append([ex, self.solution[:]])
                self.solution.append(inc)
                self.matrix = inc.matrix.copy()
                self.h = inc.h
                print("---------------------")
                print(True)
                print()

        elif self.checking_past_paths(ex, inc):
            self.list_dangling_branches.append([inc, self.solution[:]])
            self.solution.append(ex)
            self.matrix = inc.matrix.copy()
            self.h = inc.h
            print(False)
            print("---------------------")
            print()

    def checking_past_paths(self, cl, cl1):     #Проверка на оптимальность в оборванных ветвях
        for i in range(len(self.list_dangling_branches)):
            if self.list_dangling_branches[i][0] < cl:
                self.solution = self.list_dangling_branches[i][1][:]
                self.solution.append(self.list_dangling_branches[i][0])
                self.matrix = self.list_dangling_branches[i][0].matrix.copy()
                self.h = self.list_dangling_branches[i][0].h
                del self.list_dangling_branches[i]
                self.list_dangling_branches.append([cl, self.solution[:]])
                self.list_dangling_branches.append([cl1, self.solution[:]])
                return False
        return True


if __name__ == "__main__":
    m = Main_method("pp", 0)
    m.solution_cycle()
