from vpython import *

w = 600
h = 600
scene.width = w
scene.height = h
hw = w / 2
hh = h / 2
scene.fov = 0.001
scene.range = hw
scene.background = color.white
scene.userspin = False
scene.userzoom = False
scene.userpan = False
scene.lights = []
distant_light(direction=vec(0, 0, 1), color=color.white)
left = -0.95 * hw
top = 0.95 * hh
lineheight = 20
a = 0
b = 0
sum = 0
orange = 0.8 * color.orange

s = """a = 5
a = a + 3
b = 10
a = a + b
b = 1
sum = 0
while b < 4:
    sum = sum + b
    print(b, sum)
    b = b + 1
print("sum =", sum)"""

##### Setup program, CPU area, Memory area and Print area
shift = 0.18 * hh + 50
for n in range(5):  # create computer memory containers
    curve(pos=[vec(40, -n * 40 - shift, 0), vec(0.9 * hw, -n * 40 - shift, 0), vec(0.9 * hw, -n * 40 - shift + 30, 0),
               vec(40, -n * 40 - shift + 30, 0), vec(40, -n * 40 - shift, 0)], radius=2, color=color.black, shininess=0)

y = 0.18 * hh
lvaldrag = label(text='', height=30, box=False, color=orange, opacity=0)
rvaldrag = label(text='', height=30, box=False, color=orange, opacity=0)
oplabel = label(pos=vec(90, y, 0), text='', height=30, box=False, color=orange, opacity=0)
eqlabel = label(pos=vec(150, y, 0), text='', height=30, box=False, color=orange, opacity=0)
resultlabel = label(pos=vec(180, y, 0), text='', height=30, box=False, color=orange, opacity=0)

xleft = vec(60, y, 0)
xright = vec(120, y, 0)
xresult = vec(180, y, 0)

s = s.split('\n')
box(pos=vec(left - 15, top - 10 - lineheight * len(s) / 2, 0), size=vec(40, lineheight * len(s), 1),
    color=color.gray(0.5))
linenumbers = [None]
lines = [None]
for i in range(1, len(s) + 1):
    linenumbers.append(label(text="{}".format(i), pos=vec(left + 5, top - lineheight * (i), 0), align='right',
                             box=False, color=color.black, opacity=0, height=15))
    lines.append(label(text="{}".format(s[i - 1]), pos=vec(left + 15, top - lineheight * (i), 0), align='left',
                       box=False, color=color.black, opacity=0, height=15))

c = color.blue
label(pos=vec(left, hh - 10, 0), text='<b>Python Program</b>', align='left', color=c, box=False, opacity=1)
label(pos=vec(left, 0, 0), text='<b>Print Output</b>', align='left', color=c, box=False, opacity=1)

label(pos=vec(0.4 * hw, 0.85 * hh, 0), text='<b>Computer Processing Unit (CPU)</b>', color=c,
      align='center', height=0.05 * hh, box=0)
curve(pos=[vec(-40, 0, 0), vec(0.95 * hw, 0, 0), vec(0.95 * hw, 0.95 * hh, 0), vec(-40, 0.95 * hh, 0), vec(-40, 0, 0)],
      radius=5, color=c, shininess=0)

label(pos=vec(0.4 * hw, -55, 0), text='<b>Computer Memory</b>', color=c,
      align='center', height=0.05 * hh, box=0)
curve(pos=[vec(-40, -30, 0), vec(0.95 * hw, -30, 0), vec(0.95 * hw, -0.95 * hh, 0), vec(-40, 0. - 0.95 * hh, 0),
           vec(-40, -30, 0)],
      radius=5, color=c, shininess=0)

ytop = top - lineheight * 6.25
xend = left + 0.48 * hw
loopoutline = curve(pos=[vec(left + 10, ytop, 0), vec(xend, ytop, 0),
                         vec(xend, top - lineheight * 10.5, 0), vec(left + 10, top - lineheight * 10.5, 0),
                         vec(left + 10, ytop, 0)], radius=2, color=c, shininess=0, visible=False)

comment = label(pos=vec(-20, 0.75 * hh, 0), text='', align='left', color=color.black, box=False, opacity=0)
regular_prompt = vec((-40 + 0.95 * hw) / 2, 20, 0)
prompt = label(pos=regular_prompt, text='', align='center', color=color.black, box=False, opacity=0)
seetext = "Click the NEXT button to execute line {}."
nexttext = "Click the NEXT button to go to line {}."
varlabels = []  # attached to memory containers
vars = {}
names = ['a', 'b', 'sum']

