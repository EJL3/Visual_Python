from vpython import *

scene.background = color.black
scene.width = 1000
scene.height = 400
scene.fov = 0.001
scene.userspin = False

endx = 30
thick = 0.08
scene.range = 12


class lens:
    def __init__(self, pos, R1, R2, radius, n):
        self.rays = []
        self.setup(pos, R1, R2, radius, n)

    def setup(self, pos, R1, R2, radius, n):
        self.pos = vector(pos)
        self.R1 = R1
        self.R2 = R2
        if R1 == -R2:
            raise ValueError("A lens with R1 = {:.1f} and R2 = {:.1f} won't deflect".format(R1, R2))
        maxangle1 = asin(radius / abs(R1))
        maxangle2 = asin(radius / abs(R2))
        thick1 = abs(R1) * (1 - cos(maxangle1))
        thick2 = abs(R2) * (1 - cos(maxangle2))
        self.spacer1 = self.spacer2 = 0
        if R1 > 0:
            if R2 < 0:
                if thick2 > thick1:
                    self.spacer2 = thick2 + 0.05 * radius
        else:
            if R2 > 0:
                if thick1 > thick2:
                    self.spacer2 = thick2
            else:  # both surfaces concave
                self.spacer1 = thick1 + 0.03 * radius
                self.spacer2 = thick2 + 0.03 * radius
        self.radius = radius
        self.n = n  # index of refraction
        lensaxis = curve(pos=[vector(-3 * endx, 0, 0), vector(3 * endx, 0, 0)], radius=thick, color=color.yellow)
        self.center1 = vector(self.pos.x + R1 * cos(maxangle1) - self.spacer1, self.pos.y, 0)
        self.leftsurface = curve(radius=thick, color=color.white)
        self.rightsurface = curve(radius=thick, color=color.white)
        for t in arange(-maxangle1, maxangle1 + .0005, .001):
            self.leftsurface.append(pos=vector(self.center1.x - R1 * cos(t), self.center1.y + R1 * sin(t), 0))
        self.center2 = vector(self.pos.x - R2 * cos(maxangle2) + self.spacer2, self.pos.y, 0)
        for t in arange(-maxangle2, maxangle2 + .0005, .001):
            self.rightsurface.append(pos=vector(self.center2.x + R2 * cos(t), self.center2.y + R2 * sin(t), 0))
        self.bottom = None
        self.top = None
        if R1 > 0:
            self.left = self.center1.x - R1
        else:
            self.left = self.leftsurface.point(0).pos.x
        if R2 > 0:
            self.right = self.center2.x + R2
        else:
            self.right = self.rightsurface.point(0).pos.x
        if self.spacer1 + self.spacer2 > 0:
            Llen = self.leftsurface.npoints
            Rlen = self.rightsurface.npoints
            leftstart = 0
            rightstart = 0
            leftend = Llen - 1
            rightend = Rlen - 1
            if self.leftsurface.point(Llen - 1).pos.y < self.leftsurface.point(0).pos.y:
                leftstart = Llen - 1
                leftend = 0
            if self.rightsurface.point(Rlen - 1).pos.y < self.rightsurface.point(0).pos.y:
                rightstart = Rlen - 1
                rightend = 0
            self.top = curve(pos=[self.leftsurface.point(leftend).pos, self.rightsurface.point(rightend).pos],
                             radius=thick)
            self.bottom = curve(pos=[self.leftsurface.point(leftstart).pos, self.rightsurface.point(rightstart).pos],
                                radius=thick)

    def removelens(self):
        self.leftsurface.visible = False
        self.rightsurface.visible = False
        if self.top is not None: self.top.visible = False
        if self.bottom is not None: self.bottom.visible = False

    def makeray(self, raycolor=color.red):
        self.rays.append(curve(color=raycolor, radius=thick))

    def removerays(self):
        for ray in self.rays:
            ray.visible = False

    def raytrace(self, ray, pos, angle):
        pos = vector(pos)
        ray.clear()
        ray.append(pos=pos)
        rhat = vector(cos(angle), sin(angle), 0)
        if rhat.x < 0:
            ray.append(pos=pos + (-3 * endx) / cos(angle) * rhat)
            return
        dr = 0.01 * self.radius
        if pos.x > self.right:
            ray.append(pos=pos + (2 * endx - pos.x) / cos(angle) * rhat)
            return
        elif (pos + (self.left - pos.x) / cos(angle) * rhat).y > self.radius:
            ray.append(pos=pos + (2 * endx - pos.x) / cos(angle) * rhat)
            return
        elif (pos + (self.left - pos.x) / cos(angle) * rhat).y < -self.radius:
            ray.append(pos=pos + (2 * endx - pos.x) / cos(angle) * rhat)
            return
        elif pos.x < self.left:
            ray.append(pos=pos + (self.left - pos.x) / cos(angle) * rhat)
        while True:
            pos = pos + dr * rhat
            if pos.x >= self.pos.x or abs(pos.y) >= abs(self.R1):
                ray.append(pos=pos + (2 * endx - pos.x) / cos(angle) * rhat)
                return
            if pos.x > self.center1.x - self.R1 * cos(asin(pos.y / abs(self.R1))):
                ray.append(pos=pos)
                break
        beta = asin(pos.y / self.R1)
        theta1 = angle + beta
        theta2 = sin(theta1) / self.n
        angle2 = theta2 - beta
        rhat = vector(cos(angle2), sin(angle2), 0)
        while True:
            pos = pos + dr * rhat
            if pos.x > self.center2.x + self.R2 * cos(asin(pos.y / self.R2)):
                ray.append(pos=pos)
                break
        beta = asin(pos.y / self.R2)
        theta1 = beta - angle2
        theta2 = self.n * sin(theta1)
        angle3 = beta - theta2
        rhat = vector(cos(angle3), sin(angle3), 0)
        ray.append(pos=pos + (2 * endx - pos.x) / cos(angle3) * rhat)

