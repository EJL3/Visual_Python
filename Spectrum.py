from vpython import *

scene.caption = "Click to sequence through various spectrum situations."

d = 0.05
L = 0.6
N = 100
zblue = 0.6*d
zlong = 1.8*d
wslit = zlong/N
wslitadjust = 1*wslit
hslit = 0.8*d
dy = 0.1*d

scene.width = 800
scene.height = 600
scene.range = 0.35*L
scene.center = vector(4*d+0.75*L, -0.05*L, 0)
scene.forward = -vector(1, .7, .8)
scene.background = color.black

gray = color.gray(0.4)
scene.lights = []
distant_light(direction=vector(0, 0, 1), color=gray)
distant_light(direction=vector(1, 0, 0), color=color.white)
distant_light(direction=vector(0, 0, 1), color=gray)
distant_light(direction=vector(0, 1, 0), color=gray)
container = box(size=vector(8*d, d, d), color=gray)

objs = [container]
objs.append(box(pos=vector(4*d+L,hslit/2+dy/2,0), size=vector(0.01*d,dy,2*zblue+2*(N-1)*wslit+wslit+2*dy), color=gray, shininess=0))
objs.append(box(pos=vector(4*d+L,-hslit/2-dy/2,0), size=vector(0.01*d,dy,2*zblue+2*(N-1)*wslit+wslit+2*dy), color=gray, shininess=0))
objs.append(box(pos=vector(4*d+L,0,zblue+(N-1)*wslit+wslit/2+dy/2), size=vector(0.01*d,hslit,dy), color=gray, shininess=0))
objs.append(box(pos=vector(4*d+L,0,-zblue-(N-1)*wslit-wslit/2-dy/2), size=vector(0.01*d,hslit,dy), color=gray, shininess=0))
objs.append(box(pos=vector(4*d+L,0,(zblue+wslit/2)/2), size=vector(0.01*d,hslit,(zblue-wslit/2)), color=gray, shininess=0))
objs.append(box(pos=vector(4*d+L,0,(-zblue-wslit/2)/2), size=vector(0.01*d,hslit,(zblue-wslit/2)), color=gray, shininess=0))
apparatus = compound(objs)

slit = box(pos=vector(4*d,0,0), size=vector(0.3*d,hslit,wslit), color=gray)
center = box(pos=vector(4*d+L,0,0), size=vector(0.015*d,hslit,wslit), color=gray, shininess=0) # center of spectrum screen

gobjects = []
w = 0.05*d
gobjects.append(box(pos=vector(0,0,-d), size=vector(0.01*d,2.1*d,0.1*d), color=gray, visible=False))
gobjects.append(box(pos=vector(0,0,d), size=vector(0.01*d,2.1*d,0.1*d), color=gray, visible=False))
gobjects.append(box(pos=vector(0,d,0), size=vector(0.01*d,0.1*d,2*d), color=gray, visible=False))
gobjects.append(box(pos=vector(0,-d,0), size=vector(0.01*d,0.1*d,2*d), color=gray, visible=False))
for z in arange(-d+0.05*d+w, d-0.05*d, w):
    gobjects.append(cylinder(pos=vector(0,-d,z), axis=vector(0,2*d,0), radius=0.01*d, color=gray, visible=False))

grating = compound(gobjects, pos=slit.pos+vector(0.5*L,0,0), visible=False)

gratingtitle = label(pos=slit.pos+vector(0.5*L,1.5*d,-1.8*d), text='Diffraction Grating', visible=False, box=False)
sourcetitle = label(pos=container.pos+vector(-container.length/2,container.height,0), text='White Light Source', box=False)
leftspectrum = label(pos=center.pos+vector(0,-1.1*hslit,1.5*d), text='Spectrum', visible=False, box=False)
rightspectrum = label(pos=center.pos+vector(0.1*hslit,-1.1*hslit,-1.8*d), text='Spectrum', visible=False, box=False)

