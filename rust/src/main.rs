mod vec3;
use vec3::Vec3;

mod raytracer;
use raytracer::{Camera, Hittable, HitRecordFull, HitRecordTest, Ray, Sphere};
use png_encode_mini::write_rgba_from_u32;

use std::fs::File;
use std::path::Path;

fn write_png(data: &mut Vec<u32>, w: usize, h: usize) {
    // Flip vertically
    for i in 0..(h / 2) {
        let l0 = w * i;
        let r1 = w * (h - i);
        let sl = &mut data[l0..r1];
        let (left, right) = sl.split_at_mut(w);
        let start = right.len() - w;
        left.swap_with_slice(&mut right[start..]);
    }
    let path = Path::new("out.png");
    let mut file = File::create(&path).unwrap();
    write_rgba_from_u32(&mut file, data, w as u32, h as u32).unwrap();
}

fn bg_color(ray: &Ray) -> Vec3 {
    let t = (ray.arrow.y() + 1.) / 2.;
    let blue = Vec3::new(0.5, 0.7, 1.);
    let white = Vec3::new(1., 1., 1.);
    t * blue + (1. - t) * white
}

fn ray_color<'a>(ray: Ray, objs: &'a Vec<&dyn Hittable<'a>>) -> Vec3 {
    let mut hit: Option<HitRecordTest> = None;
    for obj in objs {
        if let Some(new_hit) = obj.hit_test(ray.clone(), 0., 1000.) {
            hit = match hit {
                Some(old_hit) =>
                    if new_hit.t < old_hit.t {
                        Some(new_hit)
                    } else {
                        Some(old_hit)
                    },
                None => Some(new_hit),
            };
        }
    }
    if let Some(h) = hit {
        let full = h.obj.hit_full(&h);
        let factor = if full.front { 1. } else { 0.5 };
        factor * (full.normal + Vec3::new(1., 1., 1.)) / 2.
    } else {
        bg_color(&ray)
    }
}

fn main() {
    let mut objs: Vec<&dyn Hittable> = Vec::new();
    let s1 = Sphere { center: Vec3::new(0., 0., -1.), r: 0.5 };
    let s2 = Sphere { center: Vec3::new(0., -500.5, -1.), r: 500. };
    objs.push(&s1);
    objs.push(&s2);
    let cl = |x: Ray| ray_color(x, &objs);
    let camera = Camera::new(1600, 900, 1);
    let mut data = camera.render(&cl, false);
    write_png(&mut data, 1600, 900);
    // println!("{:?}", data);
}