lens1 = lens(vector(0, 0, 0), 40, 40, 5, 3)
Nrays = 20
for i in range(Nrays):
    lens1.makeray()
lens1.makeray()
lens1.makeray()
direct = lens1.rays[-2]  # a ray through the center of the lens
parallel = lens1.rays[-1]  # a horizontal ray
drag = False
drag_pos = None

def update():
    for i in range(Nrays):
        #console.log(i, lens1.rays[i])
        lens1.raytrace(lens1.rays[i], drag_pos, (i + .5) * 2 * pi / Nrays)
    lens1.raytrace(direct, drag_pos, atan(drag_pos.y / drag_pos.x))
    lens1.raytrace(parallel, drag_pos, 0)


def grab(evt):
    global drag, drag_pos
    p = scene.mouse.pos
    if p.x > -0.001: return
    drag_pos = p
    update()
    drag = True


def move(evt):
    global drag, drag_pos
    if not drag: return
    p = scene.mouse.pos
    if p.x > 0 or p == drag_pos: return
    drag_pos = p
    update()


def drop(evt):
    global drag, drag_pos
    drag = False
    drag_pos = None


scene.bind('mousedown', grab)
scene.bind('mousemove', move)
scene.bind('mouseup', drop)


def B_Lensbutton(b):
    global drag_pos
    lens1.removelens()
    if b.text == "Diverging lens":
        lens1.setup(vector(0, 0, 0), -40, -40, 5, 3)
        b.text = "Converging lens"
    else:
        lens1.setup(vector(0, 0, 0), 40, 40, 5, 3)
        b.text = "Diverging lens"
    drag_pos = lens1.rays[0].point(0).pos
    update()
    drag_pos = None

button(text="Diverging lens", bind=B_Lensbutton)
scene.append_to_caption("      Click or drag to the left of the lens.")
