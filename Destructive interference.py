from vpython import *

scene.width = 1000
scene.height = 400
scene.forward = vector(0, -1, -2)
scene.background = color.black
scene.range = 0.12
scene.fov = 0.1

lamb = 1e-1
c = 3e8
omega = 2 * pi * c / lamb
## slit spacing
d = 2 * lamb

Evec1 = []
Evec2 = []

dist_to_screen = 4 * lamb
scene.center = vector(dist_to_screen * .65, -d / 4, 0)
scene.caption = "Click to toggle seeing magnetic field"
ds = lamb / 20
dt = lamb / c / 100
E0 = lamb / 3

screen = curve(pos=[vector(dist_to_screen, 0, 0), vector(dist_to_screen, 0, 2 * d)], color=vector(.6, .6, .6))
slit1 = vector(0, 0, -d / 2)
slit2 = vector(0, 0, d / 2)

max1 = vector(dist_to_screen, 0, 0)
max2 = vector(dist_to_screen, 0, 0.24)
min1 = vector(dist_to_screen, 0, 0.108)

r1 = min1 - slit1
r2 = min1 - slit2

dr1 = ds * norm(r1)
dr2 = ds * norm(r2)

rr1 = slit1 + vector(0, 0, 0)  ## current loc along wave 1
rr2 = slit2 + vector(0, 0, 0)  ## current loc along wave 2

i1 = None
i2 = None

## create first wave
for i in range(120):
    ea = arrow(pos=rr1, axis=vector(0, E0 * cos(2 * pi * mag(rr1 - slit1) / lamb), 0), color=color.red,
               shaftwidth=lamb / 40)
    ba = arrow(pos=rr1, axis=vector(0, 0, 0), color=vector(.4, .4, 1), shaftwidth=lamb / 40., visible=False)
    ea.B = ba
    if abs(ea.pos.x - dist_to_screen) < 0.002 and i1 == None:
        i1 = ea
    else:
        Evec1.append(ea)
    rr1 = rr1 + dr1

#### create second wave
for i in range(100):
    ea = arrow(pos=rr2, axis=vector(0, E0 * cos(2 * pi * mag(rr2 - slit2) / lamb), 0), color=vector(1., .6, 0),
               shaftwidth=lamb / 40)
    ba = arrow(pos=rr2, axis=vector(0, 0, 0), color=color.cyan, shaftwidth=lamb / 40., visible=False)
    ea.B = ba
    if abs(ea.pos.x - dist_to_screen) < 0.002 and i2 == None:
        i2 = ea
    else:
        Evec2.append(ea)
    rr2 = rr2 + dr2

i1.visible = False


def clicked(evt):
    for a in Evec1:
        a.B.visible = not a.B.visible
    for a in Evec2:
        a.B.visible = not a.B.visible
    i2.B.visible = not i2.B.visible


scene.bind('click', clicked)
t = 0
while True:
    rate(50)
    t = t + dt
    for ea in Evec1:
        ea.axis = vector(0, E0 * cos(omega * t - 2 * pi * mag(ea.pos - slit1) / lamb), 0)
        ea.B.axis = cross(norm(r1), ea.axis) * .7
    for ea in Evec2:
        ea.axis = vector(0, E0 * cos(omega * t - 2 * pi * mag(ea.pos - slit2) / lamb), 0)
        ea.B.axis = cross(norm(r2), ea.axis) * .7
    sum = E0 * cos(omega * t - 2 * pi * mag(i1.pos - slit1) / lamb) + E0 * cos(
        omega * t - 2 * pi * mag(i2.pos - slit2) / lamb)  # superposition
    i2.axis = vector(0, sum, 0)
    i2.B.axis = cross(i2.axis, norm(r2)) * .7
