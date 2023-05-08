import pytest

from Littles_method import Basic_methods, Var_edge, Main_Method
import params

class TestBasicOperations:

    def test_first_step_easy(self):
        test1 = Basic_methods(params.arr1.copy())
        mat1, H1 = test1.first_step()
        assert params.equal_matrix(mat1, params.res1[0])
        assert H1 == params.res1[1]

        test2 = Basic_methods(params.arr2.copy())
        mat2, H2 = test2.first_step()
        assert params.equal_matrix(mat2, params.res2[0])
        assert H2 == params.res2[1]

    def test_first_step_normal(self):
        test3 = Basic_methods(params.arr3.copy())
        mat3, H3 = test3.first_step()
        assert params.equal_matrix(mat3, params.res3[0])
        assert H3 == params.res3[1]

        test4 = Basic_methods(params.arr4.copy())
        mat4, H4 = test4.first_step()
        assert params.equal_matrix(mat4, params.res4[0])
        assert H4 == params.res4[1]

        test5 = Basic_methods(params.arr11)
        mat5, H5 = test5.first_step()
        assert params.equal_matrix(mat5, params.res11_1[0])
        assert H5 == params.res11_1[1]


    def test_second_step_easy(self):
        test5 = Basic_methods(params.arr5.copy())
        res = test5.second_step()
        assert res == params.res5

        test6 = Basic_methods(params.arr1.copy())
        res = test6.second_step()
        assert res == params.res6

    def test_second_step_normal(self):
        test7 = Basic_methods(params.arr7.copy())
        res = test7.second_step()
        assert res == params.res7

        test8 = Basic_methods(params.arr8.copy())
        res = test8.second_step()
        assert res == params.res8


class TestVarEdge:

    def test_include_edge_easy(self):
        test9 = Var_edge(params.arr9[0].copy(), params.arr9[1], params.arr9[2], 0)
        test9.include_edge_graph()
        assert test9.h == params.res9

    def test_include_edge_normal(self):
        test10 = Var_edge(params.arr10[0].copy(), params.arr10[1], params.arr10[2], 0)
        test10.include_edge_graph()
        assert test10.h == params.res10_w

    def test_exclude_edge_easy(self):
        test9 = Var_edge(params.arr9[0].copy(), params.arr9[1], params.arr9[2], 0)
        test9.exclude_edge_graph()
        assert test9.h == params.res9

    def test_exclude_edge_normal(self):
        test10 = Var_edge(params.arr10[0].copy(), params.arr10[1], params.arr10[2], 0)
        test10.exclude_edge_graph()
        assert test10.h == params.res10_wo

class TestMain_method:

    @pytest.mark.parametrize('arr, res', [
        [params.arr11, params.res11_2],
        [params.arr12, params.res12],
        [params.arr13, params.res13],
    ])
    def test_littles_method(self, arr, res):
        test1 = Main_Method("", arr, 1)
        sol1 = test1.solution_cycle()[0]
        assert params.equal_sol(sol1, res)

    @pytest.mark.parametrize('matrix, start_coord, number_bpla, res', [
        [params.up_matr1, 4, 4, params.res_up_matr1],
        [params.up_matr2, 5, 3, params.res_up_matr2]
    ])
    def test_upd_matr_bpla(self, matrix, start_coord, number_bpla, res):
        test_u1 = Main_Method("", [], start_coord)
        res_u = test_u1.upd_matr_bpla(matrix, start_coord, number_bpla)
        assert params.equal_matrix(res_u, res)

    @pytest.mark.parametrize('ans, res', [
        [params.tes_g_c1, False],
        [params.test_g_c2, True]
    ])
    def test_hamiltonian_cycle(self, ans, res):
        test_hc = Main_Method("", [], 1)
        res_hc = test_hc.test_an(ans, len(ans))
        assert res_hc == res
