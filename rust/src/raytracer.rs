use crate::vec3::Vec3;

#[derive(Clone)]
pub struct Ray {
    origin: Vec3,
    pub arrow: Vec3,
}

impl Ray {
    fn new(origin: Vec3, arrow: Vec3) -> Self {
        Ray {
            origin,
            arrow: arrow.unity(),
        }
    }
}

pub struct Camera {
    scr_w: usize,
    scr_h: usize,
    msaa: u8,
    view_w: f32,
    view_h: f32,
    eye_pos: Vec3,
    eye_up: Vec3,
    eye_right: Vec3,
    view_tl: Vec3,
}

impl Camera {
    pub fn new(scr_w: usize, scr_h: usize, msaa: u8) -> Self {
        // random.seed(42)
        let aspect_ratio: f32 = (scr_w as f32) / (scr_h as f32);
        let view_hh = 1.0;
        let view_hw = aspect_ratio * view_hh;

        let eye_pos = Vec3::new(0., 0., 0.);
        let eye_dir = Vec3::new(0., 0., -1.);
        let eye_up = Vec3::new(0., 1., 0.);
        let eye_right = eye_dir.cross(eye_up);

        let focal_len = 1.0;
        let view_center = eye_pos + eye_dir.at_len(focal_len);
        let view_tl =
            view_center
            + eye_up.at_len(view_hh)
            - eye_right.at_len(view_hw);

        Self {
            scr_w,
            scr_h,
            msaa,
            view_w: view_hw * 2.,
            view_h: view_hh * 2.,
            eye_pos,
            eye_up,
            eye_right,
            view_tl, 
        }
    }

    fn get_ray(&self, u: f32, v: f32) -> Ray {
        Ray::new(
            self.eye_pos,
            self.view_tl
            + self.eye_right.at_len(u * self.view_w)
            - self.eye_up.at_len(v * self.view_h)
            - self.eye_pos)
        }

    // def rand():
    //     return random.randint(-524288, 524288) / 1048575

    pub fn render<F>(&self, ray_color_fn: &F, print_progress: bool) -> Vec<u32>
            where F: Fn(Ray) -> Vec3 {
        let mut img = vec![0u32; (self.scr_w * self.scr_h) as usize];
        for j in 0..self.scr_h {
            if print_progress && j % 100 == 0 {
                println!("{} of {}", j, self.scr_h);
            }
            let v = ((j as f32) + 0.5) / (self.scr_h as f32);
            for i in 0..self.scr_w {
                let u = ((i as f32) + 0.5) / (self.scr_w as f32);
                let ray = self.get_ray(u, v);
                let col = ray_color_fn(ray);
                img[j * self.scr_w + i] =
                    (((col.z() * 255.) as u32) << 16)
                    | (((col.y() * 255.) as u32) << 8)
                    | ((col.x() * 255.) as u32)
                    | 0xff000000;
            }
        }
        img
    }
}

pub trait Hittable<'a> {
    fn hit_test(&'a self, ray: Ray, tmin: f32, tmax:f32) -> Option<HitRecordTest>;
    fn hit_full(&self, hit: &HitRecordTest) -> HitRecordFull;
}

pub struct HitRecordTest<'a> {
    pub t: f32,
    pub ray: Ray,
    pub obj: &'a dyn Hittable<'a>,
}

pub struct HitRecordFull {
    pub front: bool,
    pub normal: Vec3,
    pub point: Vec3,
}

pub struct Sphere {
    pub center: Vec3,
    pub r: f32,
}

impl<'a> Hittable<'a> for Sphere {
    fn hit_test(&'a self, ray: Ray, tmin: f32, tmax:f32) -> Option<HitRecordTest> {
        let oc = ray.origin - self.center;
        let half_b = oc.dot(ray.arrow);
        let c = oc.dot(oc) - self.r * self.r;
        let discriminant = half_b * half_b - c;

        if discriminant < 0. {
            None
        } else {
            let sqrtd = discriminant.sqrt();
            let mut root = -half_b - sqrtd;
            if root < tmin || root > tmax {
                root = -half_b + sqrtd;
                if root < tmin || root > tmax {
                    return None
                }
            }
            Some(HitRecordTest {
                t: root,
                ray,
                obj: self,
            })
        }
    }

    fn hit_full(&self, hit: &HitRecordTest) -> HitRecordFull {
        let point = hit.ray.arrow.at_len(hit.t);
        let mut normal = (point - self.center).unity();
        let mut front = true;
        if hit.ray.arrow.dot(normal) > 0. {
            front = false;
            normal = -normal;
        } 
        HitRecordFull {
            front,
            normal,
            point,
        }
    }
}
