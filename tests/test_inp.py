import math
import numpy as np
import pytest
from Inp_Rea import Read_Json, CircleTour, PolygonTour


class TestReadJson:
    @pytest.mark.parametrize('sec1, sec2, res',
                             [([(0, 4), (4, 4)], [(0.5, 6), (2, 0)], True)])
    def test_check_intersection(self, sec1, sec2, res):
        test = Read_Json("file_kt_1.json")
        assert test.check_intersection(sec1, sec2) == res

    @pytest.mark.parametrize('id1, id2, res',
                             [(1004, 1003, True),
                              (1007, 1002, True),
                              (1005, 1006, False)])
    def test_check_with_SVN(self, id1, id2, res):
        test = Read_Json("file_kt_1.json")

        assert test.check_w_SVN(id1, id2) == res

    @pytest.mark.parametrize('A, B, res',
                             [[(27.100201, 100.100201), (30.100101, 40.100101), False],
                              [(14.100201, 80.100201), (100.100101, 13.100101), (True, (45.100101, 44.100101), 11)]])
    def test_check_with_circle(self, A, B, res):
        test = Read_Json("file_kt_1.json")
        assert test.check_w_circle(A, B) == res

    arr18 = [(35.100201, 80.100201), (52.100201, 14.100201), 11]
    res18 = ((41.14470935797548, 13.111665274023988), (62.17000911134637, 18.527272786255885), 68.15423684555495)

    @pytest.mark.parametrize('point, point_circle, R, res',
                             [[(35.100201, 80.100201), (52.100201, 14.100201), 11,
                               ((41.14470935797548, 13.111665274023988), (62.17000911134637, 18.527272786255885),
                                68.15423684555495)]])
    def test_build_tangent(self, point, point_circle, R, res):
        test = CircleTour(1, 1)
        assert test.build_tangent(point, point_circle, R) == res

    @pytest.mark.parametrize('point1, point2, radius, res',
                             [[(2, 2), (4, 2), 1, math.pi]])
    def test_calculate_arc_length(self, point1, point2, radius, res):
        test = CircleTour(1, 1)

        assert np.isclose(test.arc_length(point1, point2, radius), res, atol=1.0)

    @pytest.mark.parametrize('point1, point2, circle_point, r, res',
                             [[(35.100201, 80.100201), (62.17000911134637, 18.527272786255885), (45.100101, 44.100101),
                               11, ((54.36232187203905, 50.0340090307639), (55.828431207269176, 46.52969581473675),
                                    71.92749449898035)]])
    def test_build_circle_detour(self, point1, point2, circle_point, r, res):
        test = CircleTour(1, 1)
        test.build_circle_detour(point1, point2, circle_point, r)
        assert test.tang1 == res[0]
        assert test.tang2 == res[1]
        assert np.isclose(test.L, res[2], atol=0.01)

    @pytest.mark.parametrize('A, B, res',
                             [[(150, 0), (150, 15), False], [(105, 16), (120, 10), True]])
    def test_check_w_polygon(self, A, B, res):
        test = Read_Json("file_kt_1.json")
        assert test.check_w_polygon(A, B) == res

    @pytest.mark.parametrize('A, B, res',
                             [[[(150, 0), (150, 15)], [(105, 16), (120, 10)], None],
                              [[(1, 4), (3, 2)], [(2, 4), (2, 1)], (2.0, 3.0)]])
    def test_line_intersection(self, A, B, res):
        test = PolygonTour(1, 1, 1)
        assert test.line_intersection(A, B) == res

    @pytest.mark.parametrize('A, B, res',
                             [[[(1, 2), (3, 4), (5, 6), (7, 8)], [(0, 0), (10, 10)], True]])
    def test_points_on_same_side(self, A, B, res):
        test = PolygonTour(1, 1, 1)
        assert test.points_on_same_side(A, B) == res

    @pytest.mark.parametrize('A, B, res',
                             [[(0, 0), [(6, 6), (10, 4), (8, 1), (3, 2), (1, 4)], ((8, 1), (1, 4))]])
    def test_build_tangent(self, A, B, res):
        test = PolygonTour(1, 1, 1)
        assert test.build_tangent(A, B) == res

    @pytest.mark.parametrize('p1, p2, points, res',
                             [[(3, 4), (6, 3), [(4, 4), (5, 4), (5, 3), (4, 3)], 3.414213562373095]])
    def test_build_detour(self, p1, p2, points, res):
        test = PolygonTour(p1, p2, points)
        test.build_detour()
        assert np.isclose(test.L, res, atol=0.01)
