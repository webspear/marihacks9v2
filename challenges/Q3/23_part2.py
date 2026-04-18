import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np


def animate(t, theta, c="b"):
    l = 1
    x = l * np.sin(theta)
    y = -l * np.cos(theta)
    # print(x, y)
    fig, axe = plt.subplots(figsize=(6, 6))
    axe.set_aspect("equal")
    axe.grid(True)
    axe.set_xlabel("x")
    axe.set_ylabel("y")

    axe.set_xlim(-1.5, 1.5)
    axe.set_ylim(-1.5, 1.5)

    (line,) = axe.plot([], [], "-o", c=c, lw=3, markersize=10)

    def start():
        line.set_data([], [])
        return (line,)

    def update(frame):
        line.set_data([0, x[frame]], [0, y[frame]])
        # print(frame)
        return (line,)

    dt = t[1] - t[0] * 1000
    # print(dt)
    ani = anim.FuncAnimation(
        fig,
        update,
        frames=len(t),
        init_func=start,
        blit=True,
        interval=dt,
    )
    plt.show()


if __name__ == "__main__":
    g = 9.81
    l = 1
    t_0 = 0
    t_end = 10
    steps = 5000

    dt = (t_end - t_0) / steps

    t = np.linspace(t_0, t_end, steps)
    # print(len(t))
    theta = np.zeros(steps)
    omega = np.zeros(steps)

    theta[0] = np.pi / 2
    omega[0] = 0

    for i in range(steps - 1):
        # print("step", i)
        # using explicit euler - fah the energy not conserved
        # theta[i + 1] = theta[i] + omega[i] * dt
        # omega[i + 1] = omega[i] - (g / l) * np.sin(theta[i]) * dt

        # using semi implicit euler
        omega[i + 1] = omega[i] - (g / l) * np.sin(theta[i]) * dt
        theta[i + 1] = theta[i] + omega[i + 1] * dt
    animate(t, theta)
