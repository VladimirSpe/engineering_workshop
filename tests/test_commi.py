import pytest

from Littles_method import Basic_methods, Var_edge, Main_Method
import params

class TestBasicOperations:

    @pytest.mark.parametrize('arr, res', [
        [params.arr1, params.res1],
        [params.arr2, params.res2],
        [params.arr3, params.res3],
        [params.arr4, params.res4],
        [params.arr11, params.res11_1]
    ])
    def test_reduction(self, arr, res):
        test1 = Basic_methods(arr.copy())
        mat1, H1 = test1.reduction()
        assert params.equal_matrix(mat1, res[0])
        assert H1 == res[1]

    @pytest.mark.parametrize('arr, res', [
        [params.arr5, params.res5],
        [params.arr1, params.res6],
        [params.arr7, params.res7],
        [params.arr8, params.res8]
    ])
    def test_zero_rating(self, arr, res):
        test5 = Basic_methods(params.arr5.copy())
        res = test5.zero_rating()
        assert res == params.res5


class TestVarEdge:

    @pytest.mark.parametrize('arr, res', [
        [params.arr9, params.res9],
        [params.arr10, params.res10_w],
    ])
    def test_include_edge_easy(self, arr, res):
        test9 = Var_edge(arr[0].copy(), arr[1], arr[2], False)
        test9.include_edge_graph()
        assert test9.h == res

    @pytest.mark.parametrize('arr, res', [
        [params.arr9, params.res9],
        [params.arr10, params.res10_wo]
    ])
    def test_exclude_edge_easy(self, arr, res):
        test9 = Var_edge(arr[0].copy(), arr[1], arr[2], False)
        test9.exclude_edge_graph()
        assert test9.h == res


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

    @pytest.mark.parametrize('arr, res', [
        [params.test_m_a1, params.res_m_a1]
    ])
    def test_mtsp_answer(self, arr, res):
        test_ma = Main_Method("", [], 1)
        test_ma.start_coord = 4
        test_ma.number_bpla = 3
        res_ma = test_ma.mtsp_answer(arr)
        assert params.equal_sol(res_ma, res)