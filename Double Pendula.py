from vpython import *

scene.height = scene.width = 500
scene.background = color.white

g = 9.8
M1 = 2
M2 = 1
d = 0.05  # thickness of each bar
gap = 2 * d  # distance between two parts of upper, U-shaped assembly
L1 = 0.5  # physical length of upper bar
L1display = L1 + d
L2 = 1  # physical length of lower bar
L2display = L2 + d / 2
I1 = M1 * L1 ** 2 / 12  # moment of inertia of upper assembly
I2 = M2 * L2 ** 2 / 12  # moment of inertia of lower bar
R1 = L1 / 2  # distance from fixed axle to center of upper bar
R2 = L2 / 2 - d / 4  # distance from moving axle to center of lower bar

hpedestal = 1.3 * (L1 + L2)  # height of pedestal
wpedestal = 0.1  # width of pedestal
tbase = 0.05  # thickness of base
wbase = 8 * gap  # width of base
offset = 2 * gap  # from center of pedestal to center of U-shaped upper assembly
topofbar = vector(0, 0, 0)
scene.center = topofbar - vector(0, L1, 0)

pedestal = box(pos=topofbar - vector(0, hpedestal / 2, 0), height=1.1 * hpedestal, length=wpedestal, width=wpedestal,
               color=vector(0.4, 0.4, 0.5))
base = box(pos=topofbar - vector(0, hpedestal + tbase / 2, 0), height=tbase, length=wbase, width=wbase,
           color=pedestal.color)
axle = cylinder(pos=topofbar - vector(0, 0, offset - gap / 2 + d / 5),
                axis=vector(0, 0, 2 * (offset - gap / 2 + d / 5)), radius=d / 4, color=color.yellow)


class pendulum:

    def __init__(self, pos=topofbar, theta1=1, theta1dot=0, theta2=0, theta2dot=0):
        self.pos = pos
        self.initial_theta1 = theta1
        self.initial_theta1dot = theta1dot
        self.initial_theta2 = theta2
        self.initial_theta2dot = theta2dot
        b1 = box(pos=pos + vector(R1, 0, -(gap + d) / 2), size=vector(L1display, d, d), color=color.red)
        b2 = box(pos=pos + vector(R1, 0, (gap + d) / 2), size=vector(L1display, d, d), color=color.red)
        c = cylinder(pos=pos + vector(L1, 0, -(gap + d) / 2), axis=vector(0, 0, gap + d), radius=axle.radius,
                     color=color.green)
        self.frame1 = compound([b1, b2, c])
        self.frame1.rotate(angle=self.initial_theta1 - pi / 2, axis=vector(0, 0, 1), origin=vector(0, 0, 0))
        self.frame1.initial_pos = vector(self.frame1.pos)
        self.frame1.initial_axis = vector(self.frame1.axis)

        b3 = box(pos=vector(R2, 0, 0), size=vector(L2display, d, d), color=color.green)
        self.frame2 = compound([b3])
        self.reset()
        self.__visible = True

    def update(self, dtheta1=0, dtheta2=0):
        self.theta1 += dtheta1
        self.theta2 += dtheta2
        self.frame1.rotate(angle=dtheta1, axis=vector(0, 0, 1), origin=self.pos)
        axle2pos = self.frame1.pos + R1 * norm(self.frame1.axis)  # center of cylinder in the U-shaped assembly
        self.frame2.rotate(angle=dtheta2, axis=vector(0, 0, 1), origin=axle2pos)
        self.frame2.pos = axle2pos + R2 * norm(self.frame2.axis)

    def reset(self):
        self.theta1 = self.initial_theta1
        self.theta1dot = self.initial_theta1dot
        self.theta2 = self.initial_theta2
        self.theta2dot = self.initial_theta2dot
        self.frame1.pos = self.frame1.initial_pos
        self.frame1.axis = self.frame1.initial_axis
        axle2pos = self.frame1.pos + R1 * norm(self.frame1.axis)
        self.frame2.pos = axle2pos + vector(R2, 0, 0)
        self.frame2.axis = vector(L2display, 0, 0)
        self.frame2.rotate(angle=self.theta2 - pi / 2, axis=vector(0, 0, 1), origin=axle2pos)

    def get_visible(self):
        return self.__visible

    def set_visible(self, vis):
        self.__visible = self.frame1.visible = self.frame2.visible = vis


