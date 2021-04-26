from vpython import *

scene.width = scene.height = 700
scene.background = color.black
scene.foreground = color.black
scene.title="Quantum Oscillator"

def U(s):
    Us = 0.5*ks*s**2
    return Us

L0 = 10
U0 = -10
dU = 2
m1 = sphere(pos=vector(-L0,0.5*5**2,0), radius=0.5, color=color.red)
m2 = sphere(pos=vector(0,0.5*5**2,0), radius=0.5, color=color.cyan)
m1.mass = 0.025
m2.mass = 0.025
ks = 1.2
omega = sqrt(ks/m2.mass)
spring = helix(pos=m1.pos, axis=(m2.pos-m1.pos), radius=0.40, coils=10, thickness=0.2, color=vector(.7, .5, 0))
well=curve(radius=0.2, color=color.gray(.7))
for xx in arange(-5.8, 5.3, 0.1):
    well.append(pos=vector(xx, .5*ks*xx**2+U0, 0))
well.append(pos=vector(8,.5*ks*5.2**2+U0,0))
vline1=cylinder(pos=vector(-5,m1.pos.y-dU,0), axis=vector(0,2*dU,0), radius=0.05, color=color.gray(.6), visible=False)
vline2=cylinder(pos=vector(5,m1.pos.y-dU,0), axis=vector(0,2*dU,0), radius=0.05, color=color.gray(.6), visible=False)

s = """Semiclassical model of quantum oscillator.
Click on an energy level to put the oscillator into that state."""

label(pos=vector(0, U0-dU, 0), text=s, color=color.white, box=0)


levels = []
for Ux in arange(0.5*dU, 7.51*dU, dU):
    s = sqrt(2*Ux/ks)
    l1 = cylinder(radius=0.2, pos=vector(-s, Ux+U0, 0), axis=vector(2*s,0,0), color=color.white)
    levels.append(l1)

scene.center = vector(0, U0+5*dU, 0)
scene.range = 15

t = 0.0
dt = 0.003
oldlvl = None
lvl = None
RUN = False

clicked = False
def getclick():
    global clicked
    clicked = True

scene.bind('click', getclick)

while True:
    rate(200)
    if clicked:
        clicked = False
        a = scene.mouse.pick
        if a in levels:
            oldlvl = lvl
            lvl = a
            lvl.color=color.red
            if oldlvl is not None:
                oldlvl.color = color.white
            Ampl = abs(lvl.pos.x)
            vline1.visible = vline2.visible = True
            vline1.pos.x = lvl.pos.x
            vline2.pos.x = lvl.pos.x+lvl.axis.x
            RUN = True
        else:
            continue

    elif RUN:
        m2.pos = vector(Ampl*cos(omega*t),m2.pos.y,m2.pos.z)
        spring.pos = m1.pos
        spring.axis = m2.pos-m1.pos
        t = t+dt
