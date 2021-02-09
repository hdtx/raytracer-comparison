include("raytracer.jl")
import .RT: Camera, render, ray_color
using Images

camera = Camera(1600, 900)
save("out.png", render(camera, ray_color))
