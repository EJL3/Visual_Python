from vpython import *

R = 4e11
scene.background = color.black
scene.width = scene.height = 700
scene.range = 2.5*R
scene.caption= """To rotate "camera", drag with right button.
To zoom, use scroll wheel.
  On a two-button mouse, middle is left + right.
To pan left/right and up/down, Shift-drag.
Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""

s1 = sphere(pos=vector(0, R, 0), radius=1e10, color=color.magenta, make_trail=True, emissive=True)
s2 = sphere(pos=vector(0, -R, 0), radius=1e10, color=color.blue, make_trail=True, emissive=True)
s3 = sphere(pos=vector(2*R, 0, 0), radius=1e10, color=color.orange, make_trail=True, emissive=True)
s1.m = 5e30
s2.m = 5e30
s3.m = 5e30*1e-1
G = 6.7e-11
v = sqrt(G*s1.m/(4*R))
s1.p = s1.m*vector(0,0,-v)
s2.p = s2.m*vector(0,0,v)
s3.p = vector(0,0,0)
dt = 60*1000
t = 0
while True:
    rate(200)
    r21 = s2.pos - s1.pos
    F21 = -norm(r21)*G*s1.m*s2.m/mag(r21)**2
    r32 = s3.pos - s2.pos
    F32 = -norm(r32)*G*s3.m*s2.m/mag(r32)**2
    r31= s3.pos - s1.pos
    F31 = -norm(r31)*G*s3.m*s1.m/mag(r31)**2
    s3.p = s3.p + (F32+F31)*dt
    s2.p = s2.p + (F21-F32)*dt
    s1.p = s1.p + (-F21-F31)*dt
    s1.pos = s1.pos + (s1.p/s1.m)*dt
    s2.pos = s2.pos + (s2.p/s2.m)*dt
    s3.pos = s3.pos + (s3.p/s3.m)*dt
    t = t+dt
