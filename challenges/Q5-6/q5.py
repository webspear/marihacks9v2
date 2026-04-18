import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from euler_solver import all_steps
import math
from tqdm import tqdm
import signal


plt.rcParams["axes3d.mouserotationstyle"] = "azel"

# lorentz system parameters
# original, from wikipedia
sigma = 10
rho = 28
beta = 8 / 3

# sometimes stable
# sigma = 20
# rho = 20
# beta = 8 / 3

# stable
# sigma = 5
# rho = 5
# beta = 8 / 3


# simulation parameters
dt_sim = 5.0
step_count = 1000
n_frames = 500


# get derivatives of x,y,z
def dpdt(p):
    x, y, z = p
    return np.array((sigma * (y - x), x * (rho - z) - y, x * y - beta * z))


# initial position animation
def initial_pos(t):
    t *= math.tau
    return np.array((0, 0, 25)) + 5 * np.array(
        (math.sin(t), math.cos(t), math.sin(2 * t))
    )


ps = np.zeros((n_frames, step_count + 1, 3))
for i in tqdm(range(len(ps))):
    ps[i] = all_steps(dt_sim, step_count, initial_pos(i / len(ps)), dpdt)


# plotting

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.view_init(elev=20.0, azim=-35)
min_v = np.minimum.reduce(ps, axis=(0, 1))
max_v = np.maximum.reduce(ps, axis=(0, 1))
ax.set_xlim(min_v[0], max_v[0])
ax.set_ylim(min_v[1], max_v[1])
ax.set_zlim(min_v[2], max_v[2])
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

(line,) = ax.plot(*ps[0].T, color="tab:blue")
(start,) = ax.plot(*ps[0][0], "o", color="tab:green", label="start")
(end,) = ax.plot(*ps[0][-1], "o", color="tab:red", label="end")

ax.legend(handlelength=0, bbox_to_anchor=(1, 1), loc="upper left")
ax.text2D(
    1.0,
    0.0,
    f"Δt = {dt_sim:.5g}\n{step_count} steps",
    verticalalignment="bottom",
    transform=ax.transAxes,
)
ax.text2D(
    -0.1,
    0.0,
    f"ρ = {rho:.5g}\nσ = {sigma:.5g}\nβ = {beta:.5g}",
    verticalalignment="bottom",
    transform=ax.transAxes,
)
init_pos = ax.text2D(
    -0.1,
    1.0,
    "",
    verticalalignment="top",
    transform=ax.transAxes,
)

rng = np.random.default_rng()


def update(i):
    line.set_data_3d(ps[i].T)
    start.set_data_3d(np.expand_dims(ps[i][0], -1))
    end.set_data_3d(np.expand_dims(ps[i][-1], -1))
    # end.set_offsets(end.get_offsets() + 1)
    init_pos.set_text(
        f"x₀ = {ps[i][0][0]:.5f}\ny₀ = {ps[i][0][1]:.5f}\nz₀ = {ps[i][0][2]:.5f}",
    )


ani = FuncAnimation(fig, update, frames=len(ps), interval=16)

signal.signal(signal.SIGINT, lambda *_: plt.close())
plt.show()
