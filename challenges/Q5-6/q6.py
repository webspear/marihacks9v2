import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.colors import to_rgb
import pandas as pd
import numpy as np
from scipy.integrate import solve_ivp
from euler_solver import after_t
import signal
import os

# we pick the simple pendulum as the mechanical system
g = 9.8
l = 1.0


def dpdt(p):
    a, dadt = p.T
    return np.array((dadt, -(g / l) * np.sin(a))).T


# I couldn't find an exact solution online so you'll have to take this


def after_t_exact(t: float, p, dpdt):
    rtol = 1e-12
    atol = 1e-15
    ps = np.copy(p)
    for i, p in enumerate(ps):
        ps[i] = solve_ivp(
            lambda _, p: dpdt(p), (0, t), p, t_eval=[t], rtol=rtol, atol=atol
        ).y[:, 0]
    return ps


# reading the polygon
scale = 2.0
offset = np.array((0, 0))
df = pd.read_csv(os.path.join(__file__, "..", "cat.csv"))
boundary_parts = [
    df[[f"x{i}", f"y{i}"]].dropna().to_numpy(dtype="float64") * scale + offset
    for i in list(dict.fromkeys(int(col[1:]) for col in df.columns))
]
for i, loop in enumerate(boundary_parts):
    if not np.all(loop[-1] == loop[0]):
        boundary_parts[i] = np.vstack((loop, loop[0]))
# assume the boundary parts are correctly oriented
# also assume that mapping the region preserves its boundary

sign = 1


def area(bp):
    total = 0
    for loop in bp:
        a = loop[:-1]
        b = loop[1:]
        total += np.sum(a[:, 0] * b[:, 1] - b[:, 0] * a[:, 1])
    return sign * total / 2


if area(boundary_parts) < 0:
    sign = -1


def path(bp):
    vs, cs = [], []
    for loop in bp:
        vs.append(np.vstack((loop, (0, 0))))
        cs += [Path.MOVETO] + [Path.LINETO] * (len(loop) - 1) + [Path.CLOSEPOLY]
    return Path(np.vstack(vs), cs)


def draw_region(ax, bp, color="tab:blue", with_area=True):
    ax.add_patch(
        PathPatch(
            path(bp),
            fc=(*to_rgb(color), 0.4),
            ec=(*to_rgb(color), 1),
            lw=1.5,
        )
    )
    ax.set_axisbelow(True)
    ax.grid(True)
    ax.set_xlim(-scale + offset[0], scale + offset[0])
    ax.set_ylim(-scale + offset[1], scale + offset[1])
    if with_area:
        a = area(bp)
        ax.text(0.1, 0.1, f"area = {a}", transform=ax.transAxes)


# region plots

fig, ax = plt.subplots(2, 2)
draw_region(ax[0, 0], boundary_parts)
ax[0, 0].set_title("Original region")

t = 1.0
draw_region(ax[1, 0], [after_t_exact(t, p, dpdt) for p in boundary_parts])
ax[1, 0].set_title(f"Exact region, {t}s")

n = 100
draw_region(ax[0, 1], [after_t(t, n, p, dpdt) for p in boundary_parts])
ax[0, 1].set_title(f"Euler ({n} steps)")

n = 10_000
draw_region(ax[1, 1], [after_t(t, n, p, dpdt) for p in boundary_parts])
ax[1, 1].set_title(f"Euler ({n} steps)")


plt.tight_layout()

# Error chart


def area_error(t: float, step_count: int, bp):
    original_area = area(bp)
    euler_area = area([after_t(t, step_count, ps, dpdt) for ps in bp])
    return abs(euler_area - original_area)


fig2, ax2 = plt.subplots()
t = 5.0
ax2.set_title(f"Error of mapped area estimation (t={t})")
step_counts = [100, 300, 1000, 3000, 10000, 30000, 100000]
original_area = area(boundary_parts)
errors = [
    abs(original_area - area([after_t(t, n, p, dpdt) for p in boundary_parts]))
    for n in step_counts
]
ax2.plot(step_counts, errors)
ax2.set_xlabel("Log step count")
ax2.set_ylabel("Area deviation")
ax2.set_xscale("log")
ax2.set_axisbelow(True)
ax2.grid(True)


signal.signal(signal.SIGINT, lambda *_: plt.close())
plt.show()
