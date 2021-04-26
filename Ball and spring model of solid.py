from vpython import *

N = 4
k = 1
m = 1
spacing = 1
atom_radius = 0.3 * spacing
L0 = spacing - 1.8 * atom_radius
V0 = pi * (0.5 * atom_radius) ** 2 * L0  # initial volume of spring
scene.background = color.black
scene.center = 0.5 * (N - 1) * vector(1, 1, 1)
dt = 0.04 * (2 * pi * sqrt(m / k))
axes = [vector(1, 0, 0), vector(0, 1, 0), vector(0, 0, 1)]

scene.caption = """A model of a solid represented as atoms connected by interatomic bonds.

To rotate "camera", drag with right button.
To zoom, drag with middle button or use scroll wheel.
  On a two-button mouse, middle is left + right.
Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""

class crystal:

    def atomAt(self, np):
        if (np.x >= 0 and np.y >= 0 and np.z >= 0 and np.x < N and np.y < N and np.z < N):
            return self.atoms[int(np.x + np.y * N + np.z * N * N)]
        w = box()
        w.visible = False
        w.radius = atom_radius
        w.pos = np * spacing
        w.momentum = vector(0, 0, 0)
        return w

    def __init__(self, N, atom_radius, spacing, momentumRange):
        self.atoms = []
        self.springs = []

        # Create N^3 atoms in a grid
        for z in range(N):
            for y in range(N):
                for x in range(N):
                    atom = sphere()
                    atom.pos = vector(x, y, z) * spacing
                    atom.radius = atom_radius
                    atom.color = vector(0, 0.58, 0.69)
                    px = 2 * random() - 1
                    py = 2 * random() - 1
                    pz = 2 * random() - 1
                    atom.momentum = momentumRange * vector(px, py, pz)
                    self.atoms.append(atom)

        # Create a grid of springs linking each atom to the adjacent atoms
        for d in range(3):
            for z in range(-1, N):
                for y in range(-1, N):
                    for x in range(-1, N):
                        atom = self.atomAt(vector(x, y, z))
                        neighbor = self.atomAt(vector(x, y, z) + axes[d])
                        if (atom.visible or neighbor.visible):
                            spring = helix()
                            spring.visible = atom.visible and neighbor.visible
                            spring.thickness = 0.05
                            spring.radius = 0.5 * atom_radius
                            spring.length = spacing
                            spring.atoms = [atom, neighbor]
                            spring.color = vector(1, 0.5, 0)
                            self.springs.append(spring)


c = crystal(N, atom_radius, spacing, 0.1 * spacing * sqrt(k / m))

while True:
    rate(40)
    for atom in c.atoms:
        atom.pos = atom.pos + atom.momentum / m * dt
    for spring in c.springs:
        spring.axis = spring.atoms[1].pos - spring.atoms[0].pos
        L = mag(spring.axis)
        spring.axis = spring.axis.norm()
        spring.pos = spring.atoms[0].pos + 0.5 * atom_radius * spring.axis
        Ls = L - 1 * atom_radius
        spring.length = Ls
        Fdt = spring.axis * (k * dt * (1 - spacing / L))
        spring.atoms[0].momentum = spring.atoms[0].momentum + Fdt
        spring.atoms[1].momentum = spring.atoms[1].momentum - Fdt
