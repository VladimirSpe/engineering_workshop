import numpy as np

class Commivoyajor:
    def __init__(self, arr):
        self.arr = arr
        self.dags = np.array([])
        self.solution = np.array([])
        self.edge_max_degree = (0, 0)
        self.H = 0
        self.H_w_edge = 0
        self.H2_wo_edge = 0

    def reduction_lines(self):
        lines_min = []
        for i in range(1, len(self.arr)):
            min_iter = min(self.arr[i])
            for k in range(1, len(self.arr[i])):
                self.arr[i][k] -= min_iter
            lines_min.append(min_iter)
        self.H += sum(lines_min)

    def reduction_columns(self):
        self.arr.transpose()
        self.reduction_lines()
        self.arr.transpose()

    def src_max_degree(self):
        max_degree = 0
        index_max = (0, 0)
        for i in range(1, len(self.arr)):
            for j in range(1, len(self.arr[i])):
                if self.arr[i][j] == 0:

                    min_line = min(np.concatenate((self.arr[i][1:j], self.arr[i][j + 1:len(self.arr[i])])))
                    min_column = min(np.concatenate((self.arr[1:i, j], self.arr[i + 1:len(self.arr), j])))
                    if min_column + min_line > max_degree:
                        max_degree = min_line + min_column
                        index_max = i-1, j-1
        self.edge_max_degree = index_max

    def remove_line_and_column(self):
        self.arr = np.delete(self.arr, (self.edge_max_degree[1]+1), axis = 1)
        self.arr = np.delete(self.arr, (self.edge_max_degree[0]+1), axis = 0)
    def compare_solutions(self):
        pass

    def compare_w_daglings(self):
        pass
