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

    (line,) = axe.plot([], [], "-o", c=c)

    def start():
        line.set_data([], [])
        return (line,)

    def update(i):
        line.set_data([0, x[i]], [0, y[i]])
        # print(i)
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


def animate_double(t, theta1, theta2):
    l1 = 1
    l2 = 1

    x1 = l1 * np.sin(theta1)
    y1 = -l1 * np.cos(theta1)

    x2 = x1 + l2 * np.sin(theta2)
    y2 = y1 - l2 * np.cos(theta2)
    # print(x1, y1, x2, y2)

    fig, axe = plt.subplots(figsize=(6, 6))
    axe.set_aspect("equal")  # adjustable="box"
    axe.grid(True)
    axe.set_xlabel("x")
    axe.set_ylabel("y")

    b = (l1 + l2) * 1.5
    axe.set_xlim(-b, b)
    axe.set_ylim(-b, b)

    (line,) = axe.plot([], [], "-o")
    (trace,) = axe.plot([], [], "-")

    def start():
        line.set_data([], [])
        trace.set_data([], [])
        return line, trace

    def update(i):
        # print(i)
        # trans = np.linspace(0.1, 1, len(x2[start:i]))
        # trace.set_alpha(trans)
        line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])

        start = max(0, i - 400)  # back
        trace.set_data(x2[start:i], y2[start:i])

        return line, trace

    dt = (t[1] - t[0]) * 1000

    ani = anim.FuncAnimation(
        fig,
        update,
        frames=len(t),
        init_func=start,
        blit=True,
        interval=dt,
    )
    plt.show()
