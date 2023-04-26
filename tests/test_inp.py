import numpy as np

from Inp_Rea import Read_Json, CircleTour
import params


class TestReadJson:
    def test_check_intersection(self):
        test2 = Read_Json(params.file_kt_1)
        assert test2.check_intersection(params.arr15[0], params.arr15[1])

    def test_check_with_SVN(self):
        test2 = Read_Json(params.file_kt_1)

        assert test2.check_w_SVN(params.arr16[0][0], params.arr16[0][1]) == params.res16[0]
        assert test2.check_w_SVN(params.arr16[1][0], params.arr16[1][1]) == params.res16[1]
        assert test2.check_w_SVN(params.arr16[2][0], params.arr16[2][1]) == params.res16[2]

    def test_check_with_circle(self):
        test2 = Read_Json(params.file_kt_1)

        assert test2.check_w_circle(params.arr17[0][0], params.arr17[0][1]) == params.res17[0]
        assert test2.check_w_circle(params.arr17[1][0], params.arr17[1][1]) == params.res17[1]

    def test_build_tangent(self):
        test2 = CircleTour(1, 1)
        assert test2.build_tangent(params.arr18[0], params.arr18[1], params.arr18[2]) == params.res18

    def test_calculate_arc_length(self):
        test2 = CircleTour(1, 1)
        assert np.isclose(test2.arc_length(params.arr19[2], params.arr19[3], params.arr19[1]), params.res19, atol=1.0)

    def test_build_circle_detour(self):
        test2 = CircleTour(1, 1)
        test2.build_circle_detour(params.arr20[1], params.arr20[2], params.arr20[3],
                                  params.arr20[0])
        assert test2.tang1 == params.res20[0]
        assert test2.tang2 == params.res20[1]
        assert test2.L == params.res20[2]