for i in range(3):  # where to display the values of variables in memory
    tag = label(pos=vec(40, -i * 40 - shift + 15, 0), text=names[i], color=color.black, height=20, xoffset=-20,
                opacity=0, visible=False)
    lend = vec((40 + 0.85 * hw) / 2, -i * 40 - shift + 13, 0)
    value = label(pos=lend, text='', height=25, box=False, color=color.black, opacity=0)
    vars[names[i]] = {'result': 0, 'nvar': i, 'tag': tag, 'value': value}

prints = []  
p = ['<b>1  1</b>', '<b>2  3</b>', '<b>3  6</b>', '<b>sum = 6</b>']
for i in range(4):
    prints.append(label(pos=vec(left, -30 - i * 30, 0), text=p[i], height=23,
                        align='left', color=color.black, box=False, opacity=1, visible=False))

varcomment = label(align='left', text='''"a" is called a "variable" because its
value may vary during the program.''', pos=vec(-20, 0.75 * hh - 6 * lineheight, 0), box=False, color=orange, opacity=0,
                   visible=False)
a = 5
b = 1
sum = 0
step = 1

def clearmemory():
    for v in vars:
        vars[v]['tag'].visible = False
        vars[v]['value'].text = ''


def clearprints():
    for p in prints:
        p.visible = False


def reset():
    global a, b, sum
    a = 5
    b = 1
    sum = 0
    for L in [lvaldrag, rvaldrag, oplabel, eqlabel, resultlabel, comment, prompt]:
        L.text = ''
    varcomment.pos = vec(-20, 0.75 * hh - 6 * lineheight, 0)
    varcomment.text = '''"a" is called a "variable" because its
value may vary during the program.'''
    varcomment.visible = False
    prompt.pos = regular_prompt
    clearmemory()
    clearprints()
    
gotnext = False
gotrepeat = False


def nextb():
    global gotnext
    gotnext = True


def checknext():
    global gotnext
    if gotnext:
        gotnext = False
        return True
    return False


next = button(text='<b>NEXT</b>', bind=nextb)
scene.append_to_caption('   ')


def repeatb():
    global gotrepeat
    gotrepeat = True


def checkrepeat():
    global gotrepeat
    if gotrepeat:
        gotrepeat = False
        return True
    return False


rtext = '<b>Repeat line {}</b>'
repeat = button(text=rtext.format(1), bind=repeatb)
scene.append_to_caption(' ')


def toggle(i):  # toggles a statement between non-bold black with bold orange
    global step
    step = i
    L = lines[i]
    L.pos.x = left + 15
    if L.text[:3] == '<b>':
        L.text = L.text[3:-4]
        L.color = color.black
        L.height = 15
    else:
        L.text = '<b>' + L.text + '</b>'
        L.color = orange
        L.height = 23
        if 8 <= step <= 10:
            L.pos.x -= 10


def step1a():
    reset()
    repeat.text = rtext.format(step)
    repeat.disabled = True
    prompt.pos.y = hh / 2
    prompt.text = "Click the NEXT button to start the program."
    prompt.color = orange
    while True:
        rate(30)
        if checknext(): break
    if lines[1].color.equals(color.black): toggle(1)
    prompt.pos = regular_prompt
    prompt.text = ''
    comment.text = '''The CPU chooses an available container
in computer memory, places the number 5
in that container, and makes a note that
this location in memory can be referred
to with the name "a".'''
    varcomment.color = orange
    varcomment.visible = True
    prompt.color = color.black
    return [1, None, None, 5, None, None, 5, 'a']


def step1b(nt, bt):
    prompt.text = nexttext.format(2)
    prompt.color = orange
    comment.color = color.black
    if bt:
        vars['a']['value'].text = ''
        vars['a']['tag'].visible = False
        toggle(1)
        return
    varcomment.visible = False
    toggle(1)
    toggle(2)


def step2a():
    global a
    clearmemory()
    vars['a']['value'].text = '5'
    vars['a']['tag'].visible = True
    a = 5
    repeat.text = rtext.format(step)
    repeat.disabled = True
    comment.text = '''The CPU reads 5 from the "a" container,
adds 5+3 to make 8, and stores the 8
into the "a" container, overwriting the
previous contents. 

Note that in a Python program "a = a+5"
means <b>assign</b> the value of "a+5" to "a",
not that "a" is equal to "a+5".'''
    return [2, 'a', None, 5, 3, '+', 8, 'a']


