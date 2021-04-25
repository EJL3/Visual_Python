from vpython import *
G = 6.7e-11 #Newton gravitational constant
dt = 1e5

giant = sphere(pos=vector(-1e11, 0, 0), radius=2e10, color=color.red, make_trail=True, trail_type='points', interval=10, retain=50)
giant.mass = 2e30
giant.p = vector(0, 0, -1e4) * giant.mass

dwarf = sphere(pos=vector(1.5e11, 0, 0), radius=1e10, color=color.cyan, make_trail=True, interval=10, retain=50)
dwarf.mass = 1e30
dwarf.p = -giant.p

while True:
    rate(200)
    r = dwarf.pos - giant.pos
    f = G * giant.mass * dwarf.mass * r.hat / mag2(r)
    giant.p = giant.p + f*dt
    dwarf.p = dwarf.p - f*dt
    giant.pos = giant.pos + (giant.p/giant.mass) * dt
    dwarf.pos = dwarf.pos + (dwarf.p/dwarf.mass) * dt

