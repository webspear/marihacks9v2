# i am using other constants as
# G and M_{moon} are huge/tiny and it creates fp inaccuracies
# we normalize it to be in moon radii units

# G = G * (Mm/||r||^2)r hat => F = -G * (Mm/||r||^3*r))
# applying newton's second law
# d^2r/dt^2 = -G*M*(r/||r||^3)
# ||r|| = sqrt(x^2+y^2)
# which gives us
# dx/dt = v_x
# dy/dt = v_y
# dv_x/dt = -GM * x/((x^2+y^2)^(3/2))
# dv_y/dt = -GM * y/((x^2+y^2)^(3/2))\
import matplotlib.pyplot as plt
import numpy as np

GM = 1  # set G*M to be 1 bc of above
t_0 = 0
t_end = 250  # at longer simulation time, the trajectory wants to go inwards/outwadrs bc of inaccuracie due to euler's method for odes
steps = 10000

dt = (t_end - t_0) / steps
t = np.linspace(t_0, t_end, steps)

x = np.zeros(steps)
y = np.zeros(steps)
vx = np.zeros(steps)
vy = np.zeros(steps)

x[0] = 1

vy[0] = 1.25  # initial tangential velocity

for i in range(steps - 1):
    d = (x[i] ** 2 + y[i] ** 2) ** 1.5

    ax = -GM * x[i] / d
    ay = -GM * y[i] / d
    vx[i + 1] = vx[i] + ax * dt
    vy[1 + i] = vy[i] + ay * dt

    x[i + 1] = x[i] + vx[i + 1] * dt
    y[i + 1] = y[i] + vy[1 + i] * dt

    # print("a", ax, ay,"v", vx[i + 1],vy[1 + i], "x",x[i + 1], "y", y[i + 1])
plt.plot(x, y, label="trajectory")

plt.plot(0, 0, "o", label="moon")

plt.plot(x[0], y[0], "o", label="start")

plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc="upper right")
plt.grid(True)
plt.axis("equal")
plt.show()