def step2b(nt, bt):
    prompt.text = nexttext.format(3)
    prompt.color = orange
    if bt:
        vars['a']['value'].text = '5'
        toggle(2)
        toggle(2)
        return
    toggle(2)
    toggle(3)


def step3a():
    repeat.text = rtext.format(step)
    repeat.disabled = True
    clearmemory()
    vars['a']['value'].text = '8'
    vars['a']['tag'].visible = True
    comment.text = '''The CPU chooses an available container
in computer memory, places the number 10
in that container, and makes a note that
this location in memory can be referred
to with the name "b".'''
    return [3, None, None, 10, None, None, 10, 'b']


def step3b(nt, bt):
    prompt.text = nexttext.format(4)
    prompt.color = orange
    if bt:
        vars['b']['value'].text = ''
        vars['b']['tag'].visible = False
        toggle(3)
        toggle(3)
        return
    toggle(3)
    toggle(4)


def step4a():
    global a, b
    a = 8
    b = 10
    repeat.text = rtext.format(step)
    repeat.disabled = True
    clearmemory()
    vars['a']['value'].text = '8'
    vars['a']['tag'].visible = True
    vars['b']['value'].text = '10'
    vars['b']['tag'].visible = True
    comment.text = '''The CPU reads 8 from the "a" container,
reads 10 from the "b" container, adds 8+10
to make 18, and stores the 18 into the "a"
container, overwriting the previous contents.'''
    return [4, 'a', 'b', 8, 10, '+', 18, 'a']


def step4b(nt, bt):
    prompt.text = nexttext.format(5)
    prompt.color = orange
    if bt:
        vars['a']['value'].text = '8'
        toggle(4)
        toggle(4)
        return
    toggle(4)
    toggle(5)


def step5a():
    global a, b
    a = 18
    b = 10
    repeat.text = rtext.format(step)
    repeat.disabled = True
    clearmemory()
    vars['a']['value'].text = '18'
    vars['a']['tag'].visible = True
    vars['b']['value'].text = '10'
    vars['b']['tag'].visible = True
    comment.text = '''The CPU stores 1 into the "b" container,
overwriting the previous contents.'''
    return [5, None, None, 1, None, None, 1, 'b']


def step5b(nt, bt):
    prompt.text = nexttext.format(6)
    prompt.color = orange
    if bt:
        vars['b']['value'].text = '10'
        toggle(5)
        toggle(5)
        return
    toggle(5)
    toggle(6)


def step6a():
    global a, b
    a = 18
    b = 1
    repeat.text = rtext.format(step)
    repeat.disabled = True
    clearmemory()
    vars['a']['value'].text = '18'
    vars['a']['tag'].visible = True
    vars['b']['value'].text = '1'
    vars['b']['tag'].visible = True
    comment.text = '''The CPU chooses an available container
in computer memory, places 0 in that
container, and makes a note that this
location in memory can be referred to
with the name "sum".'''
    return [6, None, None, 0, None, None, 0, 'sum']


def step6b(nt, bt):
    prompt.text = nexttext.format(7)
    prompt.color = orange
    if bt:
        vars['sum']['value'].text = ''
        vars['sum']['tag'].visible = False
        toggle(6)
        toggle(6)
        return
    toggle(6)
    toggle(7)


def step7a():
    global b, sum
    if b == 1:
        sum = 0
    elif b == 2:
        sum = 1
    elif b == 3:
        sum = 3
    elif b == 4:
        sum = 6
    a = 18
    repeat.text = rtext.format(step)
    repeat.disabled = True
    clearmemory()
    vars['a']['value'].text = '18'
    vars['a']['tag'].visible = True
    vars['b']['value'].text = b
    vars['b']['tag'].visible = True
    vars['sum']['value'].text = sum
    vars['sum']['tag'].visible = True
    clearprints()
    for i in range(b - 1):
        prints[i].visible = True
    lvaldrag.pos = vec(120, 50, 0)
    lvaldrag.text = "{} < 4 ?".format(b)
    lvaldrag.color = color.black
    next = 8
    if b == 1:
        loopoutline.visible = True
        comment.text = '''Start of a "while" loop that repeatedly
executes the indented lines 8 through 10
until "b" is no longer less than 4. Initially
"b" is equal to 1, so the indented lines
will be executed. This loop will add up
the numbers 1 through 3, in "sum".

The outlined structure is called a "loop".'''
    elif b < 4:
        loopoutline.visible = False
        comment.text = '''The program reached the end of the
loop and branched back to line 7. Since
"b" is {}, which is less than 4, the CPU
will again execute the indented statements.'''.format(b)
    else:
        loopoutline.visible = False
        next = 11
        comment.text = '''The program reached the end of the
loop and branched back to line 7. Since 
"b" is 4, which is not less than 4, the
CPU will branch to line 11, exiting the
loop.'''
    prompt.text = 'Click the NEXT button to go to line {}.'.format(next)
    prompt.color = orange
    while True:
        rate(30)
        nt = checknext()
        bt = checkrepeat()
        if nt or bt: break
    lvaldrag.text = ''
    if bt:
        if b == 1:
            toggle(7)
            toggle(6)
            return
        else:
            toggle(7)
            toggle(10)
            return
    toggle(7)
    toggle(next)


