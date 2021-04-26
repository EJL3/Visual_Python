from vpython import *

scene.background = color.white
scene.width = 1000
scene.fov = 0.05
if version[1] == 'glowscript':
    scene.range = 10
    xmax = 20
    scene.center = vector(0, -2, 0)
    yquestion = -11
    hfont = 14
else:
    scene.range = 24
    xmax = 24
    scene.center = vector(0, -2, 0)
    yquestion = -10
    hfont = 14

visTRAIL = False
visREL = False
visTOT = False
visCM = False

w = 1
L0 = 6
yo = vector(0, 1.5 * w / 2, 0)
interval = 10
retain = 40
b1 = sphere(pos=vector(-xmax, 0.8, 0), radius=0.5, color=color.blue, m=1, make_trail=visTRAIL, interval=interval,
            retain=retain)
rod1 = cylinder(pos=b1.pos, axis=vector(0, L0, 0), radius=0.1, color=vector(0.7, 0.5, 0))
b2 = sphere(pos=rod1.pos + rod1.axis, radius=0.5, color=color.blue, m=1, make_trail=visTRAIL, interval=interval,
            retain=retain)

b3 = sphere(pos=vector(-xmax, -2 - L0, 0), radius=0.5, color=color.red, m=1, make_trail=visTRAIL, interval=interval,
            retain=retain)
rod2 = cylinder(pos=b3.pos, axis=vector(0, L0, 0), radius=0.1, color=vector(0.7, 0.5, 0))
b4 = sphere(pos=rod2.pos + rod2.axis, radius=0.5, color=color.red, m=1, make_trail=visTRAIL, interval=interval,
            retain=retain)

cm1 = vector(0.5 * (b1.pos + b2.pos))
cm2 = vector(0.5 * (b3.pos + b4.pos))
vcm = vector(5, 0, 0)
omega = 2
vscale = 0.35

v1tot = arrow(pos=b1.pos, axis=vscale * vcm, color=b1.color, shaftwidth=0.2, fixedwidth=1, visible=visTOT)
v2tot = arrow(pos=b2.pos, axis=vscale * vcm, color=b2.color, shaftwidth=0.2, fixedwidth=1, visible=visTOT)
v3rel = arrow(pos=b3.pos, axis=vector(0, 0, 0), color=color.green, shaftwidth=0.2, fixedwidth=1, visible=visREL)
v4rel = arrow(pos=b4.pos, axis=vector(0, 0, 0), color=color.green, shaftwidth=0.2, fixedwidth=1, visible=visREL)
vcma1 = arrow(axis=vector(0, 0, 0), color=color.cyan, shaftwidth=0.2, fixedwidth=1, visible=visCM)
vcma2 = arrow(axis=vector(0, 0, 0), color=color.cyan, shaftwidth=0.2, fixedwidth=1, visible=visCM)
v3tot = arrow(pos=b3.pos, axis=vector(0, 0, 0), color=b3.color, shaftwidth=0.2, fixedwidth=1, visible=visTOT)
v4tot = arrow(pos=b4.pos, axis=vector(0, 0, 0), color=b4.color, shaftwidth=0.2, fixedwidth=1, visible=visTOT)

s = 'Which object has the greater total momentum? Greater kinetic energy? Greater translational kinetic energy?'
question = label(pos=vector(0, yquestion, 0), text=s, height=hfont, color=color.black, box=0, visible=False)


def Runbutton(r):
    global run
    run = not run
    if run:
        r.text = "Pause"
    else:
        r.text = "Run"


button(text='Run', bind=Runbutton)

scene.append_to_caption('   ')


def trails(t):
    global visTRAIL
    visTRAIL = not visTRAIL
    b1.clear_trail()
    b2.clear_trail()
    b3.clear_trail()
    b4.clear_trail()
    b1.make_trail = visTRAIL
    b2.make_trail = visTRAIL
    b3.make_trail = visTRAIL
    b4.make_trail = visTRAIL


checkbox(bind=trails, text='Show trails   ')


def vrelative(f):
    global visREL
    visREL = not visREL
    v3rel.visible = visREL
    v4rel.visible = visREL


checkbox(bind=vrelative, text='Show relative velocities   ')


def vactual(v):
    global visTOT
    visTOT = not visTOT
    v1tot.visible = visTOT
    v2tot.visible = visTOT
    v3tot.visible = visTOT
    v4tot.visible = visTOT


checkbox(bind=vactual, text='Show actual velocities   ')


def cmvelocities(c):
    global visCM
    visCM = not visCM
    vcma1.visible = visCM
    vcma2.visible = visCM


checkbox(bind=cmvelocities, text='Show CM velocities')


def vcmchange(v):
    global vcm
    vcm.x = v.value


scene.append_to_caption('\n\nChange the center of mass speed:\n')
slider(value=vcm.x, length=600, max=10, top=5, bind=vcmchange)


def omegachange(o):
    global omega
    omega = o.value


scene.append_to_caption('\n\nChange the rotational speed:\n')
slider(value=omega, length=600, max=10, top=5, bind=omegachange)

run = False

dt = 0.005
t = 0

while True:
    rate(200)
    if not run: continue
    question.visible = True
    if b1.pos.x > 1.4 * xmax:
        w = 2.8
        d = vector(-2.8 * xmax, 0, 0)
        b1.pos = b1.pos + d
        b2.pos = b2.pos + d
        b3.pos = b3.pos + d
        b4.pos = b4.pos + d
        cm1 = cm1 + d
        cm2 = cm2 + d
        if visTRAIL:
            b1.clear_trail()
            b2.clear_trail()
            b3.clear_trail()
            b4.clear_trail()

    cm1 = cm1 + vcm * dt
    cm2 = cm2 + vcm * dt
    b1.pos = b1.pos + vcm * dt
    b2.pos = b2.pos + vcm * dt
    rod1.pos = b1.pos
    rod1.axis = b2.pos - b1.pos

    rod2.rotate(angle=omega * dt, axis=vector(0, 0, -1))
    rod2.pos = cm2 - 0.5 * rod2.axis
    b3.pos = cm2 - 0.5 * rod2.axis
    b4.pos = cm2 + 0.5 * rod2.axis

    if visREL:
        vrot = vscale * cross(vector(0, 0, -omega), rod2.axis)
        v3rel.pos = b3.pos
        v3rel.axis = -vrot
        v4rel.pos = b4.pos
        v4rel.axis = vrot

    if visTOT:
        v1tot.pos = b1.pos
        v2tot.pos = b2.pos
        vrot = cross(vector(0, 0, -omega), rod2.axis)
        v3tot.pos = b3.pos
        v3tot.axis = vscale * (vcm - vrot)
        v4tot.pos = b4.pos
        v4tot.axis = vscale * (vcm + vrot)

    if visCM:
        vcma1.pos = cm1
        vcma1.axis = vcm * vscale
        vcma2.pos = cm2
        vcma2.axis = vcm * vscale
