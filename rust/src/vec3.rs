use std::cmp::PartialEq;
use std::ops;

#[derive(Debug, Clone, Copy)]
pub struct Vec3 {
    x: f32,
    y: f32,
    z: f32,
}

impl Vec3 {
    pub fn new(x: f32, y: f32, z: f32) -> Self {
        Vec3 { x, y, z }
    }

    pub fn x(self) -> f32 {
        self.x
    }

    pub fn y(self) -> f32 {
        self.y
    }

    pub fn z(self) -> f32 {
        self.z
    }

    pub fn dot(self, other: Vec3) -> f32 {
        self.x * other.x + self.y * other.y + self.z * other.z
    }

    pub fn cross(self, other: Vec3) -> Vec3 {
        let a = self;
        let b = other;
        Vec3 {
            x: a.y * b.z - a.z * b.y,
            y: a.z * b.x - a.x * b.z,
            z: a.x * b.y - a.y * b.x,
        }
    }

    pub fn norm(&self) -> f32 {
        (self.x * self.x + self.y * self.y + self.z * self.z).sqrt()
    }

    pub fn compare(self, other: Vec3, tol: f32) -> bool {
        (self - other).norm() < tol.abs()
    }

    pub fn unity(&self) -> Vec3 {
        *self / self.norm()
    }

    pub fn at_len(self, t: f32) -> Vec3 {
        self.unity() * t
    }
}

impl PartialEq for Vec3 {
    fn eq(&self, other: &Self) -> bool {
        self.x == other.x && self.y == other.y && self.z == other.z
    }
}

impl ops::Add for Vec3 {
    type Output = Self;

    fn add(self, other: Self) -> Self {
        Self {
            x: self.x + other.x,
            y: self.y + other.y,
            z: self.z + other.z,
        }
    }
}

impl ops::Sub for Vec3 {
    type Output = Self;

    fn sub(self, other: Self) -> Self {
        Self {
            x: self.x - other.x,
            y: self.y - other.y,
            z: self.z - other.z,
        }
    }
}

impl ops::Neg for Vec3 {
    type Output = Self;

    fn neg(self) -> Self {
        Self {
            x: -self.x,
            y: -self.y,
            z: -self.z,
        }
    }
}

impl ops::Mul<f32> for Vec3 {
    type Output = Self;

    fn mul(self, other: f32) -> Self {
        Self {
            x: other * self.x,
            y: other * self.y,
            z: other * self.z,
        }
    }
}

impl ops::Mul<Vec3> for f32 {
    type Output = Vec3;

    fn mul(self, other: Vec3) -> Vec3 {
        Vec3 {
            x: self * other.x,
            y: self * other.y,
            z: self * other.z,
        }
    }
}

impl ops::Div<f32> for Vec3 {
    type Output = Self;

    fn div(self, other: f32) -> Self {
        Self {
            x: self.x / other,
            y: self.y / other,
            z: self.z / other,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_eq() {
        assert_eq!(Vec3::new(1., 2., 3.), Vec3::new(1., 2., 3.));
    }

    #[test]
    fn test_add() {
        assert_eq!(
            Vec3::new(1., 2., 3.) + Vec3::new(4., 5., 6.),
            Vec3::new(5., 7., 9.)
        );
    }

    #[test]
    fn test_sub() {
        assert_eq!(
            Vec3::new(5., 7., 9.) - Vec3::new(4., 5., 6.),
            Vec3::new(1., 2., 3.)
        );
    }

    #[test]
    fn test_neg() {
        assert_eq!(-Vec3::new(1., 2., 3.), Vec3::new(-1., -2., -3.));
    }

    #[test]
    fn test_mul() {
        assert_eq!(Vec3::new(1., 2., 3.) * 2., Vec3::new(2., 4., 6.));
        assert_eq!(2. * Vec3::new(1., 2., 3.), Vec3::new(2., 4., 6.));
    }

    #[test]
    fn test_div() {
        assert_eq!(Vec3::new(2., 4., 6.) / 2., Vec3::new(1., 2., 3.));
    }

    #[test]
    fn test_dot() {
        assert_eq!(Vec3::new(1., 2., 3.).dot(Vec3::new(7., 6., 5.)), 34.);
    }

    #[test]
    fn test_cross() {
        assert_eq!(
            Vec3::new(1., 0., 0.).cross(Vec3::new(0., 1., 0.)),
            Vec3::new(0., 0., 1.)
        );
    }

    #[test]
    fn test_norm() {
        assert_eq!(Vec3::new(9., 12., 112.).norm(), 113.);
    }

    #[test]
    fn test_unity() {
        assert!(
            Vec3::new(3., 4., 5.).unity().compare(
                Vec3::new(0.424, 0.566, 0.707),
                0.001));
    }
}