def step8a():
    global b, sum
    if b == 1:
        sum = 0
        answer = 1
    elif b == 2:
        sum = 1
        answer = 3
    elif b == 3:
        sum = 3
        answer = 6
    repeat.text = rtext.format(step)
    repeat.disabled = True
    clearmemory()
    vars['a']['value'].text = '18'
    vars['a']['tag'].visible = True
    vars['b']['value'].text = b
    vars['b']['tag'].visible = True
    vars['sum']['value'].text = sum
    vars['sum']['tag'].visible = True
    clearprints()
    for i in range(b - 1):
        prints[i].visible = True
    comment.color = color.black
    p = 'incorrect'
    if prediction == answer:
        p = 'correct'
    comment.color = orange
    comment.text = 'Your "sum" prediction, {}, is {}.'.format(prediction, p)
    if b == 1:
        varcomment.visible = True
        varcomment.color = color.black
        varcomment.pos.y = comment.pos.y - 2 * lineheight
        varcomment.text = '''The CPU reads {} from the "sum" container,
reads {} from the "b" container, adds
{}+{} to make {}, and stores {} into
the "sum" container, overwriting the
previous contents.'''.format(sum, b, sum, b, sum + b, sum + b)
    next.disabled = False
    return [8, 'sum', 'b', sum, b, '+', sum + b, 'sum']


def step8b(nt, bt):
    varcomment.pos.y += 2 * lineheight
    varcomment.text = ''
    varcomment.visible = False
    comment.color = color.black
    comment.text = ''
    prompt.text = nexttext.format(9)
    prompt.color = orange
    if bt:
        vars['sum']['value'].text = sum - 1
        toggle(8)
        toggle(8)
        return
    toggle(8)
    toggle(9)


def step9a():
    global b, sum
    if b == 1:
        sum = 1
    elif b == 2:
        sum = 3
    elif b == 3:
        sum = 6
    repeat.text = rtext.format(step)
    repeat.disabled = True
    clearmemory()
    vars['a']['value'].text = '18'
    vars['a']['tag'].visible = True
    vars['b']['value'].text = b
    vars['b']['tag'].visible = True
    vars['sum']['value'].text = sum
    vars['sum']['tag'].visible = True
    clearprints()
    for i in range(b - 1):
        prints[i].visible = True
    comment.text = '''The CPU reads {} from the "b" container
and {} from the "sum" container, and
prints their values.'''.format(b, sum)
    return [9, 'b', 'sum', b, sum, None, None, None]


def step9b(nt, bt):
    prompt.text = nexttext.format(10)
    prompt.color = orange
    if bt:
        toggle(9)
        toggle(9)
        return
    toggle(9)
    toggle(10)


def step10a():
    global previous, b, sum
    if b == 1:
        sum = 1
    elif b == 2:
        sum = 3
    elif b == 3:
        sum = 6
    repeat.text = rtext.format(step)
    repeat.disabled = True
    clearmemory()
    vars['a']['value'].text = '18'
    vars['a']['tag'].visible = True
    vars['b']['value'].text = b
    vars['b']['tag'].visible = True
    vars['sum']['value'].text = sum
    vars['sum']['tag'].visible = True
    clearprints()
    for i in range(b):
        prints[i].visible = True
    comment.text = '''The CPU reads {} from the "b" container,
adds {}+1 to make {}, and stores {} into 
the "b" container, overwriting the
previous contents.'''.format(b, b, b + 1, b + 1)
    return [10, 'b', None, b, 1, '+', b + 1, 'b']


def step10b(nt, bt):
    global b
    prompt.text = "Branch back to line 7."
    prompt.color = orange
    if bt:
        b -= 1
        toggle(10)
        toggle(10)
        return
    toggle(10)
    toggle(7)


