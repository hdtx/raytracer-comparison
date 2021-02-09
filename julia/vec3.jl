module V3

using LinearAlgebra
import Base.:(==)
import Base.+
import Base.-
import Base.*
import Base./
import Base.isapprox
import Base.iterate

struct Vec3
    comp::Vector{Float64}
end

x(a::Vec3) = a.comp[1]
y(a::Vec3) = a.comp[2]
z(a::Vec3) = a.comp[3]
Base.iterate(a::Vec3; kwargs...) = Base.iterate(a.comp; kwargs...)
==(a::Vec3, b::Vec3) = a.comp == b.comp
+(a::Vec3, b::Vec3) = Vec3(a.comp + b.comp)
-(a::Vec3, b::Vec3) = Vec3(a.comp - b.comp)
-(a::Vec3) = Vec3(-a.comp)
*(a::Vec3, b::Number) = Vec3(a.comp * b)
/(a::Vec3, b::Number) = Vec3(a.comp / b)
LinearAlgebra.dot(a::Vec3, b::Vec3) = a.comp ⋅ b.comp
LinearAlgebra.cross(a::Vec3, b::Vec3) = Vec3(a.comp × b.comp)
LinearAlgebra.norm(a::Vec3) = norm(a.comp)
isapprox(a::Vec3, b::Vec3; kwargs...) = isapprox(a.comp, b.comp; kwargs...)
LinearAlgebra.normalize(a::Vec3) = Vec3(normalize(a.comp))
at_len(a::Vec3, b::Number) = normalize(a) * b

end # module V3
