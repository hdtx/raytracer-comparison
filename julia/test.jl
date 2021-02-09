include("vec3.jl")
import .V3: Vec3, at_len

using LinearAlgebra
using Test

# ==
@test Vec3([1, 2, 3]) == Vec3([1, 2, 3])
@test Vec3([1, 2, 3]) != Vec3([10, 2, 3])
# +
@test Vec3([1, 2, 3]) + Vec3([4, 5, 6]) == Vec3([5, 7, 9])
@test Vec3([1, 2, 3]) + Vec3([4, 5, 6]) != Vec3([6, 8, 9])
# -
@test Vec3([9, 8, 7]) - Vec3([4, 5, 6]) == Vec3([5, 3, 1])
@test Vec3([9, 8, 7]) - Vec3([4, 5, 6]) != Vec3([2, 3, 1])
# - (unary)
@test -Vec3([9, 8, 7]) == Vec3([-9, -8, -7])
@test -Vec3([9, 8, 7]) != Vec3([-2, -8, -7])
# *
@test Vec3([9, 8, 7]) * 2 == Vec3([18, 16, 14])
@test Vec3([9, 8, 7]) * 3 != Vec3([18, 16, 14])
# /
@test Vec3([9, 12, 15]) / 3 == Vec3([3, 4, 5])
@test Vec3([9, 12, 15]) / 2 != Vec3([3, 4, 5])
# ⋅
@test Vec3([7, 6, 5]) ⋅ Vec3([1, 2, 3]) == 34
@test Vec3([7, 6, 5]) ⋅ Vec3([1, 2, 3]) != 35
# ×
@test Vec3([1, 0, 0]) × Vec3([0, 1, 0]) == Vec3([0, 0, 1])
@test Vec3([1, 0, 0]) × Vec3([0, -1, 0]) != Vec3([0, 0, 1])
# norm
@test norm(Vec3([9, 12, 112])) == 113
@test norm(Vec3([9, 2, 112])) != 113
# ≈
@test Vec3([3, 4, 5]) ≈ Vec3([3.00000001, 4.00000001, 5.00000001])
@test Vec3([3, 4, 5]) ≉ Vec3([3.0000001, 4.0000001, 5.0000001])
# normalize
@test normalize(Vec3([3, 4, 5])) ≈ Vec3([0.42426407, 0.56568543, 0.70710678])
@test normalize(Vec3([3, 4, 5])) ≉ Vec3([0.4242647, 0.5656853, 0.7071068])
# at_len
@test at_len(Vec3([9, 12, 112]), 226) == Vec3([18, 24, 224])
@test at_len(Vec3([9, 12, 112]), 225) != Vec3([18, 24, 224])
