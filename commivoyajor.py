import numpy as np


class Commivoyajor:
    def __init__(self, arr):
        # arr must be with indexes, like 0 1 2 3
        #                                1 M 7 9
        #                                2 3 M 0
        #                                3 5 2 M
        self.arr = arr
        self.solution = np.array([])
        # coordinats of edge with max degree
        self.edge_max_degree = (0, 0)
        # first H
        self.H = self.reduction_lines_columns(arr)
        # H of the matrix of which we are now using
        self.H_now = 0
        # H, when we have any edge
        self.H_w_edge = 0
        # H, when we haven't any edge
        self.H_wo_edge = 0
        # Our plan, like X1, X2 ...
        self.plans = []

    def reduction_lines_columns(self, arr):
        lines_min = []
        columns_min = []
        sum_lines = 0
        sum_columns = 0
        # lines
        for i in range(1, len(arr)):
            min_iter = min(arr[i, 1:])
            # print(min_iter)
            for k in range(1, len(arr[i])):
                arr[i][k] -= min_iter
            lines_min.append(min_iter)
        sum_lines = sum(lines_min)
        # columns
        arr.transpose()
        for i in range(1, len(arr)):
            min_iter = min(arr[i, 1:])
            for k in range(1, len(arr[i])):
                arr[i][k] -= min_iter
            columns_min.append(min_iter)
        sum_columns = sum(columns_min)
        arr.transpose()

        return sum_lines + sum_columns

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
                        index_max = int(self.arr[i][0]) - 1, int(self.arr[0][j]) - 1
        self.edge_max_degree = index_max

    # doing plan without any edge
    def plan_wo_edge(self):
        arr_plan = self.arr
        arr_plan[self.edge_max_degree[0] + 1, self.edge_max_degree[1] + 1] = np.inf
        self.H_wo_edge = self.H + self.reduction_lines_columns(arr_plan)
        return arr_plan

    # doing plan with any edge
    def plan_w_edge(self):
        arr_plan = self.arr
        arr_plan = np.delete(self.arr, (self.edge_max_degree[1] + 1), axis=1)
        arr_plan = np.delete(self.arr, (self.edge_max_degree[0] + 1), axis=0)
        arr_plan[self.edge_max_degree[1] + 1][self.edge_max_degree[0] + 1] = np.inf
        self.H_w_edge = self.H + self.reduction_lines_columns(arr_plan)
        return arr_plan

    # compare solutions with edge and without edge
    def compare_solutions(self):
        arr_w_edge = self.plan_w_edge()
        arr_wo_edge = self.plan_wo_edge()
        if self.H_wo_edge > self.H_w_edge:
            self.arr = arr_w_edge
            self.H_now = self.H_w_edge
            self.plans.append([self.H_wo_edge, arr_wo_edge])
        else:
            self.arr = arr_wo_edge
            self.H_now = self.H_wo_edge
            self.plans.append([self.H_w_edge, arr_w_edge])

    def compare_w_daglings(self):
        # ?
        '''
        arr_w_edge = self.plan_w_edge()
        arr_wo_edge = self.plan_wo_edge()
        for i in self.plans:
            if i[0] < self.H_now:
                self.arr = arr_w_edge
                self.H_now = self.H_w_edge
                self.plans.append([self.H_wo_edge, arr_wo_edge])
        '''


array = np.array([[0, 1, 2, 3, 4, 5],
                  [1, np.inf, 20, 18, 12, 8],
                  [2, 5, np.inf, 14, 7, 11],
                  [3, 12, 18, np.inf, 6, 11],
                  [4, 11, 17, 11, np.inf, 12],
                  [5, 5, 5, 5, 5, np.inf]])
a = Commivoyajor(array)
