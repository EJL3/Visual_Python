from vpython import *

win = 500
Natoms = 200  # change this to have more or fewer atoms
L = 1
gray = color.gray(0.7)  # color of edges of container
mass = 4E-3 / 6E23  # helium mass
Ratom = 0.03
k = 1.4E-23  # Boltzmann constant
T = 300
dt = 1E-5

animation = canvas(width=win, height=win, align='left')
animation.range = L
animation.title = 'A "hard-sphere" gas'
s = """&nbsp;&nbsp;Theoretical and averaged speed distributions (meters/sec).
&nbsp;&nbsp;Initially all atoms have the same speed, but collisions
&nbsp;&nbsp;change the speeds of the colliding atoms. One of the atoms is
&nbsp;&nbsp;marked and leaves a trail so you can follow its path.
&nbsp
"""
animation.caption = s

d = L / 2 + Ratom
r = 0.005
boxbottom = curve(color=gray, radius=r)
boxbottom.append([vector(-d, -d, -d), vector(-d, -d, d), vector(d, -d, d), vector(d, -d, -d), vector(-d, -d, -d)])
boxtop = curve(color=gray, radius=r)
boxtop.append([vector(-d, d, -d), vector(-d, d, d), vector(d, d, d), vector(d, d, -d), vector(-d, d, -d)])
vert1 = curve(color=gray, radius=r)
vert2 = curve(color=gray, radius=r)
vert3 = curve(color=gray, radius=r)
vert4 = curve(color=gray, radius=r)
vert1.append([vector(-d, -d, -d), vector(-d, d, -d)])
vert2.append([vector(-d, -d, d), vector(-d, d, d)])
vert3.append([vector(d, -d, d), vector(d, d, d)])
vert4.append([vector(d, -d, -d), vector(d, d, -d)])

Atoms = []
p = []
apos = []
pavg = sqrt(2 * mass * 1.5 * k * T)

for i in range(Natoms):
    x = L * random() - L / 2
    y = L * random() - L / 2
    z = L * random() - L / 2
    if i == 0:
        Atoms.append(sphere(pos=vector(x, y, z), radius=Ratom, color=color.cyan, make_trail=True, retain=100,
                            trail_radius=0.3 * Ratom))
    else:
        Atoms.append(sphere(pos=vector(x, y, z), radius=Ratom, color=gray))
    apos.append(vec(x, y, z))
    theta = pi * random()
    phi = 2 * pi * random()
    px = pavg * sin(theta) * cos(phi)
    py = pavg * sin(theta) * sin(phi)
    pz = pavg * cos(theta)
    p.append(vector(px, py, pz))

deltav = 100

def barx(v):
    return int(v / deltav)

nhisto = int(4500 / deltav)
histo = []
for i in range(nhisto): histo.append(0.0)
histo[barx(pavg / mass)] = Natoms

gg = graph(width=win, height=0.4 * win, xmax=3000, align='left', xtitle='speed, m/s', ytitle='Number of atoms',
           ymax=Natoms * deltav / 1000)
theory = gcurve(color=color.cyan)
dv = 10
for v in range(0, 3001 + dv, dv):
    theory.plot(v, (deltav / dv) * Natoms * 4 * pi * ((mass / (2 * pi * k * T)) ** 1.5) * exp(
        -0.5 * mass * (v ** 2) / (k * T)) * (v ** 2) * dv)

accum = []
for i in range(int(3000 / deltav)): accum.append([deltav * (i + .5), 0])
vdist = gvbars(color=color.red, delta=deltav)


def interchange(v1, v2):
    barx1 = barx(v1)
    barx2 = barx(v2)
    if barx1 == barx2:  return
    if barx1 >= len(histo) or barx2 >= len(histo): return
    histo[barx1] -= 1
    histo[barx2] += 1


def checkCollisions():
    hitlist = []
    r2 = 2 * Ratom
    r2 *= r2
    for i in range(Natoms):
        ai = apos[i]
        for j in range(i):
            aj = apos[j]
            dr = ai - aj
            if mag2(dr) < r2: hitlist.append([i, j])
    return hitlist

nhisto = 0

while True:
    rate(200)
    for i in range(len(accum)): accum[i][1] = (nhisto * accum[i][1] + histo[i]) / (nhisto + 1)
    if nhisto % 10 == 0:
        vdist.data = accum
    nhisto += 1

    for i in range(Natoms): Atoms[i].pos = apos[i] = apos[i] + (p[i] / mass) * dt
    hitlist = checkCollisions()

    for ij in hitlist:
        i = ij[0]
        j = ij[1]
        ptot = p[i] + p[j]
        posi = apos[i]
        posj = apos[j]
        vi = p[i] / mass
        vj = p[j] / mass
        vrel = vj - vi
        a = vrel.mag2
        if a == 0: continue;
        rrel = posi - posj
        if rrel.mag > Ratom: continue

        dx = dot(rrel, vrel.hat)
        dy = cross(rrel, vrel.hat).mag
        alpha = asin(dy / (2 * Ratom))
        d = (2 * Ratom) * cos(alpha) - dx  # distance traveled into the atom from first contact
        deltat = d / vrel.mag  # time spent moving from first contact to position inside atom

        posi = posi - vi * deltat
        posj = posj - vj * deltat
        mtot = 2 * mass
        pcmi = p[i] - ptot * mass / mtot
        pcmj = p[j] - ptot * mass / mtot
        rrel = norm(rrel)
        pcmi = pcmi - 2 * pcmi.dot(rrel) * rrel
        pcmj = pcmj - 2 * pcmj.dot(rrel) * rrel
        p[i] = pcmi + ptot * mass / mtot
        p[j] = pcmj + ptot * mass / mtot
        apos[i] = posi + (p[i] / mass) * deltat
        apos[j] = posj + (p[j] / mass) * deltat
        interchange(vi.mag, p[i].mag / mass)
        interchange(vj.mag, p[j].mag / mass)

    for i in range(Natoms):
        loc = apos[i]
        if abs(loc.x) > L / 2:
            if loc.x < 0:
                p[i].x = abs(p[i].x)
            else:
                p[i].x = -abs(p[i].x)

        if abs(loc.y) > L / 2:
            if loc.y < 0:
                p[i].y = abs(p[i].y)
            else:
                p[i].y = -abs(p[i].y)

        if abs(loc.z) > L / 2:
            if loc.z < 0:
                p[i].z = abs(p[i].z)
            else:
                p[i].z = -abs(p[i].z)
