import matplotlib.pyplot as plt

from vec3 import Vec3
from raytracer import Camera, Sphere


def bg_color(ray):
    t = (ray.arrow.y() + 1) / 2
    blue = Vec3((.5, .7, 1))
    white = Vec3((1, 1, 1))
    return t * blue + (1 - t) * white


spheres = [
    Sphere(Vec3((0, 0, -1)), .5),
    Sphere(Vec3((0, -500.5, -1)), 500),
]


def ray_color(ray):
    hit = None
    for sphere in spheres:
        new_hit = sphere.hit_test(ray)
        if new_hit.hit and (hit is None or new_hit.t < hit.t):
            hit = new_hit
    if hit:
        full = hit.obj.hit_full(hit)
        factor = 1 if full.front else .5
        return factor * (full.normal + Vec3((1, 1, 1))) / 2
    return bg_color(ray)


def main():
    camera = Camera(1600, 900, msaa=1)
    plt.imsave('out.png', camera.render(ray_color))


if __name__ == '__main__':
    main()