pend1 = pendulum(topofbar + vector(0, 0, offset), 2.1, 0, 2.4, 0)
pend2 = pendulum(topofbar + vector(0, 0, -offset), 2.1, 0, 2.4, 0)
pend2.initial_theta1 += 0.001
pend2.reset()
pend2.set_visible(False)
pendula = [pend1, pend2]
scene.autoscale = False
run = False

def reset():
    global t, gd, energy_check
    t = 0
    ResetRunbutton()
    for pend in pendula:
        pend.reset()
    if gd:
        gd.delete()
        gd = None
        energy_check = False
        EnergyCheck(None)


def ResetRunbutton():
    global run
    run = False
    Runbutton.text = "Run"


def Runb(r):
    global run
    run = not run
    if run:
        r.text = "Pause"
    else:
        r.text = "Run"


Runbutton = button(text='Run', bind=Runb)

scene.append_to_caption('   ')

button(text='Reset', bind=reset)

scene.append_to_caption('\n\nChoose a situation:   ')

options = ['One double pendulum', 'Two double pendula, starting with angles that differ by only 0.001 radian']


def choosependula(p):
    if p.selected == options[0]:  # one double pendulum
        if not pendula[1].get_visible(): return
        pendula[1].set_visible(False)
    else:  # two double pendula
        if pendula[1].get_visible(): return
        pendula[1].set_visible(True)
    reset()


setmenu = menu(choices=options, selected='One double pendulum', bind=choosependula)

scene.append_to_caption('\n \n')

energy_check = False
gd = None
gK = None
gU = None
gE = None


def EnergyCheck(ec):
    global energy_check, graphing, gd, gK, gU, gE
    energy_check = not energy_check
    if energy_check:
        if not gd:
            gd = graph(width=scene.width, height=300, title='K is green, U is blue, E = K+U is red')
            t = 0
        gK = gcurve(color=color.green)
        gU = gcurve(color=color.blue)
        gE = gcurve(color=color.red)


checkbox(bind=EnergyCheck)
scene.append_to_caption(' Graph energy (for front pendulum)\n\n')

dt = 0.0002
t = 0
n = 0

C11 = (0.25 * M1 + M2) * L1 ** 2 + I1
C22 = 0.25 * M2 * L2 ** 2 + I2

while True:
    rate(1 / dt)
    if not run: continue
    for pend in pendula:
        # Calculate accelerations of the Lagrangian coordinates:
        C12 = C21 = 0.5 * M2 * L1 * L2 * cos(pend.theta1 - pend.theta2)
        Cdet = C11 * C22 - C12 * C21
        a = .5 * M2 * L1 * L2 * sin(pend.theta1 - pend.theta2)
        A = -(.5 * M1 + M2) * g * L1 * sin(pend.theta1) - a * pend.theta2dot ** 2
        B = -.5 * M2 * g * L2 * sin(pend.theta2) + a * pend.theta1dot ** 2
        pend.atheta1 = (C22 * A - C12 * B) / Cdet
        pend.atheta2 = (-C21 * A + C11 * B) / Cdet
        pend.theta1dot += pend.atheta1 * dt
        pend.theta2dot += pend.atheta2 * dt
        dtheta1 = pend.theta1dot * dt
        dtheta2 = pend.theta2dot * dt
        pend.update(dtheta1, dtheta2)

    t = t + dt
    n += 1

    if energy_check and n >= 100:
        n = 0
        K = .5 * ((.25 * M1 + M2) * L1 ** 2 + I1) * pend1.theta1dot ** 2 + .5 * (
                    .25 * M2 * L2 ** 2 + I2) * pend1.theta2dot ** 2 + \
            .5 * M2 * L1 * L2 * cos(pend1.theta1 - pend1.theta2) * pend1.theta1dot * pend1.theta2dot
        U = -(.5 * M1 + M2) * g * L1 * cos(pend1.theta1) - .5 * M2 * g * L2 * cos(pend1.theta2)
        gK.plot(pos=(t, K))
        gU.plot(pos=(t, U))
        gE.plot(pos=(t, K + U))
