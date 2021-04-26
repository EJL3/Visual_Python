from vpython import *

h = 600
w = 600
scene.width = w
scene.height = h
hw = 1  # half width
scene.fov = 0.001
scene.range = hw
scene.userzoom = 0
scene.userspin = 0
scene.background = color.black

gridd = 0.5 * hw
gridr = 2 * hw + gridd
Rball = hw / 20
ball = sphere(pos=vector(0, 0, 0), color=color.blue, radius=Rball, make_trail=True, retain=300, interval=10)
ball.mass = 200
ball.p = vector(0, 0, 0)

scene.camera.follow(ball)

dt = 0.02
Fmouse = 1
Fview = 1
pview = 0.025

drag = False
F = vector(0, 0, 0)
Foffset = vector(0, 0, ball.size.y / 2)
Fvector = arrow(pos=ball.pos + Foffset, axis=vector(0, 0, 0), shaftwidth=hw / 30, color=color.green)
pvector = arrow(pos=ball.pos + 1.5 * Foffset, axis=vector(0, 0, 0), shaftwidth=hw / 30, color=color.red)


def reset(r):
    drag = False
    ball.clear_trail()
    ball.pos = ball.p = F = Fvector.axis = pvector.axis = vector(0, 0, 0)

button(text='Reset', bind=reset)

scene.append_to_caption('<br>Drag the (green) arrow representing the net force on the ball.<br>')
scene.append_to_caption("The ball's momentum is represented by a red arrow.<br><br>")
scene.append_to_caption('Suggestions: Try to make the ball move in a circle.<br>')
scene.append_to_caption('Or start it moving, then bring it to a stop on a line.<br>')
scene.append_to_caption('Or have it move with a constant downward force.')


def up(ev):
    global drag
    drag = False


def down(ev):
    global drag
    drag = True
    scene.bind("mouseup", up)

scene.bind("mousedown", down)

while True:
    rate(200)
    if drag:
        F = Fmouse * (scene.mouse.pos - ball.pos)
    Fvector.axis = Fview * F
    ball.p = ball.p + F * dt
    ball.pos = ball.pos + (ball.p / ball.mass) * dt
    if abs(ball.pos.x) + Rball >= gridr:
        ball.p.x = -ball.p.x
    if abs(ball.pos.y) + Rball >= gridr:
        ball.p.y = -ball.p.y
    Fvector.pos = ball.pos + Foffset
    Fvector.axis = Fview * F
    pvector.pos = ball.pos + 1.5 * Foffset
    pvector.axis = pview * ball.p
