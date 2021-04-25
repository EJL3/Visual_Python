from vpython import *

run = False
def runbutton(b):
    global run
    if run: b.text = "Run"
    else: b.text = 'Pause'
    run = not run
button(text = "Run", color=color.blue, bind=runbutton)

floor = box(pos=vector(0, -5, 0), size=vector(10, 0.2, 10), texture=textures.wood)
ball = sphere(pos=vector(-5, 5, 0), radius=0.6, color=color.blue, make_trail=True, emissive=True)

ball.m = 0.5
ball.p = ball.m*vector(1, 4, 0) #Projectile of the ball
ball_weight = 0.8
g = 9.8
t = 0
dt = 0.01

graph(height=200, title='Graph for momentum', fast=False, xtitle='<i>t</i>, s', ytitle='<i>v<sub>y</sub></i>, m')
y = gcurve(color=color.red)
l = local_light(pos=ball.pos, color=ball.color)

while ball.pos.x < 8:
    rate(200)
    if run:
        f = vector(0, -ball.m*g, 0)
        ball.p = ball.p + f * dt
        ball.pos = ball.pos + (ball.p/ball.m) * dt
        l.pos = ball.pos
        if ball.pos.y < floor.pos.y + ball.radius:
            ball.p.y = abs(ball.p.y) * ball_weight
        t += dt
        y.plot(t, ball.p.y/ball.m)
