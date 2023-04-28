import math
import numpy as np
import pytest
from Inp_Rea import Read_Json, CircleTour


class TestReadJson:
    @pytest.mark.parametrize('sec1, sec2, res',
                             [([(0, 4), (4, 4)], [(0.5, 6), (2, 0)], True)])
    def test_check_intersection(self, sec1, sec2, res):
        test2 = Read_Json("file_kt_1.json")
        assert test2.check_intersection(sec1, sec2) == res

    @pytest.mark.parametrize('id1, id2, res',
                             [(1004, 1003, True),
                              (1007, 1002, True),
                              (1005, 1006, False)])
    def test_check_with_SVN(self, id1, id2, res):
        test2 = Read_Json("file_kt_1.json")

        assert test2.check_w_SVN(id1, id2) == res

    @pytest.mark.parametrize('A, B, res',
                             [[(27.100201, 100.100201), (30.100101, 40.100101), False],
                              [(14.100201, 80.100201), (100.100101, 13.100101), (True, (45.100101, 44.100101), 11)]])
    def test_check_with_circle(self, A, B, res):
        test2 = Read_Json("file_kt_1.json")
        assert test2.check_w_circle(A, B) == res

    arr18 = [(35.100201, 80.100201), (52.100201, 14.100201), 11]
    res18 = ((41.14470935797548, 13.111665274023988), (62.17000911134637, 18.527272786255885), 68.15423684555495)

    @pytest.mark.parametrize('point, point_circle, R, res',
                             [[(35.100201, 80.100201), (52.100201, 14.100201), 11,
                               ((41.14470935797548, 13.111665274023988), (62.17000911134637, 18.527272786255885),
                                68.15423684555495)]])
    def test_build_tangent(self, point, point_circle, R, res):
        test2 = CircleTour(1, 1)
        assert test2.build_tangent(point, point_circle, R) == res

    @pytest.mark.parametrize('point1, point2, radius, res',
                             [[(2, 2), (4, 2), 1, math.pi]])
    def test_calculate_arc_length(self, point1, point2, radius, res):
        test2 = CircleTour(1, 1)

        assert np.isclose(test2.arc_length(point1, point2, radius), res, atol=1.0)

    @pytest.mark.parametrize('point1, point2, circle_point, r, res',
                             [[(35.100201, 80.100201), (62.17000911134637, 18.527272786255885), (45.100101, 44.100101),
                               11, ((54.36232187203905, 50.0340090307639), (55.828431207269176, 46.52969581473675),
                                    71.92749449898035)]])
    def test_build_circle_detour(self, point1, point2, circle_point, r, res):
        test2 = CircleTour(1, 1)
        test2.build_circle_detour(point1, point2, circle_point, r)
        assert test2.tang1 == res[0]
        assert test2.tang2 == res[1]
        assert test2.L == res[2]
