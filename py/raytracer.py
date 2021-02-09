import numpy as np
import random

from collections import namedtuple
from math import sqrt
from vec3 import Vec3


class Ray:
    def __init__(self, origin: Vec3, arrow: Vec3):
        self.origin = origin
        self.arrow = arrow.unity()


class Camera:
    def __init__(self, scr_w, scr_h, msaa=1):
        random.seed(42)
        self.msaa = msaa
        self.scr_w = scr_w
        self.scr_h = scr_h
        ASPECT_R = self.scr_w / self.scr_h

        VIEW_HH = 1.0
        VIEW_HW = ASPECT_R * VIEW_HH
        self.view_h = VIEW_HH * 2
        self.view_w = VIEW_HW * 2

        self.eye_pos = Vec3((0, 0, 0))
        EYE_DIR = Vec3((0, 0, -1))
        self.eye_up = Vec3((0, 1, 0))
        self.eye_right = EYE_DIR.cross(self.eye_up)

        FOCAL_LEN = 1.0
        VIEW_CENTER = self.eye_pos + EYE_DIR.at_len(FOCAL_LEN)
        self.view_tl = (
            VIEW_CENTER
            + self.eye_up.at_len(VIEW_HH)
            - self.eye_right.at_len(VIEW_HW))

    def get_ray(self, u, v):
        return Ray(
            self.eye_pos,
            self.view_tl
            + self.eye_right.at_len(u * self.view_w)
            - self.eye_up.at_len(v * self.view_h)
            - self.eye_pos)

    def rand():
        return random.randint(-524288, 524288) / 1048575

    def render(self, ray_color_fn, print_progress=True):
        img = np.zeros((self.scr_h, self.scr_w, 3))
        for j in range(self.scr_h):
            if print_progress and j % 100 == 0:
                print('{} of {}'.format(j, self.scr_h))
            v = (j + .5) / self.scr_h
            for i in range(self.scr_w):
                u = (i + .5) / self.scr_w
                if self.msaa == 1:
                    ray = self.get_ray(u, v)
                    col = ray_color_fn(ray)
                else:
                    col = Vec3((0, 0, 0))
                    for k in range(self.msaa):
                        du = Camera.rand() / self.scr_w
                        dv = Camera.rand() / self.scr_h
                        ray = self.get_ray(u + du, v + dv)
                        col += ray_color_fn(ray)
                    col /= self.msaa
                img[j][i] = col.comp
        return img


HitRecordTest = namedtuple('HitRecordTest', ['t', 'hit', 'ray', 'obj'])
HitRecordFull = namedtuple('HitRecordFull', ['front', 'normal', 'point'])


class Hittable:
    def hit_test(self, ray: Ray, tmin=float('-inf'), tmax=float('inf')) -> HitRecordTest:
        return HitRecordTest(None, False, None, None)

    def hit_full(self, hit: HitRecordTest) -> HitRecordFull:
        return HitRecordFull(None, None)


class Sphere(Hittable):
    def __init__(self, center: Vec3, r: Vec3):
        self.center = center
        self.r = r

    def hit_test(self, ray: Ray, tmin=0, tmax=float('inf')) -> HitRecordTest:
        oc = ray.origin - self.center
        half_b = oc.dot(ray.arrow)
        c = oc.dot(oc) - self.r * self.r
        discriminant = half_b * half_b - c
        if discriminant < 0:
            return HitRecordTest(None, False, None, None)
        else:
            sqrtd = sqrt(discriminant)
            root = -half_b - sqrtd
            if not (tmin <= root <= tmax):
                root = -half_b + sqrtd
                if not (tmin <= root <= tmax):
                    return HitRecordTest(None, False, None, None)
            t = root
            return HitRecordTest(t, True, ray, self)

    def hit_full(self, hit: HitRecordTest) -> HitRecordFull:
        p = hit.ray.arrow.at_len(hit.t)
        normal = (p - self.center).unity()
        front = True
        if hit.ray.arrow.dot(normal) > 0:
            front = False
            normal = -normal
        return HitRecordFull(front, normal, p)
