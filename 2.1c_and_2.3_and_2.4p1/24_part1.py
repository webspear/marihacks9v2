# using maths from https://physics.umd.edu/hep/drew/pendulum2.html
import matplotlib.pyplot as plt
import numpy as np

from util import animate_double

g = 9.81
m1 = 1
m2 = 1
l1 = 1
l2 = 1

t_0 = 0
t_end = 10
steps = 5000

# dt = 0.01
dt = (t_end - t_0) / steps
t = np.linspace(t_0, t_end, steps)

theta1 = np.zeros(steps)
omega1 = np.zeros(steps)

theta2 = np.zeros(steps)
omega2 = np.zeros(steps)

theta1[0] = np.pi / 2  # start position everything on the right
theta2[0] = np.pi / 2

omega1[0] = 0
omega2[0] = 0

M = m1 + m2

for i in range(steps - 1):
    d_theta = theta1[i] - theta2[i]

    # right beloe eqn 7
    c = m1 + m2 * np.sin(d_theta) ** 2
    # print(i, d_theta, c)

    # eqn 6
    n1 = -np.sin(d_theta) * (
        m2 * l1 * omega1[i] ** 2 * np.cos(d_theta) + m2 * l2 * omega2[i] ** 2
    ) - g * (M * np.sin(theta1[i]) - m2 * np.sin(theta2[i]) * np.cos(d_theta))

    a1 = n1 / (l1 * c)
    # print(1, n1, a1)
    # eqn 7
    n2 = np.sin(d_theta) * (
        M * l1 * omega1[i] ** 2 + m2 * l2 * omega2[i] ** 2 * np.cos(d_theta)
    ) + g * (M * np.sin(theta1[i]) * np.cos(d_theta) - M * np.sin(theta2[i]))

    a2 = n2 / (l2 * c)
    # print(2, n2, a2)
    # using eulers,
    # w_new = w_old + a * dt
    omega1[i + 1] = omega1[i] + a1 * dt
    omega2[i + 1] = omega2[i] + a2 * dt

    # theta_new = theta_old + w_new * dt
    theta1[i + 1] = theta1[i] + omega1[i + 1] * dt
    theta2[i + 1] = theta2[i] + omega2[i + 1] * dt

x1 = l1 * np.sin(theta1)
y1 = -l1 * np.cos(theta1)

x2 = x1 + l2 * np.sin(theta2)
y2 = y1 - l2 * np.cos(theta2)

plt.plot(x1, y1, label="trajectory of m1")
plt.plot(x2, y2, label="trajectory of m2")
plt.plot(0, 0, "o", label="origin")
plt.plot(x1[0], y1[0], "o", label="initial m1 position")
plt.plot(x2[0], y2[0], "o", label="initial m2 position")
plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc="upper right")
plt.grid(True)
plt.axis("equal")
animate_double(t, theta1, theta2)
plt.show()
