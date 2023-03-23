from Inp_Rea import Read_Json
import params


class TestReadJson:

    def test_initialize(self):
        test1 = Read_Json(params.file_kt_1, params.file_zd_1)
        test1.find_cords_by_name()
        assert test1.SVN_cords == params.res_file

    def test_check_intersection(self):
        test2 = Read_Json(params.file_kt_1, params.file_zd_1)
        assert test2.check_intersection(params.arr15[0], params.arr15[1])

    def test_all(self):
        test1 = Read_Json(params.file_kt_1, params.file_zd_1)
        res = test1.preparation()
        assert params.equal_matrix(res, params.res15)