def step11a():
    global b, sum, step
    b = 4
    sum = 6
    repeat.text = rtext.format(step)
    repeat.disabled = True
    clearmemory()
    vars['a']['value'].text = '18'
    vars['a']['tag'].visible = True
    vars['b']['value'].text = b
    vars['b']['tag'].visible = True
    vars['sum']['value'].text = sum
    vars['sum']['tag'].visible = True
    clearprints()
    for i in range(b - 1):
        prints[i].visible = True
    comment.text = '''The CPU reads 6 from the "sum" container
and prints this value, with some text
to name the variable that is shown.'''.format(b, sum)
    return [11, None, 'sum', 'sum = ', sum, None, None, None]


def step11b(nt, bt):
    if bt:
        toggle(11)
        toggle(11)
        return
    toggle(11)
    toggle(1)  # return to start of program; this bolds line 1
    toggle(1)

prediction = None

keylabel = label(text='', pos=varcomment.pos + vec(20, -35, 0), box=False, align='left', visible=False)


def get_prediction(evt):
    global prediction
    prediction = evt.number


def execute():
    global a, b, sum, prediction

    # Note that a and b and sum have updating values in this program, set by execute
    R = 50  # animation rate
    pausing = 1.5
    params = []

    if step == 8:
        loopoutline.visible = False
        next.disabled = True
        repeat.disabled = True
        prediction = None
        prompt.text = ''
        comment.color = color.black
        comment.text = '''

In the input box at the bottom of the page,
type your prediction of what the value of 
"sum" will be after executing line 8.'''

        get0 = wtext(text='Type your prediction, then press ENTER: ')
        get = winput(bind=get_prediction)
        while True:
            rate(30)
            if prediction is not None: break
        get0.delete()
        get.delete()

    if step == 1:
        params = step1a()
    elif step == 2:
        params = step2a()
    elif step == 3:
        params = step3a()
    elif step == 4:
        params = step4a()
    elif step == 5:
        params = step5a()
    elif step == 6:
        params = step6a()
    elif step == 7:
        step7a()
        return
    elif step == 8:
        params = step8a()
    elif step == 9:
        params = step9a()
    elif step == 10:
        params = step10a()
    elif step == 11:
        params = step11a()

    linenum = params[0]
    leftarg = params[1]
    rightarg = params[2]
    leftvalue = params[3]
    rightvalue = params[4]
    op = params[5]
    result = params[6]
    store = params[7]

    prompt.text = seetext.format(step)
    prompt.color = color.black
    prompt.visible = True
    while True:
        rate(30)
        if checknext(): break
    prompt.visible = False

    if step == 2:
        comment.text = '''The CPU reads 5 from the "a" container,
adds 5+3 to make 8, and stores the 8
into the "a" container, overwriting the
previous contents.'''

    repeat.disabled = True
    next.disabled = True
    leftdrag = lvaldrag
    rightdrag = rvaldrag  # never changes
    leftdrag.visible = False
    rightdrag.visible = False
    nprints = 0
    isprint = (lines[linenum].text.find('print') >= 0)
    if isprint:
        for i, p in enumerate(prints):
            if not p.visible:
                nprints = i
                break
    if store in vars:
        nvar = vars[store]['nvar']
    if leftarg is None and rightarg is None:  # a = 5
        lstart = linenumbers[linenum].pos + vec(50, 0, 0)
        lend = xleft
        lmove = lend - lstart
        rmove = None
        lvaldrag.pos = lstart
        lvaldrag.color = orange
        lvaldrag.text = leftvalue
    elif rightarg is None:  # a = a+3
        lstart = vec((40 + 0.85 * hw) / 2, -vars[leftarg]['nvar'] * 40 - shift + 13, 0)
        lend = xleft
        lmove = lend - lstart
        lvaldrag.pos = lstart
        lvaldrag.color = color.black
        lvaldrag.text = leftvalue
        rstart = linenumbers[linenum].pos + vec(50, 0, 0)
        rend = xright
        rmove = rend - rstart
        rvaldrag.pos = rstart
        rvaldrag.color = orange
        rvaldrag.text = rightvalue
    elif leftarg is None:
        lstart = linenumbers[linenum].pos + vec(50, 0, 0)
        lend = xleft
        lmove = lend - lstart
        lvaldrag.pos = lstart
        lvaldrag.color = orange
        lvaldrag.text = leftvalue
        rstart = vec((40 + 0.85 * hw) / 2, -vars[rightarg]['nvar'] * 40 - shift + 13, 0)
        rend = xright
        rmove = rend - rstart
        rvaldrag.pos = rstart
        rvaldrag.color = orange
        rvaldrag.text = rightvalue
    else:  # a = a+b
        lstart = vec((40 + 0.85 * hw) / 2, -vars[leftarg]['nvar'] * 40 - shift + 13, 0)
        lend = xleft
        lmove = lend - lstart
        lvaldrag.pos = lstart
        lvaldrag.color = color.black
        lvaldrag.text = leftvalue
        rstart = vec((40 + 0.85 * hw) / 2, -vars[rightarg]['nvar'] * 40 - shift + 13, 0)
        rend = xright
        rmove = rend - rstart
        rvaldrag.pos = rstart
        rvaldrag.color = color.black
        rvaldrag.text = rightvalue
    leftdrag.visible = True
    rightdrag.visible = True

    for n in range(50):
        rate(R)
        leftdrag.pos += .02 * lmove
        if rmove is not None: rightdrag.pos += .02 * rmove

    if op is not None:
        oplabel.text = op
        eqlabel.text = '='
        resultlabel.pos = xresult
        resultlabel.text = result

    sleep(pausing)

    if leftarg is None and rightarg is None:  # a = 5
        lstart = lend
        lend = vec((40 + 0.85 * hw) / 2, -nvar * 40 - shift + 13, 0)
        lmove = lend - lstart
        leftdrag = lvaldrag
    elif rightarg is None:  # a = a+3
        lvaldrag.text = ''
        rvaldrag.text = ''
        oplabel.text = ''
        eqlabel.text = ''
        lstart = resultlabel.pos
        lend = vec((40 + 0.85 * hw) / 2, -vars[leftarg]['nvar'] * 40 - shift + 13, 0)
        lmove = lend - lstart
        leftdrag = resultlabel
    else:
        if isprint:
            lstart = lvaldrag.pos
            lend = vec(left, -30 - nprints * 30, 0)
            rstart = rvaldrag.pos
            rend = vec(left + 60, -30 - nprints * 30, 0)
            if step == 11:
                lend.x += 45
                rend.x += 40
            lmove = lend - lstart
            rmove = rend - rstart
            leftdrag = lvaldrag
        else:
            lvaldrag.text = ''
            rvaldrag.text = ''
            oplabel.text = ''
            eqlabel.text = ''
            lstart = resultlabel.pos = xresult
            lend = vec((40 + 0.85 * hw) / 2, -vars[leftarg]['nvar'] * 40 - shift + 13, 0)
            rmove = None
            leftdrag = resultlabel
        lmove = lend - lstart

    for n in range(50):
        rate(R)
        leftdrag.pos += .02 * lmove
        if rmove is not None: rightdrag.pos += .02 * rmove

    leftdrag.text = ''
    rvaldrag.text = ''
    if isprint:
        prints[nprints].visible = True
    else:
        vars[store]['tag'].visible = True
        vars[store]['value'].pos = lend
        vars[store]['value'].text = result
        if store == 'a':
            a = result
        elif store == 'b':
            b = result
        elif store == 'sum':
            sum = result

    repeat.disabled = False
    next.disabled = False
    if step == 10:
        prompt.text = nexttext.format(7)
    elif step == 11:
        prompt.text = nexttext.format(1)
    else:
        prompt.text = nexttext.format(step + 1)
    prompt.color = orange
    prompt.visible = True
    while True:
        rate(30)
        nt = checknext()
        bt = checkrepeat()
        if nt or bt: break

    if step == 1:
        step1b(nt, bt)
    elif step == 2:
        step2b(nt, bt)
    elif step == 3:
        step3b(nt, bt)
    elif step == 4:
        step4b(nt, bt)
    elif step == 5:
        step5b(nt, bt)
    elif step == 6:
        step6b(nt, bt)
    elif step == 7:
        return
    elif step == 8:
        step8b(nt, bt)
    elif step == 9:
        step9b(nt, bt)
    elif step == 10:
        step10b(nt, bt)
    elif step == 11:
        step11b(nt, bt)


while True:
    if step == 1: execute()
    if step == 2: execute()
    if step == 3: execute()
    if step == 4: execute()
    if step == 5: execute()
    if step == 6: execute()
    if step == 7: execute()  # looping on the value of b
    if step == 8: execute()
    if step == 9: execute()
    if step == 10: execute()
    if step == 11: execute()
