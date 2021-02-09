module RT

include("vec3.jl")
import .V3: Vec3, at_len, x, y, z

using LinearAlgebra
using Images

struct Ray
    origin::Vec3
    arrow::Vec3
    Ray(o::Vec3, a::Vec3) = new(o, normalize(a))
end

struct Camera
    scr_w::UInt16
    scr_h::UInt16
    view_w::Float64
    view_h::Float64
    eye_pos::Vec3
    eye_up::Vec3
    eye_right::Vec3
    view_tl::Vec3
end

function Camera(scr_w, scr_h)
    ASPECT_R = scr_w / scr_h
    VIEW_HH = 1.0
    VIEW_HW = ASPECT_R * VIEW_HH
    view_h = VIEW_HH * 2
    view_w = VIEW_HW * 2

    eye_pos = Vec3([0, 0, 0])
    EYE_DIR = Vec3([0, 0, -1])
    eye_up = Vec3([0, 1, 0])
    eye_right = EYE_DIR × eye_up

    FOCAL_LEN = 1.0
    VIEW_CENTER = eye_pos + at_len(EYE_DIR, FOCAL_LEN)
    view_tl = VIEW_CENTER + at_len(eye_up, VIEW_HH) - at_len(eye_right, VIEW_HW)

    Camera(scr_w, scr_h, view_w, view_h, eye_pos, eye_up, eye_right, view_tl)
end

get_ray(self::Camera, u, v) =
    Ray(
        self.eye_pos,
        self.view_tl
        + at_len(self.eye_right, u * self.view_w)
        - at_len(self.eye_up, v * self.view_h)
        - self.eye_pos
    )

function render(self::Camera, ray_color_fn, print_progress=true)
    img = zeros(RGB, self.scr_h, self.scr_w)
    for j in 1:self.scr_h
        if print_progress && j % 100 == 0
            println("$j of $(self.scr_h)")
        end
        v = (j - .5) / self.scr_h
        for i in 1:self.scr_w
            u = (i - .5) / self.scr_w
            ray = get_ray(self, u, v)
            img[j, i] = ray_color_fn(ray)
        end
    end
    img
end

abstract type Hittable end

struct HitRecordTest
    t::Float64
    ray::Ray
    obj::Hittable
end

struct HitRecordFull
    front::Bool
    normal::Vec3
    point::Vec3
end

struct Sphere <: Hittable
    center::Vec3
    r::Float64
end

function hit_test(self::Sphere, ray::Ray, tmin=0, tmax=Inf)::Union{HitRecordTest, Nothing}
    oc = ray.origin - self.center
    half_b = oc ⋅ ray.arrow
    c = oc ⋅ oc - self.r^2
    Δ = half_b^2 - c
    if Δ < 0
        return nothing
    else
        sΔ = sqrt(Δ)
        root = -half_b - sΔ
        if root < tmin || root > tmax
            root = -half_b + sΔ
            if root < tmin || root > tmax
                return nothing
            end
        end
        return HitRecordTest(root, ray, self)
    end
end

function hit_full(self::Sphere, hit::HitRecordTest)::HitRecordFull
    p = at_len(hit.ray.arrow, hit.t)
    normal = normalize(p - self.center)
    front = true
    if hit.ray.arrow ⋅ normal > 0
        front = false
        normal = -normal
    end
    HitRecordFull(front, normal, p)
end

function bg_color(ray::Ray)::RGB
    t = (y(ray.arrow) + 1) / 2
    blue = RGB(.5, .7, 1)
    white = RGB(1, 1, 1)
    t * blue + (1 - t) * white
end

spheres = [
    Sphere(Vec3([0, 0, -1]), .5),
    Sphere(Vec3([0, -500.5, -1]), 500),
]

function ray_color(ray::Ray)::RGB
    hit = nothing
    for sphere in spheres
        new_hit = hit_test(sphere, ray)
        if !isnothing(new_hit) && (isnothing(hit) || new_hit.t < hit.t)
            hit = new_hit
        end
    end
    if !isnothing(hit)
        full = hit_full(hit.obj, hit)
        factor = full.front ? 1 : .5
        col = (full.normal + Vec3([1, 1, 1])) * factor / 2
        RGB(x(col), y(col), z(col))
    else
        bg_color(ray)
    end
end

end # module RT
