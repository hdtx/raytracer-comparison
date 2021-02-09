# Raytracer comparison
Same simple ray-traced image generated from Python, Julia, Rust. Who will win?

No effort on optimization at all -- the idea was to try to be idiomatic in each language and write the thing sort of quickly.

Code based on https://raytracing.github.io/books/RayTracingInOneWeekend.html

Results on my laptop:
```
$:~/projects/raytracer/py$ time python3 run.py 

real    1m1.350s
user    1m1.609s
sys     0m0.640s

$:~/projects/raytracer/julia$ time julia run.jl 

real	0m19.767s
user	0m19.894s
sys	0m0.777s

$:~/projects/raytracer/rust$ time ./target/release/rust

real	0m0.221s
user	0m0.164s
sys	0m0.025s
```
