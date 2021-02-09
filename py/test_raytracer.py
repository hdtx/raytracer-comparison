import pytest
from vec3 import Vec3

class TestVec3:
    def test_components(self):
        v = Vec3((1, 2, 3))
        assert v.x() == 1
        assert v.y() == 2
        assert v.z() == 3

    def test_eq_equal(self):
        assert Vec3((1, 2, 3)) == Vec3((1, 2, 3))

    def test_eq_different(self):
        assert Vec3((1, 2, 3)) != Vec3((3, 2, 1))

    def test_eq_int_raises(self):
        with pytest.raises(NotImplementedError):
            Vec3((1, 2, 3)) == 1

    def test_sum_ok(self):
        assert Vec3((1, 2, 3)) == Vec3((0, 1, 2)) + Vec3((1, 1, 1))

    def test_sum_wrong(self):
        assert Vec3((1, 2, 3)) != Vec3((10, 1, 2)) + Vec3((1, 1, 1))

    def test_sum_int_raises(self):
        with pytest.raises(NotImplementedError):
            Vec3((1, 2, 3)) + 1

    def test_neg_ok(self):
        assert -Vec3((1, 2, 3)) == Vec3((-1, -2, -3))

    def test_sub_ok(self):
        assert Vec3((7, 6, 5)) - Vec3((1, 2, 3)) == Vec3((6, 4, 2))

    def test_sub_wrong(self):
        assert Vec3((7, 6, 5)) - Vec3((3, 2, 1)) != Vec3((6, 4, 2))

    def test_sub_int_raises(self):
        with pytest.raises(NotImplementedError):
            Vec3((1, 2, 3)) - 1

    def test_mul_int_ok(self):
        assert Vec3((7, 6, 5)) * 2 == Vec3((14, 12, 10))

    def test_mul_int_wrong(self):
        assert Vec3((7, 6, 5)) * 3 != Vec3((14, 12, 10))

    def test_mul_float_ok(self):
        assert Vec3((7, 6, 5)) * 2. == Vec3((14., 12., 10.))

    def test_mul_float_wrong(self):
        assert Vec3((7, 6, 5)) * 3. != Vec3((14., 12., 10.))

    def test_mul_Vec3_raises(self):
        with pytest.raises(NotImplementedError):
            Vec3((1, 2, 3)) * Vec3((1, 2, 3))

    def test_rmul_float_ok(self):
        assert 2. * Vec3((7, 6, 5)) == Vec3((14., 12., 10.))

    def test_div_int_ok(self):
        assert Vec3((7, 6, 5)) / 2 == Vec3((3.5, 3, 2.5))

    def test_div_int_wrong(self):
        assert Vec3((7, 6, 5)) / 3 != Vec3((3.5, 3, 2.5))

    def test_div_float_ok(self):
        assert Vec3((7, 6, 5)) / 2. == Vec3((3.5, 3, 2.5))

    def test_div_float_wrong(self):
        assert Vec3((7, 6, 5)) / 3. != Vec3((3.5, 3, 2.5))

    def test_div_Vec3_raises(self):
        with pytest.raises(NotImplementedError):
            Vec3((1, 2, 3)) / Vec3((1, 2, 3))

    def test_dot_ok(self):
        assert Vec3((7, 6, 5)).dot(Vec3((1, 2, 3))) == 34

    def test_dot_int_raises(self):
        with pytest.raises(NotImplementedError):
            Vec3((1, 2, 3)).dot(1)

    def test_cross_ok(self):
        assert Vec3((1, 0, 0)).cross(Vec3((0, 1, 0))) == Vec3((0, 0, 1))

    def test_cross_wrong(self):
        assert Vec3((0, 1, 0)).cross(Vec3((1, 0, 0))) != Vec3((0, 0, 1))

    def test_cross_int_raises(self):
        with pytest.raises(NotImplementedError):
            Vec3((1, 2, 3)).cross(1)

    def test_compare_ok(self):
        assert Vec3((3, 4, 5)).compare(Vec3((3.01, 4.01, 5.01)), .1)

    def test_compare_wrong(self):
        assert not Vec3((3, 4, 5)).compare(Vec3((3.01, 4.01, 5.01)), .01)

    def test_norm_ok(self):
        assert Vec3((9, 12, 112)).norm() == 113

    def test_unity_ok(self):
        assert Vec3((3, 4, 5)).unity().compare(Vec3((.424, .566, .707)), .001)

    def test_at_len_ok(self):
        assert Vec3((9, 12, 112)).at_len(226) == Vec3((18, 24, 224))

    def test_abs_ok(self):
        assert Vec3((-1, 2, -3)).abs() == Vec3((1, 2, 3))