left = []
right = []
leftray = []
rightray = []
white = []
for nn in range(N):
    left.append(box(pos=center.pos+vector(0,0,zblue+nn*wslit), size=vector(0.01*d,hslit,wslitadjust), color=gray, shininess=0))
    leftray.append(box(pos=(grating.pos+left[-1].pos)/2, size=vector(mag(left[-1].pos-grating.pos),hslit,wslit), color=gray, visible=0, shininess=0))
    leftray[-1].axis = left[-1].pos-grating.pos
    right.append(box(pos=center.pos+vector(0,0,-zblue-nn*wslit), size=vector(0.01*d,hslit,wslitadjust), color=gray, shininess=0))
    rightray.append(box(pos=(grating.pos+right[-1].pos)/2, size=vector(mag(right[-1].pos-grating.pos),hslit,wslit), color=gray, visible=0, shininess=0))
    rightray[-1].axis = right[-1].pos-grating.pos
    white.append(color.hsv_to_rgb(vector((nn/N)*(2/3),1,1)))

beam1 = box(pos=(slit.pos+center.pos)/2, size=vector(center.pos.x-slit.pos.x,hslit,wslit), color=color.white, visible=0)

absorber = box(pos=container.pos+container.axis/2+vector(L/5,0,0), size=vector(0.2*d,1.4*hslit,1.4*hslit), color=vector(0.4,0.4,0.4), visible=0)
absorbertitle = label(pos=absorber.pos+vector(-10*hslit,-3*hslit,1.1*hslit), text='Cold gas #2 absorber', visible=False, box=False)

def showspectrum(colorlist, absorb):
    raycolor = vector(0,0,0)
    nlines = 0
    if not absorb:
        for nn in range(N):
            left[nn].color = gray
            right[nn].color = gray
            leftray[nn].visible = False
            rightray[nn].visible = False
    if colorlist is off:
        slit.color = center.color = gray
        beam1.visible = False
        return
    beam1.visible = True
    for col in colorlist:
        hsv = color.rgb_to_hsv(col)
        hue = hsv.x
        nindex = int(N*(1-1.5*hue)+0.5)
        if nindex >= N:
            nindex = N-1
        setcol = col
        if absorb:
            setcol = color.black
        for n in [nindex, nindex+1]:
            if (not absorb and n != nindex): break
            left[n].color = setcol
            right[n].color = setcol
            leftray[n].color = setcol
            leftray[n].visible = True
            rightray[n].color = setcol
            rightray[n].visible = True
        nindex += 1
        if not col.equals(vector(0,0,0)):
            raycolor = raycolor + vector(col)
            nlines += 1
    raycolor = raycolor/nlines
    hsv = color.rgb_to_hsv(raycolor)
    if nlines > 1:
        hsv = vector(hsv.x, hsv.y, 1)
    if colorlist is white or absorb:
        hsv = vector(0,0,1)
    beam1.color = slit.color = center.color = color.hsv_to_rgb(hsv)

off = [gray]
gas1 = [color.green, vector(1,0.3,0)]
gas2 = [color.hsv_to_rgb(vector(0.2,1,1)), color.orange, color.cyan]
gas2absorb = [color.orange, color.cyan]

while True:
    grating.visible = False
    gratingtitle.visible = False
    leftspectrum.visible = rightspectrum.visible = False
    sourcetitle.text = 'Light Source Off'
    showspectrum(off, False)
    scene.waitfor('click')
    sourcetitle.text = 'White Light Source'
    beam1.color = slit.color = center.color = color.white
    beam1.visible = True
    scene.waitfor('click')
    grating.visible = True
    gratingtitle.visible = True
    leftspectrum.visible = rightspectrum.visible = True
    showspectrum(white, False)
    scene.waitfor('click')
    sourcetitle.text = 'Electron-excited Gas #1'
    showspectrum(gas1, False)
    scene.waitfor('click')
    sourcetitle.text = 'Electron-excited Gas #2'
    showspectrum(gas2, False)
    scene.waitfor('click')
    sourcetitle.text = 'White Light Source'
    showspectrum(white, False)
    scene.waitfor('click')
    absorber.visible = absorbertitle.visible = True
    showspectrum(gas2absorb, True)
    scene.waitfor('click')
    absorber.visible = absorbertitle.visible = False
